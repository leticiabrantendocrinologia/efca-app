import streamlit as st

# =========================================================
# CONFIGURAÇÕES INICIAIS DO APP
# =========================================================
st.set_page_config(
    page_title="EFCA - Avaliação",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Avaliação EFCA – Escala de Fome, Compulsão e Apetite")

st.write("""
Responda às perguntas abaixo e ao final clique em **VER RESULTADO**.
""")


# =========================================================
# CSS COMPLETO — Inclua exatamente aqui
# =========================================================
st.markdown("""
<style>

/* Remove estilo nativo dos botões do iOS/Android */
button, .stButton button, div.stButton > button, button[kind="primary"] {
    -webkit-appearance: none !important;
    appearance: none !important;
}

/* Botão padrão (inclui “Ver Resultado”) */
.stButton button,
div.stButton > button,
button[kind="primary"] {
    background-color: #b3b795 !important;
    color: black !important;
    border-radius: 10px !important;
    border: 2px solid #7d816e !important;
    padding: 12px 20px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    width: 100% !important;
    text-shadow: none !important;
    box-shadow: none !important;
}

/* Hover */
.stButton button:hover,
div.stButton > button:hover,
button[kind="primary"]:hover {
    background-color: #a4a986 !important;
    color: black !important;
}

/* Botões especiais */
.whatsapp-btn {
    background-color: #c8d2b0 !important;
    border: 2px solid #7d816e !important;
    color: #1a1a1a !important;
    border-radius: 15px !important;
    padding: 12px !important;
    font-size: 20px !important;
    width: 100% !important;
    display: block;
    text-align: center;
}

.refazer-btn {
    background-color: #b3c29f !important;
    border: 2px solid #7d816e !important;
    color: #1a1a1a !important;
    border-radius: 15px !important;
    padding: 12px !important;
    font-size: 20px !important;
    width: 100% !important;
    display: block;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)



# =========================================================
# QUESTIONÁRIO EFCA
# =========================================================

st.subheader("Responda às perguntas")

opcoes = ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]
valores = {"Nunca": 0, "Raramente": 1, "Às vezes": 2, "Frequentemente": 3, "Sempre": 4}

# 5 domínios com perguntas de exemplo
perguntas = {
    "Comer Emocional": [
        "Eu como mais quando estou ansioso(a).",
        "Eu como para lidar com tristeza."
    ],
    "Comer Hiperfágico": [
        "Eu como grandes quantidades rapidamente.",
        "Tenho episódios de perda de controle alimentar."
    ],
    "Comer Desorganizado": [
        "Pulo refeições com frequência.",
        "Minha rotina alimentar é irregular."
    ],
    "Comer Hedônico": [
        "Eu busco comida pelo prazer mesmo sem fome.",
        "Eu penso em comida saborosa mesmo após comer."
    ],
    "Comer Compulsivo": [
        "Sinto urgência em comer que não consigo controlar.",
        "Sinto necessidade de comer escondido(a)."
    ]
}

respostas = {}

for dominio, itens in perguntas.items():
    st.markdown(f"### **{dominio}**")
    for i, item in enumerate(itens):
        chave = f"{dominio}_{i}"
        respostas[chave] = st.selectbox(item, opcoes, key=chave)


# =========================================================
# BOTÃO PARA CALCULAR RESULTADO
# =========================================================

if st.button("Ver Resultado"):
    st.header("📊 Resultado da EFCA")

    # Somatório por domínio
    resultados = {}

    for dominio, itens in perguntas.items():
        soma = sum(valores[respostas[f"{dominio}_{i}"]] for i in range(len(itens)))
        resultados[dominio] = soma

    # Exibição
    for dominio, score in resultados.items():
        if score <= 2:
            nivel = "Baixo"
        elif score <= 5:
            nivel = "Moderado"
        else:
            nivel = "Alto"

        st.write(f"**{dominio}: {score} — {nivel}**")

    st.divider()

    # Botão WhatsApp
    st.markdown(
        '<a href="https://wa.me/55" class="whatsapp-btn">📩 Enviar resultado pelo WhatsApp</a>',
        unsafe_allow_html=True
    )

    # Botão Refazer
    st.markdown(
        '<a href="/" class="refazer-btn">🔄 Refazer o formulário</a>',
        unsafe_allow_html=True
    )
