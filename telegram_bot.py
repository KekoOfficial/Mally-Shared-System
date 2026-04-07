import telebot
import yt_dlp
import os
from datetime import datetime
from config import TOKEN

# Inicializamos el bot de IMPERIO MP
bot = telebot.TeleBot(TOKEN)

def descargar_y_enviar(video_url, chat_id):
    """
    Descarga el video de TikTok y lo envía al canal con el formato:
    Vídeo: [Título]
    Fecha: [Fecha de subida]
    Creador: Khassamx.//Dev
    Mally
    """
    archivo_temp = "mally_video.mp4"
    
    # Opciones de descarga para yt-dlp
    ydl_opts = {
        'outtmpl': archivo_temp,
        'quiet': True,
        'no_warnings': True,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraemos la información completa antes de enviar
            info = ydl.extract_info(video_url, download=True)
            
            titulo = info.get('title', 'Contenido Mally')
            
            # Formatear la fecha de subida (TikTok entrega YYYYMMDD)
            upload_date = info.get('upload_date')
            if upload_date:
                try:
                    fecha_obj = datetime.strptime(upload_date, '%Y%m%d')
                    fecha_final = fecha_obj.strftime('%d/%m/%Y')
                except:
                    fecha_final = "Reciente"
            else:
                fecha_final = "No disponible"

        # --- DISEÑO DEL MENSAJE (ESTILO KHASSAM) ---
        mensaje_caption = (
            f"🎬 *Vídeo:*\n"
            f"{titulo}\n\n"
            f"📅 *Fecha:* {fecha_final}\n"
            f"👤 *Creador:* Khassamx.//Dev\n"
            f"👑 *Mally*"
        )

        # Enviamos el video al canal
        with open(archivo_temp, 'rb') as video_file:
            bot.send_video(
                chat_id, 
                video_file, 
                caption=mensaje_caption, 
                parse_mode='Markdown'
            )
        
        # Limpieza de archivos en Termux para no saturar memoria
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)
            
    except Exception as e:
        print(f"❌ Error en el módulo de Telegram: {e}")
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)

if __name__ == "__main__":
    print("Módulo de Telegram cargado correctamente.")
