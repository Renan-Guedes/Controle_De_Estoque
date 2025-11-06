from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, LimiteProduto
from .forms import LimiteProdutoForm, MovimentoEstoqueForm, ProdutoForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator

def registrar(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro bem-sucedido. Agora você pode fazer o login.')
            return redirect('inventario:login')
    else:
        form = RegistrationForm()
    return render(request, 'inventario/registrar.html', {'form': form})

def logout_view(request):
    ''' Faz logout do usuário e redireciona para a página de login '''
    logout(request)
    messages.info(request, 'Você foi desconectado.')
    return redirect('inventario:login')

@login_required
def home(request):
    lista_produtos = Produto.objects.filter(ativo=True, deletado_em__isnull=True).order_by('nome')
    
    # Paginação
    itens_por_pagina = request.GET.get('itens_por_pagina', 10)
    paginator = Paginator(lista_produtos, itens_por_pagina)
    pagina = request.GET.get('pagina')
    produtos = paginator.get_page(pagina)
    
    for produto in produtos:
        try:
            limite = produto.limite
            status = limite.get_status(produto.quantidade_atual)
            produto.limite_minimo = limite.limite_minimo
            produto.limite_ideal = limite.limite_ideal
        except LimiteProduto.DoesNotExist:
            status = 'Sem limite definido'
        produto.status = status
    
    contexto = {'produtos': produtos, 'itens_por_pagina': itens_por_pagina}
    
    return render(request, 'inventario/home.html', contexto)

@login_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.quantidade_atual = 0
            produto.save()
            messages.success(request, 'Produto criado com sucesso.')
            return redirect('inventario:home')
        else:
            messages.error(request, f'Por favor, corrija os erros abaixo: {form.errors}')
    else:
        form = ProdutoForm()
    return render(request, 'inventario/produto_form.html', {'form': form})

@login_required
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso.')
            return redirect('inventario:home')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'inventario/produto_form.html', {'form': form})

@login_required
def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    produto.delete()
    messages.success(request, 'Produto excluído com sucesso.')
    return redirect('inventario:home')

@login_required
def limite_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    try:
        limite = produto.limite
    except LimiteProduto.DoesNotExist:
        limite = None

    if request.method == 'POST':
        form = LimiteProdutoForm(request.POST, instance=limite)
        if form.is_valid():
            limite = form.save(commit=False)
            limite.produto = produto
            limite.save()
            messages.success(request, 'Limites do produto atualizados com sucesso.')
            return redirect('inventario:home')
    else:
        form = LimiteProdutoForm(instance=limite)

    return render(request, 'inventario/produto_limite.html', {
        'form': form,
        'produto': produto
    })
    
@login_required
def movimentacao_estoque(request):
    if request.method == 'POST':
        form = MovimentoEstoqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimento de estoque registrado com sucesso.')
            return redirect('inventario:home')
    else:
        form = MovimentoEstoqueForm()
    return render(request, 'inventario/movimentacao_estoque.html', {'form': form})