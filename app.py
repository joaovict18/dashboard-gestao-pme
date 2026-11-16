from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Gestão PME | Dashboard de vendas",
    page_icon="📊",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "vendas.csv"
REQUIRED_COLUMNS = {"data", "produto", "quantidade", "valor"}


@st.cache_data
def load_sales_data() -> pd.DataFrame:
    """Carrega e prepara a base sintética de vendas."""
    data = pd.read_csv(DATA_PATH, parse_dates=["data"])
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Colunas obrigatórias ausentes na base: {missing}")

    data["faturamento"] = data["quantidade"] * data["valor"]
    return data


def format_currency(value: float) -> str:
    """Formata valores em reais no padrão usado no dashboard."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def build_abc_table(data: pd.DataFrame) -> pd.DataFrame:
    """Calcula a curva ABC por faturamento acumulado."""
    abc = (
        data.groupby("produto", as_index=False)
        .agg(faturamento=("faturamento", "sum"), quantidade=("quantidade", "sum"))
        .sort_values("faturamento", ascending=False)
    )
    abc["participacao"] = abc["faturamento"] / abc["faturamento"].sum()
    abc["participacao_acumulada"] = abc["participacao"].cumsum()
    abc["classe"] = abc["participacao_acumulada"].apply(
        lambda value: "A" if value <= 0.80 else ("B" if value <= 0.95 else "C")
    )
    return abc


st.title("📊 Gestão PME")
st.markdown(
    "#### Uma visão simples e prática do caixa de uma **Pequena e Média Empresa**"
)
st.caption(
    "Dados demonstrativos e sintéticos para fins de portfólio. "
    "O faturamento considera quantidade × valor unitário."
)

try:
    sales = load_sales_data()
except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
    st.error(f"Não foi possível carregar a base de vendas: {error}")
    st.stop()

with st.sidebar:
    st.header("Filtros")
    min_date = sales["data"].min().date()
    max_date = sales["data"].max().date()
    selected_dates = st.date_input(
        "Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    selected_products = st.multiselect(
        "Produtos",
        options=sorted(sales["produto"].unique()),
        default=sorted(sales["produto"].unique()),
    )

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = end_date = selected_dates

filtered_sales = sales[
    sales["data"].dt.date.between(start_date, end_date)
    & sales["produto"].isin(selected_products)
].copy()

if filtered_sales.empty:
    st.warning("Nenhuma venda encontrada para os filtros selecionados.")
    st.stop()

total_revenue = filtered_sales["faturamento"].sum()
average_ticket = filtered_sales["faturamento"].mean()
items_sold = filtered_sales["quantidade"].sum()

metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Faturamento total", format_currency(total_revenue))
metric_2.metric("Ticket médio", format_currency(average_ticket))
metric_3.metric("Itens vendidos", f"{items_sold:,.0f}".replace(",", "."))

st.divider()

left_column, right_column = st.columns([1.7, 1])

with left_column:
    st.subheader("Curva ABC por faturamento")
    abc_data = build_abc_table(filtered_sales)
    abc_chart = px.bar(
        abc_data,
        x="produto",
        y="faturamento",
        color="classe",
        category_orders={"produto": abc_data["produto"].tolist()},
        color_discrete_map={"A": "#0f766e", "B": "#f59e0b", "C": "#94a3b8"},
        labels={"produto": "Produto", "faturamento": "Faturamento (R$)", "classe": "Classe"},
        template="plotly_white",
    )
    abc_chart.update_layout(
        legend_title_text="Classe ABC",
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis_tickprefix="R$ ",
    )
    st.plotly_chart(abc_chart, use_container_width=True)
    st.caption(
        "A: produtos que concentram até 80% do faturamento acumulado; "
        "B: até 95%; C: faixa restante."
    )

with right_column:
    st.subheader("Resumo por produto")
    summary = (
        filtered_sales.groupby("produto", as_index=False)
        .agg(
            Faturamento=("faturamento", "sum"),
            Quantidade=("quantidade", "sum"),
            Vendas=("produto", "size"),
        )
        .sort_values("Faturamento", ascending=False)
    )
    summary["Faturamento"] = summary["Faturamento"].map(format_currency)
    st.dataframe(summary, hide_index=True, use_container_width=True)

st.subheader("Vendas no período")
daily_sales = (
    filtered_sales.groupby("data", as_index=False)["faturamento"]
    .sum()
    .sort_values("data")
)
daily_chart = px.line(
    daily_sales,
    x="data",
    y="faturamento",
    markers=True,
    labels={"data": "Data", "faturamento": "Faturamento (R$)"},
    template="plotly_white",
)
daily_chart.update_traces(line_color="#0f766e")
daily_chart.update_layout(margin=dict(l=0, r=0, t=10, b=0), yaxis_tickprefix="R$ ")
st.plotly_chart(daily_chart, use_container_width=True)
