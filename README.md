# 📊 Dashboard para Controle de Finanças Pessoais — V1

## 🎯 Objetivo

O objetivo deste projeto é oferecer uma ferramenta simples, intuitiva e eficiente para organização financeira pessoal.  
A aplicação permite que qualquer usuário registre receitas, despesas e categorias, acompanhe sua evolução financeira e visualize métricas importantes de forma clara e acessível.

Além disso, o sistema foi projetado para suportar múltiplos usuários, garantindo segurança, privacidade e uma experiência totalmente personalizada.

---

## 📘 Introdução

Este projeto foi desenvolvido com foco em **usabilidade**, **clareza** e **organização**, utilizando:

- **Streamlit** como interface principal  
- **SQLite** como banco de dados local  
- Arquitetura modular para facilitar manutenção e expansão  

A aplicação oferece um fluxo completo de autenticação:

- Criação de conta  
- Login  
- Recuperação de senha  
- Sessão persistente  
- Multiusuário isolado  

Após o login, o usuário tem acesso a um painel financeiro completo, onde pode:

- Registrar lançamentos (receitas e despesas)  
- Criar categorias personalizadas  
- Acompanhar métricas financeiras  
- Visualizar gráficos de evolução  
- Exportar dados filtrados para Excel  
- Trabalhar com lançamentos recorrentes e parcelados  

O projeto foi estruturado para ser escalável, permitindo futuras expansões como:

- Integração com APIs externas  
- Dashboards avançados  
- Sincronização em nuvem  
- Notificações inteligentes  

---

## 🎯 Metas (O que queremos visualizar)

A aplicação foi construída com o objetivo de entregar uma visão clara e completa da vida financeira do usuário.  
Entre as metas principais, estão:

### **1. Controle financeiro centralizado**
- Visualizar receitas, despesas e saldo consolidado  
- Acompanhar saldo inicial, final e previsto  
- Entender rapidamente a saúde financeira do mês  

### **2. Análises visuais e intuitivas**
- Gráficos de receitas por categoria  
- Gráficos de despesas por categoria  
- Evolução financeira ao longo do tempo  
- Indicadores de pagamentos pendentes e realizados  

### **3. Organização e categorização**
- Criar e gerenciar categorias personalizadas  
- Filtrar lançamentos por mês e ano  
- Exportar dados filtrados para Excel  

### **4. Fluxo completo de autenticação**
- Criar conta  
- Login  
- Recuperação de senha  
- Sessão persistente  
- Multiusuário isolado  

### **5. Lançamentos inteligentes**
- Lançamentos recorrentes  
- Parcelamento automático  
- Registro de status (pago/pendente)  
- Histórico completo por usuário  

---

## 🚀 Como iniciar o aplicativo

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicializar o banco de dados (primeira vez)

O banco é criado automaticamente na primeira execução, incluindo:
- Tabela de usuários
- Tabela de transações
- Tabela de categorias
- Tabela de saldos
Se quiser garantir do zero, basta apagar o arquivo *data\finance.db* (se existir) antes de rodar.

### 5. Executar o aplicativo

```bash
streamlit run run.py
```

ou 

```bash
python -m streamlit run run.py
```

### 6. Acessar no navegador

Após rodar o comando, acesse:
- http://localhost:8501
Você verá a tela de Login, com opção de:
- Criar nova conta
- Recuperar senha
- Acessar o dashboard após autenticação
