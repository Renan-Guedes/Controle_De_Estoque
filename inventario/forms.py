from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Categoria, Produto, LimiteProduto, MovimentoEstoque

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu e-mail'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Labels
        self.fields['username'].label = 'Usuário'
        self.fields['email'].label = 'E-mail'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmar senha'

        # Classes
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Seu usuário'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Crie sua senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme sua senha'
        })

        # Help texts
        if self.fields['password1'].help_text:
            self.fields['password1'].help_text = 'Sua senha deve ser segura e difícil de adivinhar.'
        if self.fields['password2'].help_text:
            self.fields['password2'].help_text = 'Digite a mesma senha para confirmação.'

class CategoriaForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Categoria'})
    )
    
    ativo = forms.CheckboxInput(attrs={'class': 'form-check-input'})
    
    class Meta:
        model = Categoria
        fields = ['nome', 'ativo']
        
class ProdutoForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Produto'})
    )
    
    sku = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU do Produto'}),
        required=False
    )
    
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do Produto', 'rows': 3}),
        required=False
    )
    
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    ativo = forms.CheckboxInput(attrs={'class': 'form-check-input'})
    
    class Meta:
        model = Produto
        # quantidade_atual removido: será sempre 0 no cadastro
        fields = ['nome', 'sku', 'descricao', 'categoria', 'ativo']

class LimiteProdutoForm(forms.ModelForm):
    limite_minimo = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Limite Mínimo'})
    )
    
    limite_ideal = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Limite Ideal'})
    )
    
    tipo_limite = forms.ChoiceField(
        choices=LimiteProduto.TIPOS_LIMITE,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = LimiteProduto
        fields = ['limite_minimo', 'limite_ideal', 'tipo_limite']

class MovimentoEstoqueForm(forms.ModelForm):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tipo_movimento = forms.ChoiceField(
        choices=MovimentoEstoque.TIPOS_MOVIMENTO,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    quantidade = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'})
    )
    
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do Movimento', 'rows': 3}),
        required=False
    )
    
    class Meta:
        model = MovimentoEstoque
        fields = ['produto', 'tipo_movimento', 'quantidade', 'descricao']