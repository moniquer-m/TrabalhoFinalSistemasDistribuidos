# Documentacao do Projeto de Autenticação e Gerenciamento de Usuários Baseado em Privilegio

## Descrição da Proposta do Trabalho

Este projeto implementa um sistema de autenticação e gerenciamento de usuários utilizando Flask, um framework web em Python. O sistema permite o registro de novos usuários, login, logout, visualização e atualização de perfis de usuário, além de funcionalidades administrativas para gerenciar todos os usuários.

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

## Comunicação Cliente-Servidor

A comunicação entre o cliente e o servidor é realizada através de requisições HTTP. Aqui está um diagrama de sequência simplificado para o processo de login:

## Descrição do Serviço no Servidor

O servidor utiliza Flask para gerenciar as rotas e processar as requisições. Ele implementa as seguintes funcionalidades principais:

1. **Autenticação de Usuários**: Verifica as credenciais fornecidas e cria sessões para usuários autenticados.
2. **Gerenciamento de Usuários**: Permite a criação, leitura, atualização e exclusão de usuários.
3. **Controle de Acesso**: Restringe o acesso a certas rotas com base nas permissões do usuário.
4. **Armazenamento de Dados**: Utiliza um sistema de armazenamento (por exemplo, um banco de dados) para manter as informações dos usuários.
