import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="EFCA – Escala de Fenótipo de Comportamento Alimentar")

st.title("🧠 EFCA – Escala de Fenótipo de Comportamento Alimentar")
st.write("Responda todas as perguntas abaixo usando a escala de frequência.")

# -------------------------
# LISTA DE PERGUNTAS OFICIAIS (18 itens)
# -------------------------

questions = {
    "Eu como rápido.": [],
    "Eu como até me sentir desconfortável.": [],
    "Eu como mesmo quando não estou com fome.": [],
    "Eu sinto que perco o controle quando começo a comer.": [],
    "Belisco comida ao longo do dia.": [],
    "Eu como escondido.": [],
    "Eu sinto fome intensa súbita.": [],
    "Tenho dificuldade de parar de comer alimentos palatáveis.": [],
    "Como para lidar com emoções negativas.": [],
    "Tenho vontade incontrolável de comer certos alimentos.": [],
    "Sinto que preciso comer para me acalmar.": [],
    "Quando começo a comer, exagero sem perceber.": [],
    "Eu como por tédio.": [],
    "Como mais quando estou estressado(a).": [],
    "Fico pensando em comida mesmo após já ter comido.": [],
    "Busco comida mesmo sem necessidade fisiológica.": [],
    "Fico ansiando por comida durante o dia.": [],
    "Sinto culpa depois de comer em excesso.": [],
}

options = ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]

score_map = {
    "Nunca": 0,
    "Raramente": 1,
    "Às vezes": 2,
    "Frequentemente": 3,
    "Sempre": 4
}

responses = {}

# -------------------------
# FORMULÁRIO DO QUESTIONÁRIO
# -------------------------

with st.form("efca_form"):
    st.subheader("📝 Responda às 18 perguntas abaixo:")

    for q in questions:
        responses[q] = st.radio(q, options)

    submitted = st.form_submit_button("Enviar Respostas")

# -------------------------
# PROCESSAMENTO DA PONTUAÇÃO
# -------------------------

if submitted:
    st.success("Respostas enviadas com sucesso!")

    # calcular pontuação total
    total_score = sum([score_map[resp] for resp in responses.values()])

    st.subheader(f"🎯 Pontuação Total: **{total_score} / 72**")

    # interpretação
    if total_score <= 18:
        st.info("🟢 Baixo fenótipo de comportamento alimentar disfuncional.")
    elif total_score <= 36:
        st.warning("🟡 Médio fenótipo alterado.")
    else:
        st.error("🔴 Alto fenótipo de comportamento alimentar disfuncional.")

    # mostrar respostas
    st.subheader("📄 Suas respostas:")
    st.write(responses)

    # salvar em CSV (no Streamlit Cloud)
    df = pd.DataFrame([{
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "pontuacao_total": total_score,
        **responses
    }])

    try:
        old = pd.read_csv("efca_respostas.csv")
        new = pd.concat([old, df], ignore_index=True)
    except:
        new = df

    new.to_csv("efca_respostas.csv", index=False)

    st.success("As respostas foram salvas com sucesso!")

