import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

@st.cache_data
def carregar_dados():
    df = pd.read_csv("Chocolate Sales.csv")
    df["Amount"] = df["Amount"].replace('[\$,]', '', regex=True).astype(float)
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")
    return df

df = carregar_dados()

st.title("Dashboard de Vendas de Chocolate")

# Filtros
with st.sidebar:
    st.header("Filtros")
    paises = ["Todos"] + sorted(df["Country"].unique())
    pais = st.selectbox("Filtrar por País", paises)
    if pais != "Todos":
        df = df[df["Country"] == pais]

    data_min = df["Date"].min()
    data_max = df["Date"].max()
    data_inicial, data_final = st.date_input("Intervalo de Datas", [data_min, data_max])
    df = df[(df["Date"] >= pd.to_datetime(data_inicial)) & (df["Date"] <= pd.to_datetime(data_final))]

col1, col2, col3 = st.columns(3)
col1.metric("Total em Vendas", f"${df['Amount'].sum():,.2f}")
col2.metric("Total de Caixas", int(df["Boxes Shipped"].sum()))
col3.metric("Produto Mais Vendido", df["Product"].mode()[0])

st.markdown("---")

# Abas
aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "Faturamento Mensal",
    "Produtos Mais Vendidos",
    "Top Vendedores",
    "Vendas por País",
    "Análises Avançadas"
])

with aba1:
    df["Ano-Mês"] = df["Date"].dt.to_period("M").astype(str)
    vendas_mensais = df.groupby("Ano-Mês")["Amount"].sum()
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.lineplot(x=vendas_mensais.index, y=vendas_mensais.values, marker="o", ax=ax1)
    ax1.set_xlabel("Mês")
    ax1.set_ylabel("Total em Vendas ($)")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with aba2:
    st.subheader("Top 5 Produtos")
    produtos = df["Product"].value_counts().head(5)
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.barplot(x=produtos.values, y=produtos.index, palette="Greens_d", ax=ax2)
    ax2.set_xlabel("Número de Vendas")
    ax2.set_ylabel("Produto")
    st.pyplot(fig2)

with aba3:
    st.subheader("Top 5 Vendedores (por Receita)")
    top_vendedores = df.groupby("Sales Person")["Amount"].sum().sort_values(ascending=False).head(5)
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    sns.barplot(x=top_vendedores.values, y=top_vendedores.index, palette="Blues_d", ax=ax3)
    ax3.set_xlabel("Valor Vendido ($)")
    ax3.set_ylabel("Vendedor")
    st.pyplot(fig3)

with aba4:
    st.subheader("Vendas por País")
    vendas_pais = df.groupby("Country")["Amount"].sum().sort_values(ascending=False)
    fig4, ax4 = plt.subplots(figsize=(10, 4))
    sns.barplot(x=vendas_pais.values, y=vendas_pais.index, palette="Purples_d", ax=ax4)
    ax4.set_xlabel("Valor Vendido ($)")
    ax4.set_ylabel("País")
    st.pyplot(fig4)

with aba5:
    st.subheader("Dispersão: Valor vs. Caixas (Plotly)")
    fig5 = px.scatter(
        df,
        x="Boxes Shipped",
        y="Amount",
        color="Sales Person",
        hover_data=["Product", "Country", "Date"],
        title="Relacionamento entre Valor e Caixas Enviadas"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Heatmap: Vendedor vs Produto")
    heatmap_data = pd.pivot_table(df, values="Amount", index="Sales Person", columns="Product", aggfunc="sum", fill_value=0)
    fig6, ax6 = plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax6)
    st.pyplot(fig6)

    st.subheader("Tabela de Dados")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Baixar Dados Filtrados", data=csv, file_name="dados_filtrados.csv", mime="text/csv")
