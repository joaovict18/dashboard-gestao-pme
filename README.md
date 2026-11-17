# 📊 Gestão PME

> Dashboard de vendas para apoiar decisões rápidas de um pequeno comércio.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/feito%20com-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Licença](https://img.shields.io/badge/licença-MIT-2ea44f)](LICENSE)

## Sobre o projeto

**PME** significa **Pequenas e Médias Empresas**. Este projeto simula o caixa
de um pequeno comércio usando uma base pública e sintética de vendas. A ideia
é transformar registros simples de venda em informações úteis para gestão:

- faturamento total do período;
- ticket médio por venda registrada;
- quantidade total de itens vendidos;
- curva ABC de produtos por faturamento;
- evolução diária do faturamento;
- resumo comparativo por produto.

O campo `valor` da base representa o **valor unitário**. Assim, cada venda tem
seu faturamento calculado por `quantidade × valor`.

## ✨ Demonstração

![Prévia do dashboard](https://placehold.co/1200x650/0f766e/ffffff?text=Gestao+PME+Dashboard)

[Acessar o dashboard online](https://gestao-pme.streamlit.app/)

O aplicativo oferece filtros por período e produto. A curva ABC classifica:

- **A:** produtos que acumulam até 80% do faturamento;
- **B:** produtos que acumulam de 80% a 95%;
- **C:** produtos restantes.

> Os dados são fictícios e foram criados exclusivamente para demonstração e
> portfólio. Não representam clientes ou transações reais.

## 📁 Estrutura

```text
.
├── app.py                 # Aplicação Streamlit
├── data/
│   └── vendas.csv         # Base sintética pública
├── requirements.txt       # Dependências do projeto
└── README.md
```

### Dicionário de dados

| Coluna | Tipo | Descrição |
|---|---|---|
| `data` | data | Data da venda |
| `produto` | texto | Produto vendido |
| `quantidade` | inteiro | Unidades vendidas |
| `valor` | decimal | Valor unitário em reais |

## 🚀 Executar localmente

Requisitos: Python 3.10 ou superior.

```bash
git clone https://github.com/joaovict18/dashboard-gestao-pme.git
cd dashboard-gestao-pme
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

O navegador abrirá o dashboard em `http://localhost:8501`.

## ☁️ Deploy imediato no Streamlit Community Cloud

1. Crie um repositório **público** no GitHub, por exemplo
   `dashboard-gestao-pme`.
2. Na pasta do projeto, publique os commits:

   ```bash
   git remote add origin https://github.com/joaovict18/dashboard-gestao-pme.git
   git branch -M main
   git push -u origin main
   ```

3. Acesse [share.streamlit.io](https://share.streamlit.io/) e entre com sua
   conta do GitHub.
4. Clique em **Create app** e selecione:
   - **Repository:** `joaovict18/dashboard-gestao-pme`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Clique em **Deploy**. O Streamlit instalará automaticamente as dependências
   de `requirements.txt` e fornecerá uma URL pública para seu portfólio.

Sempre que você fizer `git push` para a branch `main`, o app será atualizado
automaticamente. Para compartilhar o resultado, adicione a URL gerada pelo
Streamlit na descrição do repositório e no seu currículo/portfólio.

O dashboard publicado está disponível em:
<https://gestao-pme.streamlit.app/>

## 🧩 Próximas evoluções

- importar vendas reais via banco de dados;
- incluir margem de lucro e estoque;
- criar metas mensais e alertas;
- adicionar autenticação para dados privados.

## Licença

Este projeto está sob a licença MIT. A base de dados é sintética e pode ser
reutilizada para estudos e demonstrações.
