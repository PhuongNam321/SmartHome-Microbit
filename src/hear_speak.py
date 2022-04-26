import speech_recognition as sr
from gtts import gTTS
import playsound
import os

def hear():
    c = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Adjusting noise ")
        c.adjust_for_ambient_noise(source, duration = 2)
        # print("Recording for 4 seconds")
        c.pause_threshold = 2
        audio = c.listen(source, phrase_time_limit = 3)
        # print("Done recording")
    try:
        query = c.recognize_google(audio,language='vi-VN')
        print("SmartHome: "+query)
    except sr.UnknownValueError:
        print('Xin lỗi tôi không nghe được bạn nói. Bạn có thể viết ra được không?')
        query = str(input('Điều bạn muốn: '))
    return query.lower()

def speak(query):
    print("SmartHome: " + query)
    tts = gTTS(text= query, lang="vi", slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", True)
    os.remove("sound.mp3")

        