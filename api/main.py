from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

API_KEY = os.getenv("rnd_PoA2HiwFWAHLRmMPhKO9XGLnI2e0")  # Clave de API de Render
SERVICE_ID = os.getenv("srv-crnl62e8ii6s73et86n0")  # ID de tu servicio

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.get("/")
def read_root():
    return {"message": "API de Control de Bot"}

@app.get("/status")
def get_service_status():
    """Verificar el estado del servicio."""
    response = requests.get(f"https://api.render.com/v1/services/{SERVICE_ID}", headers=HEADERS)
    if response.status_code == 200:
        service_info = response.json()
        return {"status": service_info.get("status")}
    else:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener el estado del servicio")

@app.post("/restart")
def restart_service():
    """Reiniciar el servicio si está apagado."""
    response = requests.post(f"https://api.render.com/v1/services/{SERVICE_ID}/restart", headers=HEADERS)
    if response.status_code == 202:
        return {"message": "Servicio reiniciado correctamente"}
    else:
        raise HTTPException(status_code=response.status_code, detail="Error al reiniciar el servicio")
