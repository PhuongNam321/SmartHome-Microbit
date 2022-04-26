from hear_speak import *
# from speak import *

speak("Xin chào")

while True:

    you = hear()

    if you == None:
        speak("Bạn nói lại được không?")
    elif "hôm nay" in you and "bao nhiêu" in you and "ngày" in you:
        speak("Hôm nay là ngày 11 tháng 4")