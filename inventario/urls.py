from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Produto URLs
    path('produto/criar/', views.criar_produto, name='criar_produto'),
    path('produto/<int:pk>/editar/', views.editar_produto, name='editar_produto'),
    path('produto/<int:pk>/deletar/', views.deletar_produto, name='deletar_produto'),
    path('produto/<int:pk>/limite/', views.limite_produto, name='limite_produto'),
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    
    # Movimento de Estoque
    path('movimentacao_estoque/', views.movimentacao_estoque, name='movimentacao_estoque'),
    
    # Categorias
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/criar/', views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/deletar/', views.deletar_categoria, name='deletar_categoria'),
]