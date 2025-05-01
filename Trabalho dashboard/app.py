import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

@st.cache_data
def carregar_dados():
    df = pd.read_csv("Chocolate Sales.csv")
    df["Amount"] = df["Amount"].replace('[\$,]', '', regex=True).astype(float)
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")
    return df

df = carregar_dados()

paises = ["Todos"] + sorted(df["Country"].unique())
pais = st.selectbox("Filtrar por País", paises)
if pais != "Todos":
    df = df[df["Country"] == pais]

st.title("Dashboard de Vendas de Chocolate")

col1, col2, col3 = st.columns(3)
col1.metric("Total em Vendas", f"${df['Amount'].sum():,.2f}")
col2.metric("Total de Caixas", int(df["Boxes Shipped"].sum()))
col3.metric("Produto Mais Vendido", df["Product"].mode()[0])

st.markdown("---")

df["Ano-Mês"] = df["Date"].dt.to_period("M").astype(str)
vendas_mensais = df.groupby("Ano-Mês")["Amount"].sum()

st.subheader("Faturamento por Mês")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(x=vendas_mensais.index, y=vendas_mensais.values, marker="o", ax=ax1)
ax1.set_xlabel("Mês")
ax1.set_ylabel("Total em Vendas ($)")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("Produtos Mais Vendidos")
produtos = df["Product"].value_counts().head(5)

fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(x=produtos.values, y=produtos.index, palette="Greens_d", ax=ax2)
ax2.set_xlabel("Número de Vendas")
ax2.set_ylabel("Produto")
st.pyplot(fig2)

st.subheader("Top 5 Vendedores (por Receita)")
top_vendedores = df.groupby("Sales Person")["Amount"].sum().sort_values(ascending=False).head(5)

fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.barplot(x=top_vendedores.values, y=top_vendedores.index, palette="Blues_d", ax=ax3)
ax3.set_xlabel("Valor Vendido ($)")
ax3.set_ylabel("Vendedor")
st.pyplot(fig3)

st.subheader("Vendas por País")
vendas_pais = df.groupby("Country")["Amount"].sum().sort_values(ascending=False)

fig4, ax4 = plt.subplots(figsize=(10, 4))
sns.barplot(x=vendas_pais.values, y=vendas_pais.index, palette="Purples_d", ax=ax4)
ax4.set_xlabel("Valor Vendido ($)")
ax4.set_ylabel("País")
st.pyplot(fig4) 