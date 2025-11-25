import streamlit as st

# =========================================================
# CSS COMPLETO — Botão “Ver Resultado” corrigido DEFINITIVAMENTE
# =========================================================
st.markdown("""
<style>

/* ===== Reset global para todos os botões ===== */
button, .stButton button, div.stButton > button, button[kind="primary"] {
    -webkit-appearance: none !important;
    appearance: none !important;
}

/* ===== Estilo global dos botões ===== */
.stButton button,
div.stButton > button,
button[kind="primary"] {
    background-color: #b3b795 !important;
    color: black !important;
    border-radius: 10px !important;
    border: 2px solid #7d816e !important;
    padding: 10px 20px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    width: 100% !important;
    height: auto !important;

    /* força override absoluto para iOS */
    box-shadow: none !important;
    text-shadow: none !important;
}

/* ===== HOVER ===== */
.stButton button:hover,
div.stButton > button:hover,
button[kind="primary"]:hover {
    background-color: #a4a986 !important;
    color: black !important;
}

/* ===== Botões específicos de WhatsApp e Refazer ===== */
.whatsapp-btn {
    background-color: #c8d2b0 !important;
    border: 2px solid #7d816e !important;
    color: #1a1a1a !important;
    border-radius: 15px !important;
    padding: 12px !important;
    font-size: 20px !important;
}

.refazer-btn {
    background-color: #b3c29f !important;
    border: 2px solid #7d816e !important;
    color: #1a1a1a !important;
    border-radius: 15px !important;
    padding: 12px !important;
    font-size: 20px !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# EXEMPLO DE USO — BOTÃO “VER RESULTADO”
# =========================================================

st.write("### Questionário exemplo")
responder = st.button("Ver Resultado")

if responder:
    st.header("Resultado da EFCA")

    st.write("""
    - Comer Emocional: 0 — Baixo  
    - Comer Hiperfágico: 0 — Baixo  
    - Comer Desorganizado: 4 — Moderado  
    - Comer Hedônico: 0 — Baixo  
    - Comer Compulsivo: 0 — Baixo  
    """)

    st.markdown('<button class="whatsapp-btn">📩 Enviar resultado pelo WhatsApp</button>',
                unsafe_allow_html=True)

    st.markdown('<button class="refazer-btn">🔄 Refazer o formulário</button>',
                unsafe_allow_html=True)
