# Documentação do Projeto de Autenticação e Gerenciamento de Usuários Baseado em Privilegio

## Descrição da Proposta do Trabalho

Este projeto implementa um sistema robusto de autenticação e gerenciamento de usuários utilizando Flask, um framework web leve e poderoso em Python. O sistema é projetado para oferecer uma solução segura e escalável para aplicações web que necessitam de controle de acesso baseado em privilégios.

### Objetivos Principais:

1. **Autenticação Segura**: Implementar um sistema de login que utiliza técnicas modernas de criptografia (Argon2) para proteger as senhas dos usuários.

2. **Gerenciamento de Usuários**: Permitir o registro de novos usuários, bem como a visualização e atualização de perfis existentes.

3. **Controle de Acesso Baseado em Papéis**: Implementar um sistema de privilégios que distingue entre diferentes tipos de usuários (por exemplo, clientes, PQLs e administradores), cada um com permissões específicas.

4. **Interface Administrativa**: Desenvolver uma área administrativa para gerenciar todos os usuários do sistema, incluindo a capacidade de criar, atualizar e excluir contas.

5. **Segurança Aprimorada**: Incorporar medidas de segurança como proteção contra ataques de força bruta, validação de entrada e sanitização de dados.

6. **Experiência de Usuário Intuitiva**: Criar uma interface de usuário amigável e responsiva para todas as funcionalidades do sistema.

### Funcionalidades Chave:

- Registro de novos usuários com validação de dados
- Login seguro com proteção contra tentativas excessivas
- Logout e gerenciamento de sessões
- Recuperação de senha via e-mail
- Visualização e edição de perfil de usuário
- Painel administrativo para gerenciamento de usuários
- Filtros e pesquisas para facilitar a administração de usuários

## Modelo de Dados

O sistema utiliza o seguinte modelo de dados:

- **User**:
  - id (int): Identificador único do usuário
  - username (string): Nome de usuário
  - password (string): Senha hash
  - email (string): Endereço de e-mail
  - role (string): Função do usuário (admin, cliente, pql)

## Configuração e Instalação

Para configurar e executar este projeto, siga os passos abaixo:

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

### Passos de Instalação

1. Clone o repositório

2. Crie um ambiente virtual (recomendado):
python -m venv venv source venv/bin/activate # No Windows use venv\Scripts\activate

3. Instale as dependências:
pip install flask
pip install flask-login
pip install passlib

### Executando o Projeto

Para iniciar o servidor de desenvolvimento, execute:

python run.py

O servidor será iniciado e estará acessível em `http://localhost:5000` por padrão.

### Notas Adicionais

- Certifique-se de que todas as dependências estão instaladas corretamente.

Se encontrar problemas durante a instalação ou execução:
1. Verifique se todas as dependências foram instaladas corretamente.
2. Verifique os logs de erro para informações mais detalhadas.

## Requisitos Funcionais

### Cliente (Frontend)

1. **Registro de Usuário**: Envio de POST request com dados do novo usuário.
2. **Login**: Envio de POST request com credenciais do usuário.
3. **Logout**: Envio de GET request para encerrar a sessão.
4. **Visualização de Perfil**: Envio de GET request para obter dados do usuário.
5. **Atualização de Perfil**: Envio de POST request com dados atualizados do usuário.
6. **Área Administrativa**: Envio de GET e POST requests para gerenciar usuários (apenas para admins).

### Servidor (Backend)

1. **Processamento de Registro**: Recebimento de POST request, validação de dados e criação de novo usuário.
2. **Autenticação**: Recebimento de POST request, verificação de credenciais e criação de sessão.
3. **Gerenciamento de Sessão**: Criação e destruição de sessões de usuário.
4. **Recuperação de Dados**: Fornecimento de dados de usuário em resposta a GET requests.
5. **Atualização de Dados**: Recebimento de POST request e atualização de dados do usuário.
6. **Funcionalidades Administrativas**: Processamento de requests para listar, atualizar e excluir usuários.

## Descrição do Serviço no Servidor

O servidor utiliza Flask para gerenciar as rotas e processar as requisições. Ele implementa as seguintes funcionalidades principais:

1. **Autenticação de Usuários**: Verifica as credenciais fornecidas e cria sessões para usuários autenticados.
2. **Gerenciamento de Usuários**: Permite a criação, leitura, atualização e exclusão de usuários.
3. **Controle de Acesso**: Restringe o acesso a certas rotas com base nas permissões do usuário.
4. **Armazenamento de Dados**: Utiliza um sistema de armazenamento (por exemplo, um banco de dados) para manter as informações dos usuários.

## Comunicação Cliente-Servidor

A comunicação entre o cliente (frontend) e o servidor (backend) neste projeto é baseada em uma arquitetura cliente-servidor típica, utilizando o protocolo HTTP para troca de informações. Esta abordagem permite uma separação clara de responsabilidades e facilita a escalabilidade e manutenção do sistema.

### Fluxo de Comunicação

1. **Requisição do Cliente**: O cliente (geralmente um navegador web) inicia a comunicação enviando uma requisição HTTP para o servidor. Estas requisições podem ser de diferentes tipos (GET, POST, PUT, DELETE) dependendo da ação desejada.

2. **Processamento no Servidor**: O servidor Flask recebe a requisição, a processa com base na rota solicitada e executa a lógica de negócio necessária.

3. **Resposta do Servidor**: Após o processamento, o servidor envia uma resposta HTTP de volta ao cliente. Esta resposta geralmente inclui um código de status HTTP e pode conter dados no corpo da resposta (frequentemente em formato JSON).

4. **Processamento no Cliente**: O cliente recebe a resposta e atualiza a interface do usuário conforme necessário.

### Exemplo de Fluxo: Processo de Login

Aqui está um exemplo detalhado do fluxo de comunicação para o processo de login:

1. O cliente envia uma requisição POST para `/login` com as credenciais do usuário.
2. O servidor recebe a requisição e verifica as credenciais.
3. Se as credenciais forem válidas, o servidor cria uma sessão e envia uma resposta de sucesso.
4. O cliente recebe a resposta e redireciona para o dashboard.
5. O cliente envia uma requisição GET para `/dashboard`.
6. O servidor verifica a sessão, recupera os dados necessários e envia de volta ao cliente.
7. O cliente recebe os dados e renderiza o dashboard.

### Segurança na Comunicação

- **HTTPS**: Todas as comunicações são realizadas sobre HTTPS para garantir a criptografia dos dados em trânsito.
- **Tokens de Sessão**: Após o login bem-sucedido, o servidor gera um token de sessão que é usado para autenticar requisições subsequentes.
- **Validação de Entrada**: Todas as entradas do cliente são validadas no servidor para prevenir injeções e outros ataques.

### Formato de Dados

- A maioria das trocas de dados entre cliente e servidor utiliza o formato JSON.
- Para uploads de arquivos, é utilizado o formato multipart/form-data.

### Tratamento de Erros

- O servidor envia códigos de status HTTP apropriados (200 para sucesso, 400 para erros do cliente, 500 para erros do servidor).
- Mensagens de erro detalhadas são incluídas no corpo da resposta para facilitar o debugging e melhorar a experiência do usuário.

### Otimização

- Caching é implementado onde apropriado para reduzir a carga no servidor e melhorar o tempo de resposta.
- As respostas são comprimidas quando possível para reduzir o volume de dados transferidos.

Esta arquitetura de comunicação permite uma interação eficiente e segura entre o frontend e o backend, fornecendo uma base sólida para as funcionalidades do sistema de autenticação e gerenciamento de usuários.


