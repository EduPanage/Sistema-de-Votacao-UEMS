# 🗳️ Sistema de Votação Digital - UEMS

**Universidade Estadual de Mato Grosso do Sul**  
**Desenvolvido por:** Eduardo Panage Avila (RGM 802.456)  
**Supervisor:** Alfred Forster Junior  
**Período:** Julho a Setembro de 2025

---

## 📋 Sobre o Sistema

Sistema web desenvolvido para gerenciar e realizar eleições digitais institucionais da UEMS de forma segura, transparente e eficiente. A plataforma permite a criação de eleições, cadastro de candidatos e eleitores, votação online e apuração automática de resultados.

### Principais Características:
- ✅ Autenticação segura via Google OAuth2
- ✅ Interface intuitiva e responsiva
- ✅ Voto secreto garantido
- ✅ Comprovante de votação (hash SHA-256)
- ✅ Notificações automáticas por e-mail
- ✅ Dashboard administrativo completo
- ✅ Apuração em tempo real

---

## 🎯 Casos de Uso

Este sistema é ideal para:
- Eleições de reitor(a) e vice-reitor(a)
- Eleições de diretores de unidade
- Consultas a conselhos universitários
- Votações de diretórios acadêmicos
- Plebiscitos e referendos internos
- Eleições de representantes estudantis

---

## 🛠️ Tecnologias Utilizadas

### Backend:
- **Python 3.11**
- **Django 5.0** - Framework web principal
- **PostgreSQL 14** - Banco de dados relacional
- **Django Allauth** - Sistema de autenticação OAuth2

### Frontend:
- **Bootstrap 5.3** - Framework CSS responsivo
- **Bootstrap Icons** - Biblioteca de ícones
- **JavaScript** - Interatividade client-side

### Infraestrutura:
- **Docker & Docker Compose** - Containerização
- **Gunicorn** - Servidor WSGI para produção

---

## 📦 Requisitos do Sistema

### Para Desenvolvimento:
- Python 3.11 ou superior
- PostgreSQL 14 ou superior
- Git para controle de versão
- Conta Google para OAuth2 (configuração)

### Para Produção com Docker:
- Docker 20.10+
- Docker Compose 2.0+

---

## 🚀 Instalação e Configuração

### Método 1: Docker (Recomendado)

#### 1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd sistema-votacao-uems
```

#### 2. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto:

```env
# Django
SECRET_KEY=gere-uma-chave-secreta-forte-aqui
DEBUG=False
ALLOWED_HOSTS=votacao.uems.br,localhost

# PostgreSQL
DB_NAME=votacao_uems
DB_USER=postgres
DB_PASSWORD=senha_forte_do_banco
DB_HOST=db
DB_PORT=5432

# Google OAuth2
GOOGLE_CLIENT_ID=seu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=seu-client-secret

# E-mail SMTP
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@uems.br
EMAIL_HOST_PASSWORD=senha_de_app_do_gmail
DEFAULT_FROM_EMAIL=Sistema de Votação UEMS <noreply@uems.br>
```

#### 3. Inicie os containers:
```bash
docker-compose up -d --build
```

#### 4. Execute as migrações:
```bash
docker-compose exec web python manage.py migrate
```

#### 5. Crie o superusuário:
```bash
docker-compose exec web python manage.py createsuperuser
```

#### 6. Acesse o sistema:
- Interface principal: http://localhost:8000
- Painel administrativo: http://localhost:8000/admin

---

### Método 2: Instalação Local

#### 1. Clone e configure ambiente virtual:
```bash
git clone [URL_DO_REPOSITORIO]
cd sistema-votacao-uems
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

#### 2. Instale as dependências:
```bash
pip install -r requirements.txt
```

#### 3. Configure o PostgreSQL:
```sql
-- Abra o psql e execute:
CREATE DATABASE votacao_uems;
CREATE USER votacao_admin WITH PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE votacao_uems TO votacao_admin;
```

#### 4. Configure o arquivo `.env` (mesmo do Método 1)

#### 5. Execute as migrações:
```bash
python manage.py migrate
```

#### 6. Crie o superusuário:
```bash
python manage.py createsuperuser
```

#### 7. Inicie o servidor:
```bash
python manage.py runserver
```

---

## 🔐 Configuração do Google OAuth2

### 1. Acesse o Google Cloud Console:
https://console.cloud.google.com/

### 2. Crie um novo projeto ou selecione existente

### 3. Ative a Google+ API:
- APIs e Serviços → Biblioteca
- Busque por "Google+ API"
- Clique em "Ativar"

### 4. Configure a tela de consentimento:
- APIs e Serviços → Tela de consentimento OAuth
- Tipo: Interno (para UEMS)
- Preencha as informações obrigatórias

### 5. Crie as credenciais:
- APIs e Serviços → Credenciais
- Criar credenciais → ID do cliente OAuth 2.0
- Tipo de aplicativo: Aplicativo da Web
- URIs de redirecionamento autorizados:
  - http://localhost:8000/accounts/google/login/callback/
  - https://votacao.uems.br/accounts/google/login/callback/

### 6. Copie as credenciais para o `.env`:
- Client ID → GOOGLE_CLIENT_ID
- Client Secret → GOOGLE_CLIENT_SECRET

---

## 📧 Configuração de E-mail

### Para Gmail Institucional:

#### 1. Ative a Verificação em 2 Etapas:
https://myaccount.google.com/security

#### 2. Gere uma Senha de App:
https://myaccount.google.com/apppasswords
- Selecionar app: E-mail
- Selecionar dispositivo: Outro (Sistema Votação UEMS)
- Copie a senha gerada

#### 3. Configure no `.env`:
```env
EMAIL_HOST_USER=noreply@uems.br
EMAIL_HOST_PASSWORD=senha_de_app_de_16_caracteres
```

### Para Servidor SMTP Institucional:
Contate o TI da UEMS para obter:
- Endereço do servidor SMTP
- Porta (587 ou 465)
- Credenciais de acesso

---

## 📖 Guia de Uso do Sistema

### Para Administradores:

#### Criar uma Eleição:
1. Acesse o Dashboard (/painel/dashboard/)
2. Clique em "Criar Nova Eleição"
3. Preencha os dados:
   - Tema da eleição
   - Descrição detalhada
   - Data e hora de início
   - Data e hora de término
   - Tipo de voto (único ou múltiplo)
4. Salve a eleição

#### Adicionar Candidatos:
1. Após criar a eleição, você será redirecionado
2. Digite o nome do candidato/opção
3. Clique em "Adicionar"
4. Repita para todos os candidatos
5. Clique em "Próximo: Adicionar Eleitores"

#### Cadastrar Eleitores:
1. Digite nome completo e e-mail (@uems.br ou @gmail.com)
2. Clique em "Adicionar Eleitor"
3. Repita para todos os eleitores autorizados
4. Clique em "Publicar Eleição"

#### Publicar Eleição:
1. Revise todas as informações
2. Confirme a publicação
3. E-mails serão enviados automaticamente
4. A eleição aparecerá na página inicial conforme as datas

#### Visualizar Resultados:
1. Aguarde o término da eleição
2. Acesse o Dashboard ou página inicial
3. Clique em "Ver Resultados"
4. Os votos são contados automaticamente

---

### Para Eleitores:

#### Como Votar:
1. Receba o e-mail de notificação
2. Clique em "Votar Agora" ou acesse votacao.uems.br
3. Faça login com sua conta Google (@uems.br)
4. Selecione a eleição ativa
5. Escolha sua opção de voto
6. Confirme o voto
7. Guarde o comprovante (hash) gerado

#### Importante:
- Use o **mesmo e-mail** cadastrado como eleitor
- Você pode votar **apenas uma vez** por eleição
- O voto é **secreto** e não pode ser alterado
- Guarde o hash para auditorias futuras

---

## 🗂️ Estrutura do Projeto

```
sistema-votacao-uems/
├── core/                          # Aplicação principal
│   ├── migrations/                # Migrações do banco de dados
│   ├── templates/                 # Templates HTML
│   │   ├── core/
│   │   │   ├── admin/            # Dashboard administrativo
│   │   │   ├── elections/        # Gerenciamento de eleições
│   │   │   ├── voting/           # Sistema de votação
│   │   │   ├── results/          # Visualização de resultados
│   │   │   ├── pages/            # Páginas institucionais
│   │   │   └── emails/           # Templates de e-mail
│   │   ├── account/              # Templates de autenticação
│   │   └── socialaccount/        # Templates OAuth2
│   ├── static/                    # Arquivos estáticos (CSS, JS, imagens)
│   ├── models.py                  # Modelos do banco de dados
│   ├── views.py                   # Lógica de negócio
│   ├── forms.py                   # Formulários Django
│   ├── urls.py                    # Rotas da aplicação
│   └── admin.py                   # Configuração do admin
├── votacao_project/               # Configurações do projeto
│   ├── settings.py                # Configurações principais
│   ├── urls.py                    # Rotas principais
│   └── wsgi.py                    # Configuração WSGI
├── docker-compose.yml             # Configuração Docker
├── Dockerfile                     # Imagem Docker
├── requirements.txt               # Dependências Python
├── .env                           # Variáveis de ambiente (não versionado)
├── .gitignore                     # Arquivos ignorados pelo Git
└── README.md                      # Este arquivo
```

---

## 🔒 Segurança Implementada

### Autenticação e Autorização:
- ✅ Login obrigatório via Google OAuth2
- ✅ Verificação de e-mail cadastrado
- ✅ Permissões por tipo de usuário (admin/eleitor)

### Proteção de Dados:
- ✅ Proteção CSRF em todos os formulários
- ✅ Voto secreto (sem vínculo eleitor-candidato)
- ✅ Hash SHA-256 para comprovante de voto
- ✅ Um voto por eleitor por eleição

### Banco de Dados:
- ✅ PostgreSQL com transações ACID
- ✅ Senhas criptografadas (Django default)
- ✅ Backups automáticos (configurar em produção)

### Infraestrutura:
- ✅ Variáveis sensíveis em .env
- ✅ DEBUG=False em produção
- ✅ HTTPS obrigatório (configurar no servidor)

---

## 🧪 Testes

### Executar testes unitários:
```bash
python manage.py test
```

### Verificar cobertura de código:
```bash
coverage run --source='.' manage.py test
coverage report
```

### Testar envio de e-mail:
```bash
python manage.py shell
```
```python
from django.core.mail import send_mail

send_mail(
    subject='Teste Sistema Votação UEMS',
    message='E-mail de teste',
    from_email='noreply@uems.br',
    recipient_list=['seu_email@uems.br'],
)
```

---

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'core'"
```bash
# Certifique-se de estar no ambiente virtual
pip install -r requirements.txt
```

### Erro: "OperationalError: FATAL: password authentication failed"
```bash
# Verifique as credenciais no .env
# Teste a conexão com PostgreSQL:
psql -U postgres -h localhost -d votacao_uems
```

### Erro: "SMTPAuthenticationError"
```bash
# Verifique se a senha de app do Gmail está correta
# Certifique-se que a verificação em 2 etapas está ativa
```

### Eleitor não consegue votar:
- ✅ Verifique se o e-mail cadastrado é exatamente o mesmo do login
- ✅ Confirme que a eleição está no período ativo
- ✅ Verifique se o eleitor já não votou

### E-mails não estão sendo enviados:
- ✅ Verifique as configurações SMTP no .env
- ✅ Teste o envio manual via shell
- ✅ Verifique a pasta de spam do destinatário

---

## 📊 Backup e Manutenção

### Backup do Banco de Dados:
```bash
# Com Docker:
docker-compose exec db pg_dump -U postgres votacao_uems > backup_$(date +%Y%m%d).sql

# Sem Docker:
pg_dump -U postgres votacao_uems > backup_$(date +%Y%m%d).sql
```

### Restaurar Backup:
```bash
# Com Docker:
docker-compose exec -T db psql -U postgres votacao_uems < backup_20250919.sql

# Sem Docker:
psql -U postgres votacao_uems < backup_20250919.sql
```

### Logs do Sistema:
```bash
# Com Docker:
docker-compose logs -f web

# Sem Docker:
# Logs estarão no console do runserver
```

---

## 🔄 Atualização do Sistema

### 1. Pare o sistema:
```bash
docker-compose down  # ou Ctrl+C no runserver
```

### 2. Atualize o código:
```bash
git pull origin main
```

### 3. Atualize as dependências:
```bash
pip install -r requirements.txt  # ou rebuild do Docker
```

### 4. Execute novas migrações:
```bash
python manage.py migrate
# ou
docker-compose exec web python manage.py migrate
```

### 5. Colete arquivos estáticos (produção):
```bash
python manage.py collectstatic --noinput
```

### 6. Reinicie o sistema:
```bash
docker-compose up -d
# ou
python manage.py runserver
```
