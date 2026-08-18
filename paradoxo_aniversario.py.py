import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Paradoxo do Aniversário", layout="wide")

st.header("Probabilidade Complementar: O Paradoxo do Aniversário")

st.sidebar.subheader("Parâmetros da Simulação")
tamanho_grupo = st.sidebar.slider("Pessoas na Sala (N)", 2, 100, 23)
num_simulacoes = st.sidebar.slider(
    "Número de Salas Simuladas", 100, 10000, 2000, step=100
)
seed = st.sidebar.number_input("Semente Aleatória (Seed)", value=42, step=1)

np.random.seed(int(seed))

# 1. Simulação de Monte Carlo
# Matriz (num_simulacoes, tamanho_grupo) com dias do ano (1 a 365)
datas = np.random.randint(1, 366, size=(num_simulacoes, tamanho_grupo))


def tem_duplicata(linha):
    return len(linha) != len(np.unique(linha))


duplicatas = np.apply_along_axis(tem_duplicata, 1, datas)
prob_empirica = np.mean(duplicatas) * 100

# 2. Cálculo Teórico para N de 1 a 100
n_valores = np.arange(1, 101)
prob_teorica = []

for n in n_valores:
    # P(todos com aniversários diferentes)
    p_diferentes = np.prod([(365 - i) / 365 for i in range(n)])
    p_compartilhado = (1 - p_diferentes) * 100
    prob_teorica.append(p_compartilhado)

prob_teorica_atual = prob_teorica[tamanho_grupo - 1]

# 3. Gráfico Plotly
fig = go.Figure()

# Curva teórica
fig.add_trace(
    go.Scatter(
        x=n_valores,
        y=prob_teorica,
        mode="lines",
        name="Probabilidade Teórica",
        line=dict(color="royalblue", width=3),
    )
)

# Ponto atual da simulação amostral
fig.add_trace(
    go.Scatter(
        x=[tamanho_grupo],
        y=[prob_empirica],
        mode="markers",
        name=f"Simulação (N={tamanho_grupo})",
        marker=dict(color="red", size=12, symbol="diamond"),
    )
)

# Linha de corte de 50%
fig.add_hline(
    y=50,
    line_dash="dash",
    line_color="green",
    annotation_text="Ponto Crítico (50%)",
    annotation_position="bottom right",
)

fig.update_layout(
    height=500,
    title="Probabilidade de Pelo Menos Duas Pessoas Compartilharem o Aniversário",
    xaxis_title="Tamanho do Grupo (Pessoas na Sala)",
    yaxis_title="Probabilidade (%)",
    yaxis=dict(range=[0, 105]),
    hovermode="x unified",
)

col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("Pessoas no Grupo", f"{tamanho_grupo}")
    st.metric("Resultado Empírico", f"{prob_empirica:.2f}%")
    st.metric("Probabilidade Teórica", f"{prob_teorica_atual:.2f}%")

    st.write("**O Princípio do Evento Complementar:**")
    st.write(
        "Calcular diretamente a chance de coincidências é complexo. Em vez disso, calcula-se a chance de **ninguém** fazer aniversário no mesmo dia:"
    )
    st.latex(
        r"P(\text{Pelo menos 1 par}) = 1 - P(\text{Todos diferentes})"
    )
    st.latex(
        r"P(\text{Diferentes}) = \frac{365}{365} \times \frac{364}{365} \times \dots \times \frac{365-N+1}{365}"
    )
    st.info(
        "Em uma sala com apenas **23 pessoas**, existem $\\binom{23}{2} = 253$ pares de comparação possíveis, fazendo a probabilidade ultrapassar os **50%**!"
    )