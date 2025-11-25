import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# ---------------- Página ----------------
st.set_page_config(
    page_title="EFCA – Comportamento Alimentar",
    page_icon="🍽️",
    layout="wide",
    menu_items={
        "About": "App EFCA para avaliação do fenótipo de comportamento alimentar."
    }
)

# ---------------- Banner com logo ----------------
banner_html = """
<div style="
    width: 100%;
    height: 300px;  /* altura do topo */
    position: relative;
    background-color: #f1e3d8;  /* mesmo fundo da logo */
">
    <img src="https://raw.githubusercontent.com/leticiabrantendocrinologia/efca-app/bf9fca05f3ee47c7425829cc2ebd26733e93b0d8/logo.png"
         style="position: absolute; top:
