from django.test import TestCase
from django.contrib.auth.models import User
from .models import Produto, MovimentoEstoque
from django.core.exceptions import ValidationError


class MovimentoEstoqueTests(TestCase):
	def setUp(self):
		self.user = User.objects.create(username='tester')
		self.produto = Produto.objects.create(nome='Produto X', usuario=self.user, quantidade_atual=0)

	def test_entrada_incrementa_estoque(self):
		mov = MovimentoEstoque.objects.create(produto=self.produto, quantidade=10, tipo_movimento='entrada')
		self.produto.refresh_from_db()
		self.assertEqual(self.produto.quantidade_atual, 10)

	def test_saida_decrementa_estoque(self):
		MovimentoEstoque.objects.create(produto=self.produto, quantidade=10, tipo_movimento='entrada')
		mov_saida = MovimentoEstoque.objects.create(produto=self.produto, quantidade=4, tipo_movimento='saida')
		self.produto.refresh_from_db()
		self.assertEqual(self.produto.quantidade_atual, 6)

	def test_update_movimento_altera_diferenca(self):
		mov = MovimentoEstoque.objects.create(produto=self.produto, quantidade=5, tipo_movimento='entrada')
		self.produto.refresh_from_db()
		self.assertEqual(self.produto.quantidade_atual, 5)
		mov.quantidade = 8
		mov.save()
		self.produto.refresh_from_db()
		self.assertEqual(self.produto.quantidade_atual, 8)

	def test_troca_tipo_movimento(self):
		mov = MovimentoEstoque.objects.create(produto=self.produto, quantidade=5, tipo_movimento='entrada')
		mov.tipo_movimento = 'saida'
		mov.save()
		self.produto.refresh_from_db()
		# Inicial +5, mudança para saída de 5 implica delta -10 total (5 - (+5)) => resultado -5 é inválido e deve levantar erro
		# Portanto deve lançar ValidationError
		self.assertEqual(self.produto.quantidade_atual, 5)  # não alterado porque save deve falhar

	def test_prevent_negative_stock(self):
		with self.assertRaises(ValidationError):
			MovimentoEstoque.objects.create(produto=self.produto, quantidade=3, tipo_movimento='saida')

	def test_delete_reverte_efeito(self):
		mov = MovimentoEstoque.objects.create(produto=self.produto, quantidade=7, tipo_movimento='entrada')
		self.produto.refresh_from_db()
		self.assertEqual(self.produto.quantidade_atual, 7)
		mov.delete()
		self.produto.refresh_from_db()
		self.assertEqual(self.produto.quantidade_atual, 0)
