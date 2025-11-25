# ------------------------------
# Importações
# ------------------------------
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.parse

# ------------------------------
# Configuração da página
# ------------------------------
st.set_page_config(
    page_title="EFCA – Comportamento Alimentar",
    page_icon="🍽️",
    layout="wide",
    menu_items={
        "About": "App EFCA para avaliação do fenótipo de comportamento alimentar."
    }
)

# ------------------------------
# CSS personalizado
# ------------------------------
st.markdown("""
<style>
/* Fundo geral do aplicativo */
[data-testid="stAppViewContainer"] {
    background-color: #f1e3d8 !important;
}

/* Container principal */
[data-testid="stBlock"] > div {
    background-color: #f1e3d8 !important;
}

/* Container interno do Streamlit */
.block-container {
    background-color: #f1e3d8 !important;
    padding: 2rem 3rem;
    border-radius: 12px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #f1e3d8 !important;
}

/* Botões */
.stButton>button {
    background-color: #556b2f !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    font-size: 1rem !important;
}

/* Diminui espaço acima do título */
h1 {
    margin-top: 0.5rem;
}

/* Texto preto em todo o app */
body, .stApp, .block-container, h1, h2, h3, h4, h5, h6, p, label, .css-1kyxreq {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Banner com logo
# ------------------------------
banner_html = """
<div style="
    width: 100%;
    height: 260px;  
    position: relative;
    background-color: #f1e3d8;
">
    <img src="https://raw.githubusercontent.com/leticiabrantendocrinologia/efca-app/bf9fca05f3ee47c7425829cc2ebd26733e93b0d8/logo.png"
         style="
            position: absolute; 
            top: 45%; 
            left: 50%; 
            transform: translate(-50%, -45%);
            height: 220px;
        ">
</div>
"""
components.html(banner_html, height=260)

# ------------------------------
# Título, referência e crédito
# ------------------------------
st.title("Escala EFCA: Fenótipo de Comportamento Alimentar")

st.markdown("""
> **Questionário baseado em:**  
> Pineda-Wieselberg RJ, Soares AH, Napoli TF, Sarto MLL, Anger V, Formoso J, Scalissi NM, Salles JEN.  
> Validation for Brazilian Portuguese of the Eating Behavior Phenotypes Scale (EFCA): Confirmatory Factor Analysis and Psychometric Properties.  
> *Arch. Endocrinol. Metab.* 2025; ahead of print.
""")

st.markdown("""
<p><strong>Criado por:</strong> <a href="https://www.instagram.com/leticiaendocrino/" target="_blank">@leticiaendocrino</a></p>
""", unsafe_allow_html=True)

st.markdown("""
Bem-vindo! Este questionário avalia aspectos do seu comportamento alimentar segundo a EFCA.
Responda com sinceridade e clique em **Enviar** para ver seus resultados.
""")

# ------------------------------
# Perguntas por subescala
# ------------------------------
subscales = {
    "Comer Emocional": [
        "Acalmo as minhas emoções com comida.",
        "Tenho o hábito de petiscar (petiscar = fazer pequenas refeições entre as refeições principais - café da manhã, almoço, café da tarde e jantar - sem medir a quantidade do que se come).",
        "Faço lanches entre as refeições devido à ansiedade, tédio, solidão, medo, raiva, tristeza e/ou cansaço.",
        "Como nos momentos em que estou: entediado, ansioso, nervoso, triste, cansado, irritado e solitário."
    ],
    "Comer Hiperfágico": [
        "Eu como até ficar muito cheio.",
        "Peço mais comida quando termino meu prato.",
        "Costumo comer mais de um prato nas refeições principais."
    ],
    "Comer Desorganizado": [
        "Tomo café da manhã todos os dias.",
        "Pulo algumas - ou pelo menos uma - das refeições principais (café da manhã, almoço, café da tarde ou jantar).",
        "Passo mais de 5 horas por dia sem comer."
    ],
    "Comer Hedônico": [
        "Quando começo a comer algo que gosto muito, tenho dificuldade em parar.",
        "Sinto-me tentado a comer quando vejo/cheiro comida que gosto e/ou quando passo por um quiosque, uma padaria, uma pizzaria ou um estabelecimento de fast food.",
        "Quando me deparo com uma comida que gosto muito, mesmo sem sentir fome, acabo comendo.",
        "Quando como algo que gosto, finalizo toda a porção."
    ],
    "Comer Compulsivo": [
        "Como muita comida em pouco tempo.",
        "Quando como algo que gosto muito, como muito rápido."
    ]
}

questions = [q for sub in subscales.values() for q in sub]
options = ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]
score_map = {opt: i for i, opt in enumerate(options)}
responses = {}

# ------------------------------
# Formulário EFCA
# ------------------------------
with st.form("efca_form"):
    for q in questions:
        responses[q] = st.radio(q, options)
    submitted = st.form_submit_button("Enviar")

# ------------------------------
# Processamento de resultados
# ------------------------------
def interpret_score(score, max_score):
    pct = score / max_score
    if pct <= 0.33:
        return "Baixo"
    elif pct <= 0.66:
        return "Moderado"
    else:
        return "Alto"

if submitted:
    st.markdown("---")
    st.header("Resultado da EFCA")

    # Resultados por subescala
    subscale_results = {}
    for sub, qs in subscales.items():
        score = 0
        for q in qs:
            s = score_map[responses[q]]
            if q == "Tomo café da manhã todos os dias.":
                s = (len(options)-1) - s
            score += s
        max_subscore = len(qs) * (len(options)-1)
        interpretation = interpret_score(score, max_subscore)
        subscale_results[sub] = (score, interpretation)

    # Mostrar resultados
    st.markdown("**Resultados por subescala:**")
    for sub, (score, interp) in subscale_results.items():
        st.write(f"- {sub}: {score} pontos - {interp}")

    # ------------------------------
    # Salvar respostas em CSV
    # ------------------------------
    df = pd.DataFrame([{
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **responses
    }])
    try:
        old = pd.read_csv("efca_respostas.csv")
        new = pd.concat([old, df], ignore_index=True)
    except FileNotFoundError:
        new = df
    new.to_csv("efca_respostas.csv", index=False)

    # Botão CSV
    csv = new.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar resultado (CSV)",
        data=csv,
        file_name="resultado_efca.csv",
        mime="text/csv"
    )

    # ------------------------------
    # Gerar PDF
    # ------------------------------
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resultado da EFCA", ln=True, align='C')
    pdf.ln(10)
    for sub, (score, interp) in subscale_results.items():
        pdf.cell(200, 10, txt=f"{sub}: {score} pontos - {interp}", ln=True)

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="📥 Baixar resultado (PDF)",
        data=pdf_buffer,
        file_name="resultado_efca.pdf",
        mime="application/pdf"
    )

    # ------------------------------
    # Gerar PNG
    # ------------------------------
    img = Image.new('RGB', (600, 400), color=(241,227,216))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    y = 20
    d.text((20, y), "Resultado da EFCA", fill=(0,0,0))
    y += 30
    for sub, (score, interp) in subscale_results.items():
        d.text((20, y), f"{sub}: {score} pontos - {interp}", fill=(0,0,0))
        y += 25

    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    st.download_button(
        label="📥 Baixar resultado (PNG)",
        data=img_buffer,
        file_name="resultado_efca.png",
        mime="image/png"
    )

    # ------------------------------
    # Link para WhatsApp profissional
    # ------------------------------
    whatsapp_number = "5531996515760"
    message = "Aqui está meu resultado EFCA:\n" + "\n".join([f"{sub}: {score} pontos - {interp}" for sub, (score, interp) in subscale_results.items()])
    encoded_message = urllib.parse.quote(message)
    whatsapp_link = f"https://api.whatsapp.com/send?phone={whatsapp_number}&text={encoded_message}"

    st.markdown(f"[📩 Enviar resultado pelo WhatsApp]({whatsapp_link})", unsafe_allow_html=True)

    # ------------------------------
    # Botão para refazer
    # ------------------------------
    if st.button("Refazer o formulário"):
        st.experimental_rerun()
