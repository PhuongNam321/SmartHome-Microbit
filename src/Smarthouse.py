from src.hear_speak import *
import datetime

def time():
    Time=datetime.datetime.now().strftime("%I:%M:%p") 
    speak("Hôm nay là")
    speak(Time)

def welcome():
    hour=datetime.datetime.now().hour
    if hour >=0 and hour<12:
        speak("SmartHome xin chào buổi sáng!")
    elif hour>=12 and hour<18:
        speak("Smarthome xin chào buổi chiều!")
    elif hour>=18 and hour<24:
        speak("SmartHome xin chào buổi tối")
    speak("Tôi có thể giúp gì cho bạn?") 

# def command():
#     c = sr.Recognizer()
#     with sr.Microphone() as source:
#         # print("Adjusting noise ")
#         c.adjust_for_ambient_noise(source, duration = 2)
#         # print("Recording for 4 seconds")
#         c.pause_threshold = 2
#         audio = c.listen(source,phrase_time_limit=3)
#         # print("Done recording")
#     try:
#         query = c.recognize_google(audio,language='vi-VN')
#         print("SmartHome: "+query)
#     except sr.UnknownValueError:
#         print('Sorry sir! I didn\'t get that! Try typing the command!')
#         query = str(input('Your order is: '))
#     return query.lower()

# if __name__  =="__main__":
#     welcome()

#     while True:
#         query=command().lower()
#         # All the command will store in lower case for easy recognition
#         if "bật đèn" in query:
#             speak("What should I search,boss")
#             search=command().lower()
#             url = f"https://google.com/search?q={search}"
#             wb.get().open(url)
#             speak(f'Here is your {search} on google')
        
#         elif "youtube" in query:
#             speak("What should I search,boss")
#             search=command().lower()
#             url = f"https://youtube.com/search?q={search}"
#             wb.get().open(url)
#             speak(f'Here is your {search} on youtube')

#         elif "quit" in query:
#             speak("Friday is off. Goodbye boss")
#             quit()
#         elif "open video" in query:
#             meme =r"C:\Users\Admin\Desktop\test\meme.mp4"
#             os.startfile(meme)
#         if "bật đèn" in query:
#             speak("") 
#         elif 'time' in query:
#             time()