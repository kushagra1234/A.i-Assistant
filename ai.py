import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import calendar
import wikipedia
import pywhatkit
import pyjokes
from playsound import playsound
import os
from pygame import mixer
import keyboard

def acceptCommands():
  r=sr.Recognizer()
  with sr.Microphone() as source:
    print('Listening')
    r.pause_treshold=0.8
    audio=r.listen(source)
    try:
      print('Recognizer')
      Query=r.recognize_google(audio, language='en-in')
    except Exception as e:
      print(e)
      return "None"
    return Query

def speak(audio):
  engine=pyttsx3.init()
  voices=engine.getProperty('voices')
  engine.setProperty('voice',voices[0].id)
  rate=engine.getProperty('rate')
  engine.setProperty('rate', 130)
  engine.say(audio)
  engine.runAndWait()

def tellDay():
  day=datetime.date.today()
  speak(calendar.day_name[day.weekday()])
    
def tellTime():
  current_time=datetime.datetime.now().strftime("%I:%M %p")
  output= "Your current local time is" + current_time
  speak(output)
  
def tellDate():
  speak('todays date is')
  speak(datetime.date.today())

def Take_query(query):
    playsound('sound.wav')
    if "open youtube" in query:
      speak("Opening youtube ")
      webbrowser.open("www.youtube.com")
    
    elif "open browser" in query:
      speak("Opening Google Chrome ")
      webbrowser.open("www.google.com")
    
    elif "open chrome" in query or "open google chrome" in query:
      try:os.system('start chrome')
      except:pass
    
    elif "open firefox" in query or "open mozilla firefox" in query:
      try:os.system('start firefox')
      except:pass
      
    elif "open edge" in query or "open microsoft edge" in query:
      try:os.system('start microsoft edge')
      except:pass
      
    elif "date" in query:
      tellDate()
    
    elif "what day is it" in query or "todays day" in query:
      tellDay()
    
    elif "tell me the time" in query or "what time is it" in query:
      tellTime()
        
    elif "goodbye" in query:
      speak("Goodbye ")
      exit()
      
    elif "from wikipedia" in query:
      speak("Checking wikipedia ")
      query = query.replace("wikipedia","")
      result=wikipedia.summary(query, sentences=4)
      speak("According to Wikipedia")
      speak(result)
      
    elif "your name" in query:
      speak("I am Google")
      
    elif "search" in query:
      speak("Searching results in google!")
      query = query.split()
      query = ' '.join(query[query.index('search')+1:])
      pywhatkit.search(query)
      
    elif "play" in query:
      speak('playing'+ query)
      pywhatkit.playonyt(query)
      
    elif "joke" in query:
      speak(pyjokes.get_joke())
    
    elif "shutdown the computer" in query or "turn off the computer" in query:
      os.system('shutdown /s')
      exit()
      
    elif "restart the computer" in query:
      os.system('shutdown /r')
      exit()
      
    elif "wake me up in" in query or "set alarm at" in query:
      set_time = alarm_format(query)
      if set_time == None:return
      global alarm
      alarm = set_time
      with open('alarm.txt','w') as w:
         w.write(set_time)
      set_time = set_time.split()
      set_time.pop(0)
      speak("Setting your alarm at " + " ".join(set_time))

def alarm_format(query):
   n = datetime.datetime.now()
   if 'set alarm at' in query:
      query = query.split()
      query = query[query.index('at')+1:]
      l = len(query)
      current_h = int(n.strftime("%I"))
      current_m = int(n.strftime("%M"))
      current_p = n.strftime("%p")
      d = int(n.strftime("%d"))
      if l==1:
         if ':' not in query[0]:
            if int(query[0])>12:return
            if current_h<int(query[0]):
               return str(d) + ' ' + query[0] +' 00 '+current_p
            else:
               if current_p=='AM':return str(d) + ' ' + query[0] + ' 00 PM'
               return str(d+1) + ' ' + query[0] +' 00 AM'
         elif ':' in query[0]:
            tim = query[0].split(':')
            if current_h<int(tim[0]) or (current_h==int(tim[0]) and current_m<int(tim[1])):return str(d) + ' ' + tim[0]+' '+tim[1]+' '+current_p
            else:
               if current_p=='AM':return str(d) + ' ' + str(h) + ' ' + str(m) + ' PM'
               return str(d+1) + ' ' + tim[0] + ' ' + tim[1] + ' AM' 
            
      elif l==4:
         if int(query[0])>12 or int(query[2])>59:return
         if current_h<int(query[0]) or (current_h==int(query[0]) and current_m<int(query[2])):
            return str(d) + ' ' + query[0] + ' ' + query[2] +' '+ current_p
         else:
            if current_p=='AM':return str(d) + ' ' + query[0] + ' ' + query[2] +' PM'
            return str(d+1) + ' ' + query[0] + ' ' + query[2] +' AM'
      
      elif l==2:
         if query[1]=='AM' and current_p=='PM':d+=1
         if ':' in query[0]:
            tim = query[0].split(':')
            if int(tim[0])>12 or int(tim[1])>59:return
            return str(d) + ' ' + tim[0]+' '+tim[1]+' '+query[1].replace('.','').upper()
         if int(query[0])>12:return
         return str(d) + ' ' + query[0]+' 00 '+query[1].replace('.','').upper()
   elif 'wake me up in' in query:
      query = query.split()
      query = query[query.index('in')+1:]
      l = len(query)
      current_h = int(n.strftime("%I"))
      current_m = int(n.strftime("%M"))
      current_p = n.strftime("%p")
      d = int(n.strftime("%d"))
      m = h = 0
      _ =  int(query[0])
      if query[1]=='minutes' or query[1]=='minute':
         if current_m+(_%60)>=60:
            m = current_m+(_%60)-60
            h = current_h+(_//60)+1
         else:
            m = current_m+(_%60)
            h = current_h+(_//60)
      elif query[1]=='hour' or query[1]=='hours':
         h = current_h + _
         m = current_m
      if h>12:
         h-=12
         if current_p=='AM':return str(d) + ' ' + str(h) + ' ' + str(m) + ' PM'
         return str(d+1) + ' ' + str(h) + ' ' + str(m) + ' AM'
      return str(d) + ' ' + str(h) + ' ' + str(m) + ' ' + current_p


if __name__== '__main__':
  mixer.init()
  mixer.music.load('Kalimba.mp3')
  try:
     with open('alarm.txt','r') as r:
        alarm = r.read()
  except:alarm = ''
  while True:
    n = datetime.datetime.now()
    date = n.strftime("%d %I %M %p").split()
    date = str(int(date[0]))+" "+str(int(date[1]))+" "+str(int(date[2]))+" "+date[3]
    if alarm  == date:
       alarm = ''
       mixer.music.play(-1)
       speak("Press any key to stop the alarm")
       while True:
          if keyboard.is_pressed(' '):
             mixer.music.stop()
             speak('Alarm stopped')
             break
    query = acceptCommands().lower()
    if 'ok google' in query or 'hey google' in query:
       print('match')
       query = query.replace('ok google','').replace('hey google','').strip()
       if len(query)!=0:
          Take_query(query)
       else:
          query = acceptCommands().lower()
          Take_query(query)
       query = ''