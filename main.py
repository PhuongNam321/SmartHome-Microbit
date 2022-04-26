import serial.tools.list_ports
import sys
from Smarthouse import *
from threading import Thread
import time
from Adafruit_IO import MQTTClient

AIO_FEED_IDS = ["bedroom.led","ai","kitchen.fan"]
AIO_USERNAME = "andrewquang"
AIO_KEY = "aio_FjdB52sCWd56IjjPJcB9hUQhmTii"


def connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_IDS:
        client.subscribe(feed)


def subscribe(client, userdata, mid, granted_qos):
    print("Subcribe thanh cong...")


def disconnected(client):
    print("Ngat ket noi...")
    sys.exit(1)

Ai = ""
Led_bedroom = 45
Led_bathroom = 44
Fan_kitchen = 0

def message(client, feed_id, payload):
    global Ai,Led_bedroom,Led_bathroom,Fan_kitchen
    print("Nhan du lieu: " + payload)
    if isMicrobitConnected:
        ser.write((str(payload) + "#").encode())
    
    if payload == "53":
        Ai = 1
        print("đã nhận")
    elif payload == "47":
        Ai = 0
    elif payload == "55":
        Led_bedroom = 55
    elif payload == "45":
        Led_bedroom = 45 
    elif payload == "56":
        Led_bathroom = 56  
    elif payload == "44": 
        Led_bathroom = 44
    else:
        Fan_kitchen = int(payload) 


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort


isMicrobitConnected = False
if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    isMicrobitConnected = True

Temp = 25
Humi = 95
Gas = 99

def processData(data):
    global Temp, Humi, Gas, Led_bedroom
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    try:
        if splitData[1] == "TEMP":
            client.publish("bedroom.temp", splitData[2])
            Temp = splitData[2]
        elif splitData[1] == "HUMI":
            client.publish("bedroom.humi", splitData[2])
            Humi = splitData[2]
        elif splitData[1] == "GAS":
            client.publish("kitchen.gas", splitData[2])
            Gas = splitData[2]
        elif splitData[1] == "LEDBUTTON":
            client.publish("bedroom.led", splitData[2])
            Led_bedroom = splitData[2]
        elif splitData[1] == "LEDSENSOR":
            client.publish("bathroom.led", splitData[2]) 
    
    except:
        pass


mess = ""


def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

ON = 55
OFF = 45
Strong = 40
Medium = 30
Fit = 20
OFF_Fan = 0

def fan():
    global Fan_kitchen
    speak("Bạn muốn chọn chế độ bật quạt nào: \n1, To \n2, Trung bình \n3, Nhỏ ")
    text = hear()
    if "to" in text:
        client.publish("kitchen.fan", Strong)
        Fan_kitchen = Strong
        speak("Quạt đã bật theo ý của bạn")
    elif "trung bình" in text:
        client.publish("kitchen.fan", Medium)
        Fan_kitchen = Medium
        speak("Quạt đã bật theo ý của bạn")
    elif "nhỏ" in text:
        client.publish("kitchen.fan", Fit)
        Fan_kitchen = Fit
        speak("Quạt đã bật theo ý của bạn")

a = 1
counter = 0

def AI():
    while True:
        global a, counter, Ai, Temp, Humi, Gas, Led_bedroom, Fan_kitchen
        if Ai == 1:
            counter = 0    
            if a == 1:
                welcome()
                a = 0
            text = hear()
            if "bật đèn" in text:
                speak("Bạn muốn bật đèn nào: \n1, phòng ngủ \n2, phòng tắm")
                text = hear()
                if "phòng ngủ" in text:
                    if Led_bedroom == ON:
                        speak("Đèn phòng ngủ đang bật bạn đừng trêu tôi")
                    else:
                        client.publish("bedroom.led", ON)
                        Led_bedroom = ON
                        speak("Đèn phòng ngủ đã bật")
                elif "phòng tắm" :
                    speak("Tôi chưa được dạy")
            elif "tắt đèn" in text:
                speak("Bạn muốn tắt đèn nào: \n1, phòng ngủ \n2, phòng tắm")
                text = hear()
                if "phòng ngủ" in text:
                    if Led_bedroom == OFF:
                        speak("Đèn phòng ngủ đang tắt bạn đừng trêu tôi")
                    else:
                        client.publish("bedroom.led", OFF)
                        Led_bedroom = OFF
                        speak("Đèn phòng ngủ đã tắt")
                elif "phòng tắm" :
                    speak("Tôi chưa được dạy")
            elif "nhiệt độ" in text:
                speak("Nhiệt độ hiện tại là " + str(Temp) + " độ C")
            elif "độ ẩm" in text:
                speak("Độ ẩm hiện tại là " + str(Humi) + "%")
            elif "khí gas" in text or "nồng độ" in text:
                speak("Nồng độ khí gas hiện tại là " + str(Gas))
            elif "bật quạt" in text:
                if Fan_kitchen > Medium and Fan_kitchen <= Strong:
                    speak("Quạt đang được bật ở chế độ to, bạn muốn thay đổi chế độ khác ạ: \n1, Trung bình \n2, Nhỏ")
                    text = hear()
                    if "trung bình" in text:
                        client.publish("kitchen.fan", Medium)
                        Fan_kitchen = Medium
                        speak("Quạt đã bật theo ý của bạn")
                    elif "nhỏ" in text:
                        client.publish("kitchen.fan", Fit)
                        Fan_kitchen = Fit
                        speak("Quạt đã bật theo ý của bạn")
                elif Fan_kitchen > Fit and Fan_kitchen <= Medium:
                    speak("Quạt đang được bật ở chế độ trung bình, bạn muốn thay đổi chế độ khác ạ: \n1, To \n2, Nhỏ")
                    text = hear()
                    if "to" in text:
                        client.publish("kitchen.fan", Strong)
                        Fan_kitchen = Strong
                        speak("Quạt đã bật theo ý của bạn")
                    elif "nhỏ" in text:
                        client.publish("kitchen.fan", Fit)
                        Fan_kitchen = Fit
                        speak("Quạt đã bật theo ý của bạn")
                elif Fan_kitchen > 0 and Fan_kitchen <= Fit:
                    speak("Quạt đang được bật ở chế độ nhỏ, bạn muốn thay đổi khác ạ: \n1, To \n2, Trung bình")
                    text = hear()
                    if "to" in text:
                        client.publish("kitchen.fan", Strong)
                        Fan_kitchen = Strong
                        speak("Quạt đã bật theo ý của bạn")
                    elif "trung bình" in text:
                        client.publish("kitchen.fan", Medium)
                        Fan_kitchen = Medium
                        speak("Quạt đã bật theo ý của bạn")
                else:
                    fan()
            elif "tắt quạt" in text:
                if Fan_kitchen == OFF_Fan:
                    speak("Quạt đang được tắt bạn đừng trêu tôi")
                else:
                    client.publish("kitchen.fan", OFF_Fan)
                    Fan_kitchen = OFF_Fan
                    speak("Quạt đã được tắt")
            elif "tạm biệt" in text:
                client.publish("ai",47)
                Ai = 0
                a = 1
                counter = 2
                speak("Tạm biệt, hẹn gặp lại")
        elif Ai == 0:
            counter += 1
            if counter == 1: 
                speak("Tạm biệt, hẹn gặp lại")
        time.sleep(1)


def gateway():
    while True:
        if isMicrobitConnected:
            readSerial()
        time.sleep(1)

thread2 = Thread(target=AI)
thread2.start()

thread1 = Thread(target=gateway)
thread1.start()