import telebot
import yt_dlp
import os
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

def descargar_y_enviar(video_url, chat_id):
    filename = "temp_video.mp4"
    ydl_opts = {'outtmpl': filename, 'quiet': True}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    with open(filename, 'rb') as video:
        bot.send_video(chat_id, video, caption="🔥 Nuevo contenido Mally Shared")
    
    os.remove(filename) # Limpieza para no llenar memoria
