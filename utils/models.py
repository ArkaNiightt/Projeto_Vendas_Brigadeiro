from langchain_openai import ChatOpenAI
import streamlit as st

MODELO_DEFAULT = "o1-mini"

MODEL_OPTIONS = [
    "o1-mini",
    "gpt-4o-2024-11-20",
    "gpt-4o-mini",
    "gpt-3.5-turbo",
    "gpt-4o",
]


def getModel(model, temperature=1):
    if model in MODEL_OPTIONS:
        return ChatOpenAI(
            model=model,
            api_key=st.secrets["OPENAI_API_KEY"],
            temperature=temperature
        )