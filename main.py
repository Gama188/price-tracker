import requests
from bs4 import BeautifulSoup
import time
import os

URL = "https://www.prodynamics.com.mx/llanta-275-65-r17-zmax-terra-xplorer-c2-a-t-115t/p"
WEBHOOK = "https://discord.com/api/webhooks/1497697075587055899/Qt0EAs7vcEpLaXqHYHZE3ps67fLGNB31lq80RXF1tDw_xvA2AJP6vQxjJFdidVjakipp"

def limpiar_precio(texto):
    return float(texto.replace("$", "").replace(",", "").strip())

def obtener_precio():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        r = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        precio = soup.select_one(".price")

        if precio:
            return limpiar_precio(precio.text)
        else:
            return None

    except Exception as e:
        print("Error:", e)
        return None

def enviar_alerta(mensaje):
    try:
        requests.post(WEBHOOK, json={"content": mensaje})
    except Exception as e:
        print("Error webhook:", e)

def leer_precio():
    if not os.path.exists("precio.txt"):
        return None
    with open("precio.txt") as f:
        return float(f.read())

def guardar_precio(precio):
    with open("precio.txt", "w") as f:
        f.write(str(precio))

print("🚀 Iniciado")

while True:
    print("🔍 Revisando...")

    precio_actual = obtener_precio()

    if precio_actual:
        print("💰 Precio:", precio_actual)

        precio_anterior = leer_precio()

        if precio_anterior:
            if precio_actual < precio_anterior:
                enviar_alerta(f"🔥 Bajó el precio: ${precio_actual}")

        guardar_precio(precio_actual)

    else:
        print("⚠️ No se pudo obtener precio")

    time.sleep(600)
