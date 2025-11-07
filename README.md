# Sistema de Controle de Estoque (Django)

Projeto Django com autenticação de usuários, gerenciamento de produtos, categorias, limites de estoque e movimentações (entradas e saídas).

## Principais Funcionalidades
- Cadastro e autenticação de usuários (login, logout, registro)
- Cadastro, edição, listagem e soft delete de produtos
- Definição de limites de estoque por produto (quantidade absoluta ou percentual)
- Controle de movimentações de estoque (entrada e saída)
- Ajuste automático de quantidade atual do produto quando uma movimentação é criada
- Cadastro e gerenciamento de categorias (ativas por padrão; exclusão via soft delete)
- Filtro de exibição apenas para produtos e categorias ativos / não deletados
- Prevenção de estoque negativo
- Navegação contextual com retorno à tela de origem via parâmetro `next` (com redirecionamento seguro)

## Arquitetura e Organização
```
projeto/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── projeto/                # Configurações globais do Django
│   ├── settings.py
│   ├── urls.py              # Inclui urls do app inventario
│   ├── asgi.py / wsgi.py
├── inventario/              # App principal de estoque
│   ├── models.py            # Produto, Categoria, LimiteProduto, MovimentoEstoque
│   ├── views.py             # Lógica de negócios e fluxos (CRUD, movimentos)
│   ├── forms.py             # Formulários
│   ├── urls.py              # Rotas
│   ├── migrations/          # Histórico de migrações
│   └── templates/inventario/# Templates específicos do app
│       ├── home.html
│       ├── login.html / registrar.html
│       ├── produto_form.html / produto_lista.html / produto_limite.html
│       ├── categoria_form.html / categoria_lista.html
│       └── movimentacao_estoque.html
└── templates/
    └── base.html            # Layout base estendido pelos templates do app
```

## Modelos
- `Produto`: nome, categoria, quantidade_atual (gerenciada automaticamente), ativo, deletado_em (soft delete)
- `Categoria`: nome, ativo, deletado_em (soft delete)
- `LimiteProduto`: produto, tipo_limite (absoluto ou percentual), valor_limite, método `get_status()`
- `MovimentoEstoque`: produto, tipo (entrada/saida), quantidade, descricao

## Autenticação
Configurações de redirecionamento no `settings.py` usam nomes namespaced:
```
LOGIN_URL = 'inventario:login'
LOGIN_REDIRECT_URL = 'inventario:home'
LOGOUT_REDIRECT_URL = 'inventario:login'
```

## Requisitos
- Python 3.11+ (recomendado 3.11 ou 3.12)
- Django >= 5.0, < 6.0
- Pip para instalar dependências

## Instalação (Windows PowerShell)
```powershell
# 1. Criar ambiente virtual (opcional mas recomendado)
python -m venv .venv

# 2. Ativar ambiente
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Aplicar migrações iniciais
python manage.py migrate

# 5. Rodar servidor de desenvolvimento
python manage.py runserver
```
Acesse: http://127.0.0.1:8000/

## Endpoints Principais
| Caminho | Nome | Descrição |
|--------|------|-----------|
| `/` | `inventario:home` | Dashboard inicial / visão geral |
| `/login/` | `inventario:login` | Página de login |
| `/registrar/` | `inventario:registrar` | Cadastro de novo usuário |
| `/logout/` | `inventario:logout` | Logout |
| `/produtos/` | `inventario:listar_produtos` | Lista de produtos ativos |
| `/produto/criar/` | `inventario:criar_produto` | Formulário de criação de produto |
| `/produto/<id>/editar/` | `inventario:editar_produto` | Editar produto |
| `/produto/<id>/deletar/` | `inventario:deletar_produto` | Soft delete do produto |
| `/produto/<id>/limite/` | `inventario:limite_produto` | Definir/editar limite do produto |
| `/categorias/` | `inventario:listar_categorias` | Listagem de categorias ativas |
| `/categorias/criar/` | `inventario:criar_categoria` | Criar categoria |
| `/categorias/<id>/editar/` | `inventario:editar_categoria` | Editar categoria |
| `/categorias/<id>/deletar/` | `inventario:deletar_categoria` | Soft delete da categoria |
| `/movimentacao_estoque/` | `inventario:movimentacao_estoque` | Registrar entrada/saída |

## 📄 Licença
Declaro que esse sistema pode ser utilizado mediante citação de seu criador **[Renan Guedes](https://github.com/Renan-Guedes)**.

---
Se tiver dúvidas ou quiser evoluir o projeto, abra uma issue ou faça um fork. Bom desenvolvimento! 👨‍💻
