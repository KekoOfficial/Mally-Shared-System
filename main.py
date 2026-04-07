import time
import json
import os
from scraper import obtener_videos_filtrados
from telegram_bot import descargar_y_enviar
from config import PERFILES_TIKTOK, CANAL_DESTINO

# Nombre del archivo donde guardamos los IDs para no repetir videos
DB_FILE = "database.json"

def cargar_db():
    """Carga la lista de videos ya enviados desde el archivo JSON."""
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return []

def guardar_db(data):
    """Guarda la lista actualizada de IDs en el archivo JSON."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def run_system():
    """Ejecuta el ciclo principal del sistema Mally Shared."""
    print("--- 👑 IMPERIO MP: MALLY SHARED SYSTEM ACTIVADO ---")
    
    # Cargamos los videos que ya se enviaron antes
    enviados = cargar_db()
    print(f"📦 Historial cargado: {len(enviados)} videos registrados.")

    while True:
        for perfil in PERFILES_TIKTOK:
            print(f"🔍 Escaneando perfil: {perfil}")
            
            # Obtenemos solo los videos que duran entre 60 y 90 segundos
            videos = obtener_videos_filtrados(perfil)
            
            for v in videos:
                video_id = v['id']
                
                if video_id not in enviados:
                    print(f"✨ ¡Nuevo video detectado! ID: {video_id}")
                    print(f"⏳ Duración válida. Procesando envío a Telegram...")
                    
                    try:
                        # Descarga y envía al canal configurado
                        descargar_y_enviar(v['url'], CANAL_DESTINO)
                        
                        # Guardamos en la base de datos para no repetir
                        enviados.append(video_id)
                        guardar_db(enviados)
                        
                        print(f"✅ Enviado con éxito: {v['title'][:30]}...")
                        
                        # Pausa de seguridad para evitar bloqueos de Telegram
                        time.sleep(15) 
                    except Exception as e:
                        print(f"❌ Error al procesar video {video_id}: {e}")
                else:
                    # Opcional: print(f"⏭️ Video {video_id} ya fue enviado. Saltando...")
                    pass
        
        print(f"💤 Ronda terminada. Esperando 1 hora para la siguiente revisión...")
        time.sleep(3600) # 3600 segundos = 1 hora

if __name__ == "__main__":
    try:
        run_system()
    except KeyboardInterrupt:
        print("\n🛑 Sistema detenido manualmente.")
