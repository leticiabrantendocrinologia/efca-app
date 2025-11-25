import streamlit as st

st.title("EFCA – Escala de Fenótipo de Comportamento Alimentar")

q1 = st.radio("Eu como rápido:", ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"])
q2 = st.radio("Eu como sem fome:", ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"])

if st.button("Enviar"):
    st.success("Respostas registradas!")
    st.write("Suas respostas:")
    st.write({"Comer rápido": q1, "Comer sem fome": q2})
