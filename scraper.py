import yt_dlp
import os
from tqdm import tqdm

def obtener_videos_filtrados(url_perfil):
    """
    Escanea un perfil de TikTok, filtra videos por duración (60-90s)
    y muestra una barra de progreso en la terminal.
    """
    videos_validos = []
    
    # Configuración optimizada para evitar bloqueos y limpiar la pantalla
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
        'no_warnings': True,  # ❌ Adiós a los mensajes amarillos de impersonation
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'nocheckcertificate': True,
    }

    print(f"\n📡 [IMPERIO MP] Conectando con: {url_perfil}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # 1. Obtener la lista rápida de videos del perfil
            perfil_info = ydl.extract_info(url_perfil, download=False)
            
            if not perfil_info or 'entries' not in perfil_info:
                print("⚠️ No se pudieron encontrar videos en este perfil.")
                return []

            lista_videos = list(perfil_info['entries'])
            total = len(lista_videos)
            print(f"📦 Se detectaron {total} videos. Iniciando filtrado inteligente...")

            # 2. Procesar cada video con barra de progreso
            # 'colour="cyan"' le da el toque hacker/futurista
            for entry in tqdm(lista_videos, desc="🔍 Analizando Mally Content", unit="vids", colour="cyan"):
                url_video = entry.get('url') or entry.get('webpage_url')
                
                if not url_video:
                    continue

                try:
                    # Extraer info individual para ver la duración real
                    # Usamos process=True para obtener metadatos específicos
                    v_info = ydl.extract_info(url_video, download=False)
                    duracion = v_info.get('duration', 0)

                    # --- EL FILTRO MALLY (60 a 90 segundos) ---
                    if 60 <= duracion <= 90:
                        videos_validos.append({
                            'id': v_info.get('id'),
                            'url': v_info.get('webpage_url'),
                            'title': v_info.get('title', 'Sin título')
                        })
                except Exception:
                    # Si un video falla (borrado, privado, etc.), saltamos al siguiente
                    continue

            print(f"\n✅ Análisis terminado. {len(videos_validos)} videos listos para enviar.")

        except Exception as e:
            print(f"❌ Error crítico en Scraper: {e}")

    return videos_validos
