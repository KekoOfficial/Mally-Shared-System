import yt_dlp

def obtener_videos_filtrados(url_perfil):
    videos_validos = []
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url_perfil, download=False)
            for entry in info.get('entries', []):
                # Obtener info detallada de cada video
                v_info = ydl.extract_info(entry['url'], download=False)
                duracion = v_info.get('duration', 0)

                if 60 <= duracion <= 90:
                    videos_validos.append({
                        'id': v_info.get('id'),
                        'url': v_info.get('webpage_url'),
                        'title': v_info.get('title')
                    })
        except Exception as e:
            print(f"Error en scraper: {e}")
    
    return videos_validos
