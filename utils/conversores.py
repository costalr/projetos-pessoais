import re
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from fpdf import FPDF
import os
import pandas as pd


def gms_para_decimal_flex(coord_str):
    coord_str = coord_str.replace("º", "°").replace("′", "'").replace("’", "'").replace("″", '"').replace(",", " ").strip()
    match = re.findall(r'([NSWE])?\s*(\d{1,3})°(\d{1,2})[\'’](\d{1,2}(?:\.\d+)?)[″"]?\s*([NSWE])?', coord_str, re.IGNORECASE)
    if len(match) < 2:
        raise ValueError("Formato inválido. Ex: 2°42'47.00\"N, 62°40'12.00\"W")
    resultado = []
    for grupo in match:
        dir1, graus, minutos, segundos, dir2 = grupo
        direcao = dir1 or dir2
        decimal = int(graus) + int(minutos)/60 + float(segundos)/3600
        if direcao.upper() in ['S', 'W']:
            decimal *= -1
        resultado.append(round(decimal, 6))
    return resultado

def decimal_para_gms(lat, lon):
    def converter(valor, direcao_positiva, direcao_negativa):
        direcao = direcao_positiva if valor >= 0 else direcao_negativa
        valor = abs(valor)
        graus = int(valor)
        minutos_float = (valor - graus) * 60
        minutos = int(minutos_float)
        segundos = round((minutos_float - minutos) * 60, 2)
        return f"{graus}°{minutos}'{segundos}\"{direcao}"
    
    lat_str = converter(lat, "N", "S")
    lon_str = converter(lon, "E", "W")
    return lat_str, lon_str


def coordenada_para_municipio(coord_str):
    try:
        # Primeiro tenta converter GMS → decimal
        lat, lon = gms_para_decimal_flex(coord_str)
    except:
        # Se falhar, tenta decimal direto
        try:
            partes = re.split(r"[,\s]+", coord_str.strip())
            lat = float(partes[0])
            lon = float(partes[1])
        except:
            raise ValueError("Formato inválido. Use GMS (02°51'55\"N, 063°56'53\"W) ou decimal (2.865278, -63.948056).")

    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": lat, "lon": lon, "format": "json", "zoom": 10, "addressdetails": 1}
    headers = {"User-Agent": "consulta-subpolo-funai"}
    response = requests.get(url, params=params, headers=headers, verify=False)
    data = response.json()
    if 'address' in data:
        addr = data['address']
        municipio = addr.get('municipality') or addr.get('town') or addr.get('city') or addr.get('county')
        estado = addr.get('state')
        return f"{municipio} - {estado}" if municipio else "Sem município definido"
    else:
        return "Município não encontrado"

def csv_para_pdf(csv_file_path, output_path=None):
    df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
    pdf_file = output_path or os.path.splitext(csv_file_path)[0] + '.pdf'

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Dados Convertidos de CSV para PDF", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    
    col_widths = [40] * len(df.columns)
    row_height = pdf.font_size * 1.5

    for col in df.columns:
        pdf.cell(col_widths[df.columns.get_loc(col)], row_height, str(col), border=1, align='C')
    pdf.ln(row_height)

    for row in df.itertuples(index=False):
        for idx, cell in enumerate(row):
            pdf.cell(col_widths[idx], row_height, str(cell), border=1, align='C')
        pdf.ln(row_height)

    pdf.output(pdf_file)
    return pdf_file

def csv_para_xlsx(csv_file_path, output_path=None):
    df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
    xlsx_file = output_path or os.path.splitext(csv_file_path)[0] + '.xlsx'
    df.to_excel(xlsx_file, index=False)
    return xlsx_file

def xlsx_para_pdf(xlsx_file_path, output_path=None):
    df = pd.read_excel(xlsx_file_path)
    pdf_file = output_path or os.path.splitext(xlsx_file_path)[0] + '.pdf'

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Dados Convertidos de XLSX para PDF", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    
    col_widths = [40] * len(df.columns)
    row_height = pdf.font_size * 1.5

    for col in df.columns:
        pdf.cell(col_widths[df.columns.get_loc(col)], row_height, str(col), border=1, align='C')
    pdf.ln(row_height)

    for row in df.itertuples(index=False):
        for idx, cell in enumerate(row):
            pdf.cell(col_widths[idx], row_height, str(cell), border=1, align='C')
        pdf.ln(row_height)

    pdf.output(pdf_file)
    return pdf_file

from math import radians, sin, cos, sqrt, atan2

def calcular_distancia_km(coord1, coord2):
    """
    Recebe duas coordenadas no formato decimal:
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    Retorna a distância em quilômetros.
    """
    R = 6371  

    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distancia = R * c
    return round(distancia, 2)

import requests
def rio_mais_proximo(lat, lon, raio_km=5):
    raio_metros = raio_km * 1000
    overpass_url = "https://overpass.kumi.systems/api/interpreter"

    query = f"""
    [out:json];
    (
      way(around:{raio_metros},{lat},{lon})["waterway"="river"];
      relation(around:{raio_metros},{lat},{lon})["waterway"="river"];
    );
    out tags center;
    """

    try:
        response = requests.post(
            overpass_url,
            data={"data": query},
            headers={"User-Agent": "ferramenta-funai"},
            verify=False  # funciona na sua rede
        )
        response.raise_for_status()
        data = response.json()

        elementos = data.get("elements", [])
        for elem in elementos:
            nome = elem.get("tags", {}).get("name")
            if nome:
                return nome

        return "Nenhum rio com nome encontrado no raio especificado"

    except Exception as e:
        raise Exception(f"Erro na consulta Overpass: {e}")
