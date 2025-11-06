from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import F
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='categorias')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    deletado_em = models.DateTimeField(null=True, blank=True)
    
    def delete(self, *args, **kwargs):
        self.deletado_em = timezone.now()
        self.ativo = False
        self.save()
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='produtos')
    sku = models.CharField(max_length=50, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='produtos')
    quantidade_atual = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    deletado_em = models.DateTimeField(null=True, blank=True)
    
    def delete(self, *args, **kwargs):
        self.deletado_em = timezone.now()
        self.ativo = False
        self.save()

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        
class LimiteProduto(models.Model):
    
    TIPOS_LIMITE = [
        ('valor', 'Valor'),
        ('porcentagem', 'Porcentagem'),
    ]
    
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE, related_name='limite')
    limite_minimo = models.IntegerField(default=0)
    limite_ideal = models.IntegerField(default=0)
    tipo_limite = models.CharField(max_length=20, choices=TIPOS_LIMITE, default='valor')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def get_status(self, quantidade):
        if self.tipo_limite == 'porcentagem':
            limite_minimo = int(self.limite_minimo)
            limite_ideal = int(self.limite_ideal)
            
            # Calcula o valor ideal do limite baixo baseada na porcentagem
            limite_baixo = (limite_minimo / 100) * limite_ideal
            
            if quantidade >= limite_ideal:
                return 'ideal'
            elif quantidade <= limite_baixo:
                return 'baixo'
            else:
                return 'normal'
        else:
            if quantidade >= int(self.limite_ideal):
                return 'ideal'
            elif quantidade <= int(self.limite_minimo):
                return 'baixo'
            else:
                return 'normal'

class MovimentoEstoque(models.Model):
    TIPOS_MOVIMENTO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    tipo_movimento = models.CharField(max_length=20, choices=TIPOS_MOVIMENTO)
    data_movimento = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField(blank=True, null=True)
    
    def _effect(self, tipo: str, quantidade: int) -> int:
        return quantidade if tipo == 'entrada' else -quantidade

    def clean(self):
        super().clean()
        if self.quantidade is None or self.quantidade < 0:
            raise ValidationError({'quantidade': 'Quantidade deve ser 0 ou positiva.'})
        if self.tipo_movimento not in dict(self.TIPOS_MOVIMENTO):
            raise ValidationError({'tipo_movimento': 'Tipo de movimento inválido.'})

    def save(self, *args, **kwargs):

        prod = Produto.objects.select_for_update().get(pk=self.produto_id)
        delta = self._effect(self.tipo_movimento, self.quantidade)
        if prod.quantidade_atual + delta < 0:
            raise ValidationError('Operação resultaria em estoque negativo.')
        Produto.objects.filter(pk=prod.pk).update(
            quantidade_atual=F('quantidade_atual') + delta
        )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            prod = Produto.objects.select_for_update().get(pk=self.produto_id)
            delta = -self._effect(self.tipo_movimento, self.quantidade)
            if prod.quantidade_atual + delta < 0:
                raise ValidationError('Exclusão resultaria em estoque negativo.')
            Produto.objects.filter(pk=prod.pk).update(
                quantidade_atual=F('quantidade_atual') + delta
            )
            super().delete(*args, **kwargs)