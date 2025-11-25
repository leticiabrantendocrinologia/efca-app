import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Banner com fundo da mesma cor da logo
banner_html = """
<div style="
    width: 100%;
    height: 300px;  /* altura do topo */
    position: relative;
    background-color: #f1e3d8;  /* mesmo fundo da logo */
">
    <img src="https://raw.githubusercontent.com/leticiabrantendocrinologia/efca-app/bf9fca05f3ee47c7425829cc2ebd26733e93b0d8/logo.png"
         style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                height: 250px;">
</div>
"""  # <-- fechou corretamente a string

components.html(banner_html, height=300)
