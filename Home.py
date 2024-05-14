import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import time
warnings.filterwarnings('ignore')
def delete_element(n):
    i.empty()
    st.session_state.elements.pop(n)
    st.session_state.palabras.pop(n)

def generate(i, n):
    i = st.container(border=True)
    i.write(st.session_state.palabras[n])
    i.button("X", key=f"{n}_delete", on_click=delete_element, args=[n])
        
st.set_page_config(page_title="Client_Name",page_icon=":bar_chart",layout="wide")
if "palabras" not in st.session_state:
    st.session_state.palabras = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"]
if "elements" not in st.session_state:
    st.session_state.elements = []

st.write("___INITIAL EXECUTION___")
st.write(st.session_state)
st.title("Hello!")
if len(st.session_state.elements) > 0:
    """entra"""
    for n, i in enumerate(st.session_state.elements):
        generate(i, n)
        #st.session_state.elements.pop(n)
st.button(
    "Add a column"
    , on_click=lambda _:_.append(st.empty())
    , args=[st.session_state.elements]
)
st.write("___FINAL EXECUTION___")
st.write(st.session_state)