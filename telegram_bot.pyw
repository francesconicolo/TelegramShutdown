from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import os
import requests
from datetime import datetime
import cv2
import const

TOKEN = const.TOKEN
ACC_ID = const.ACC_ID

def help(update,context):
   update.message.reply_text("Ecco una lista dei comandi disponibili \n /start \n /spegni \n /foto \n /help")
   

def start(update, context):
   update.message.reply_text("Sono attivo")
   
def foto(update,context):
   user = update.message.from_user
   if (ACC_ID == str(user['id'])):
      cap = cv2.VideoCapture(1) 
      ret,frame = cap.read() 
      cv2.imshow('img1',frame)   
      cv2.imwrite('./temp.png',frame)
      update.message.reply_text("Foto in arrivo...")
      update.message.reply_photo(photo=open('./temp.png', 'rb'))
      cap.release()
   else:
      update.message.reply_text("Non sei autorizzato!")

def spegni(update, context):
   update.message.reply_text("Il tuo computer sta per essere spento...")
   user = update.message.from_user
   if (ACC_ID == str(user['id'])):
      os.system('shutdown /s')   



def main():
   x = requests.get('https://api.telegram.org/bot'+TOKEN+'/deleteWebhook', params={'drop_pending_updates': 'True'})
   #  print(x.status_code)
   
   now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
   msg = "["+now+"]: È stato effettuato l'accesso su Francesco-PC" 
   requests.get('https://api.telegram.org/bot'+TOKEN+'/sendMessage?chat_id='+ACC_ID+'&text='+msg)
   upd= Updater(TOKEN, use_context=True)
   disp=upd.dispatcher
   
   
   disp.add_handler(CommandHandler('start', start))
   disp.add_handler(CommandHandler('spegni', spegni))
   disp.add_handler(CommandHandler('foto', foto))
   disp.add_handler(CommandHandler('help', help))
 
   upd.start_polling()
   upd.idle()
 
if __name__=='__main__':
   main()