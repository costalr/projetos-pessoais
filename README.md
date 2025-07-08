# 🧭 Caixa de Ferramentas - Geolocalização e Conversão de Dados

Este é um projeto desenvolvido para automatizar tarefas diárias relacionadas à geolocalização, conversão de coordenadas e manipulação de arquivos. Criado inicialmente para auxiliar nas rotinas de trabalho com dados da Terra Indígena Yanomami, este painel interativo visa facilitar o acesso a ferramentas úteis com uma interface simples, acessível via web.

---

## 🚀 Funcionalidades

### 🛰️ Geolocalização
- Conversão de coordenadas GMS (graus, minutos, segundos) para Decimal
- Conversão de Decimal para GMS
- Localizador de município via coordenadas (usando API do Nominatim/OpenStreetMap)
- Distância entre duas coordenadas (com suporte a GMS e decimal)
- Identificação do rio mais próximo via Overpass API (OpenStreetMap)

### 📂 Conversores de Arquivo
- CSV → PDF
- CSV → XLSX
- XLSX → PDF

---

## 🛠️ Tecnologias utilizadas

- [Streamlit](https://streamlit.io/) – Interface web leve e interativa
- `pandas` – Manipulação de dados
- `fpdf` – Geração de arquivos PDF
- `openpyxl` – Manipulação de arquivos Excel
- `requests` – Requisições HTTP para APIs externas
- `Overpass API` e `Nominatim` – Fontes de dados geográficos baseadas no OpenStreetMap

---

## 🧰 Como rodar localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. Crie e ative um ambiente virtual:
    ```python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

3. Instalar as dependências:
    ``` pip install -r requirements.txt

4. Rodar a aplicação:
    ```streamlit run app.py
