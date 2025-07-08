import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import re
import requests
import urllib3
from utils.conversores import (
    gms_para_decimal_flex,
    coordenada_para_municipio,
    decimal_para_gms,
    xlsx_para_pdf,
    csv_para_pdf,
    csv_para_xlsx,
    calcular_distancia_km,
    rio_mais_proximo
)


st.set_page_config(page_title="Ferramentas de Coordenadas", layout="wide")
st.title("🧭 Ferramentas de Geolocalização")

aba = st.sidebar.selectbox("Escolha a ferramenta", [
    "Conversor GMS → Decimal",
    "Conversor Decimal → GMS",
    "Localizador de Município",
    "Conversores de Arquivo",
    "Distância entre Coordenadas",
    "Rio mais próximo"
])

if aba == "Conversor GMS → Decimal":
    st.subheader("📐 Conversor de coordenadas GMS para Decimal")
    entrada = st.text_input("Digite a coordenada (ex: 02°51'55\"N, 063°56'53\"W)")
    if entrada:
        try:
            lat, lon = gms_para_decimal_flex(entrada)
            st.success(f"Latitude: {lat}, Longitude: {lon}")
        except Exception as e:
            st.error(f"Erro: {str(e)}")

elif aba == "Localizador de Município":
    st.subheader("📍 Localizador de Município")
    entrada = st.text_input(
    "Digite a coordenada (ex: 02°51'55\"N, 063°56'53\"W ou 2.865278, -63.948056)")
    if entrada:
        try:
            resultado = coordenada_para_municipio(entrada)
            st.success(f"Resultado: {resultado}")
        except Exception as e:
            st.error(f"Erro: {str(e)}")

elif aba == "Conversor Decimal → GMS":
    st.subheader("🧮 Conversor de Decimal para GMS")
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude (ex: 2.713056)", format="%.6f")
    with col2:
        lon = st.number_input("Longitude (ex: -62.67)", format="%.6f")
    
    if st.button("Converter para GMS"):
        lat_gms, lon_gms = decimal_para_gms(lat, lon)
        st.success(f"{lat_gms}, {lon_gms}")

elif aba == "Conversores de Arquivo":
    st.subheader("📄 Conversores de Arquivo")

    tipo = st.radio("Escolha o tipo de conversão:", [
        "CSV → PDF",
        "CSV → XLSX",
        "XLSX → PDF"
    ])

    arquivo = st.file_uploader("Envie o arquivo correspondente")

    if arquivo:
        with st.spinner("Convertendo..."):
            if tipo == "CSV → PDF":
                caminho = f"temp_{arquivo.name}"
                with open(caminho, "wb") as f:
                    f.write(arquivo.getbuffer())
                pdf_path = csv_para_pdf(caminho)
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Baixar PDF", f, file_name=os.path.basename(pdf_path))
                os.remove(caminho)
                os.remove(pdf_path)

            elif tipo == "CSV → XLSX":
                caminho = f"temp_{arquivo.name}"
                with open(caminho, "wb") as f:
                    f.write(arquivo.getbuffer())
                xlsx_path = csv_para_xlsx(caminho)
                with open(xlsx_path, "rb") as f:
                    st.download_button("📥 Baixar XLSX", f, file_name=os.path.basename(xlsx_path))
                os.remove(caminho)
                os.remove(xlsx_path)

            elif tipo == "XLSX → PDF":
                caminho = f"temp_{arquivo.name}"
                with open(caminho, "wb") as f:
                    f.write(arquivo.getbuffer())
                pdf_path = xlsx_para_pdf(caminho)
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Baixar PDF", f, file_name=os.path.basename(pdf_path))
                os.remove(caminho)
                os.remove(pdf_path)

elif aba == "Distância entre Coordenadas":
    st.subheader("📏 Distância entre duas coordenadas")
    st.markdown("Você pode inserir coordenadas em formato GMS (ex: `02°51'55\"N`) ou decimal (ex: `2.865278`).")

    col1, col2 = st.columns(2)
    with col1:
        origem = st.text_input("Coordenada de Origem")
    with col2:
        destino = st.text_input("Coordenada de Destino")

    if origem and destino:
        try:
            # Tenta GMS → Decimal; se falhar, tenta converter direto
            try:
                lat1, lon1 = gms_para_decimal_flex(origem)
            except:
                lat1, lon1 = map(float, origem.replace(",", " ").split())

            try:
                lat2, lon2 = gms_para_decimal_flex(destino)
            except:
                lat2, lon2 = map(float, destino.replace(",", " ").split())

            distancia = calcular_distancia_km((lat1, lon1), (lat2, lon2))
            st.success(f"Distância: {distancia} km")
        except Exception as e:
            st.error(f"Erro: {str(e)}")

elif aba == "Rio mais próximo":
    st.subheader("🌊 Rio mais próximo de uma coordenada")
    entrada = st.text_input("Digite a coordenada (GMS ou decimal)")
    raio_km = st.slider("Raio de busca (km)", 1, 20, 5)

    if entrada:
        try:
            try:
                lat, lon = gms_para_decimal_flex(entrada)
            except:
                lat, lon = map(float, entrada.replace(",", " ").split())

            rio = rio_mais_proximo(lat, lon, raio_km=raio_km)
            st.success(f"Rio encontrado: {rio}")
        except Exception as e:
            st.error(f"Erro: {str(e)}")
