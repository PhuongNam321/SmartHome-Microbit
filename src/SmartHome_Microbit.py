# Code microbit muốn sử dụng hãy truy cập vào trang https://makecode.microbit.org/ 

def led_button():
    global led_status_button, status_led_button
    led_status_button = 1 - led_status_button
    pins.digital_write_pin(DigitalPin.P5, led_status_button)
    pins.digital_write_pin(DigitalPin.P6, 0)
    if led_status_button == 0:
        status_led_button = 45
        serial.write_string("!1:LEDBUTTON:" + ("" + str(status_led_button)) + "#")
    elif led_status_button == 1:
        status_led_button = 55
        serial.write_string("!1:LEDBUTTON:" + ("" + str(status_led_button)) + "#")
def led_sensor_light():
    global status_led_light
    pins.digital_write_pin(DigitalPin.P6, 0)
    pins.digital_write_pin(DigitalPin.P7, led_status_light)
    if led_status_light == 0:
        if counter_status_light <= 1:
            status_led_light = 46
            serial.write_string("!1:LEDSENSOR:" + ("" + str(status_led_light)) + "#")
    elif led_status_light == 1:
        if counter_status_dark <= 1:
            status_led_light = 54
            serial.write_string("!1:LEDSENSOR:" + ("" + str(status_led_light)) + "#")
def temp_humi_lcd():
    global counter_lcd
    counter_lcd += 1
    if counter_lcd >= 1000:
        counter_lcd = 0
        NPNBitKit.dht11_read(DigitalPin.P2)
        NPNLCD.clear()
        NPNLCD.show_string("Nhiet Do: " + ("" + str(NPNBitKit.dht11_temp())) + " C",
            0,
            0)
        NPNLCD.show_string("Do Am: " + ("" + str(NPNBitKit.dht11_hum())) + "%", 0, 1)
        serial.write_string("!1:TEMP:" + ("" + str(NPNBitKit.dht11_temp())) + "#")
        serial.write_string("!1:HUMI:" + ("" + str(NPNBitKit.dht11_hum())) + "#")
def sensor_light():
    global counter_light, counter_dark, counter_status_dark, counter_status_light, led_status_light
    if pins.analog_read_pin(AnalogPin.P1) < 600:
        counter_light = 0
        counter_dark += 1
        if counter_dark > 5:
            counter_status_dark += 1
            counter_status_light = 0
            led_status_light = 1
            led_sensor_light()
    else:
        counter_dark = 0
        counter_light += 1
        if counter_light > 5:
            counter_status_light += 1
            counter_status_dark = 0
            led_status_light = 0
            led_sensor_light()
            counter_light = 0
def button():
    global key1, key0, key_process
    key1 = key0
    key0 = pins.digital_read_pin(DigitalPin.P0)
    if key1 == key0:
        if key_process != key1:
            key_process = key1
            if key_process == 0:
                led_button()
def fan():
    pins.digital_write_pin(DigitalPin.P8, 1)
    pins.analog_write_pin(AnalogPin.P9, value * 20)
def co2_alarm():
    global counter_Co2
    if pins.analog_read_pin(AnalogPin.P3) >= 600:
        pins.digital_write_pin(DigitalPin.P10, 1)
        pins.digital_write_pin(DigitalPin.P11, 0)
        pins.digital_write_pin(DigitalPin.P4, 1)
    elif pins.analog_read_pin(AnalogPin.P3) >= 300:
        pins.digital_write_pin(DigitalPin.P10, 1)
        pins.digital_write_pin(DigitalPin.P11, 1)
    else:
        pins.digital_write_pin(DigitalPin.P10, 0)
        pins.digital_write_pin(DigitalPin.P11, 1)
    counter_Co2 += 1
    if counter_Co2 > 500:
        counter_Co2 = 0
        serial.write_string("!1:GAS:" + ("" + str(pins.analog_read_pin(AnalogPin.P3))) + "#")

def on_data_received():
    global cmd, led_status_button, led_status_light, value
    cmd = serial.read_until(serial.delimiters(Delimiters.HASH))
    if cmd == "45":
        pins.digital_write_pin(DigitalPin.P5, 0)
        led_status_button = 0
    elif cmd == "55":
        pins.digital_write_pin(DigitalPin.P5, 1)
        led_status_button = 1
    elif cmd == "46":
        pins.digital_write_pin(DigitalPin.P7, 0)
        led_status_light = 0
    elif cmd == "54":
        pins.digital_write_pin(DigitalPin.P7, 1)
        led_status_light = 1
    else:
        value = int(cmd)
serial.on_data_received(serial.delimiters(Delimiters.HASH), on_data_received)

cmd = ""
counter_Co2 = 0
value = 0
key0 = 0
key1 = 0
status_led_light = 0
status_led_button = 0
counter_status_light = 0
counter_status_dark = 0
counter_lcd = 0
counter_dark = 0
counter_light = 0
key_process = 0
led_status_light = 0
led_status_button = 0
led.enable(False)
led_status_button = 0
led_status_light = 0
pins.digital_write_pin(DigitalPin.P5, led_status_button)
pins.digital_write_pin(DigitalPin.P7, led_status_light)
pins.set_pull(DigitalPin.P0, PinPullMode.PULL_UP)
key_process = 1
counter_light = 0
counter_dark = 0
counter_lcd = 0
counter_status_dark = 0
counter_status_light = 0
NPNLCD.lcd_init()
NPNLCD.show_string("L01_CSE Xin Chao", 0, 0)

def on_forever():
    temp_humi_lcd()
    co2_alarm()
    sensor_light()
    button()
    fan()
    basic.pause(20)
basic.forever(on_forever)
