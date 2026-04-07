import time
import json
from scraper import obtener_videos_filtrados
from telegram_bot import descargar_y_enviar
from config import PERFILES_TIKTOK, CANAL_DESTINO

DB_FILE = "database.json"

def cargar_db():
    if not os.path.exists(DB_FILE): return []
    with open(DB_FILE, "r") as f: return json.load(f)

def guardar_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

def run_system():
    enviados = cargar_db()
    print("🚀 Sistema Mally Shared Iniciado...")

    while True:
        for perfil in PERFILES_TIKTOK:
            print(f"Buscando en: {perfil}")
            videos = obtener_videos_filtrados(perfil)
            
            for v in videos:
                if v['id'] not in enviados:
                    print(f"✅ Nuevo video detectado: {v['id']}")
                    descargar_y_enviar(v['url'], CANAL_DESTINO)
                    enviados.append(v['id'])
                    guardar_db(enviados)
                    time.sleep(10) # Evitar spam
        
        print("💤 Esperando nueva ronda...")
        time.sleep(3600) # Revisa cada hora

if __name__ == "__main__":
    run_system()
