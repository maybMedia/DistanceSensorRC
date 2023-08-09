from microbit import *
import radio
import neopixel

INTERVAL = 500

a_time = 0
b_time = 0

a = 0
b = 0
ab = 0

score = 0


radio.config(channel=1)
radio.on()

neopixels = neopixel.NeoPixel(pin13, 12)

for i in range(12):
    neopixels[i] = (0, 255, 0)

while True:

    msg = radio.receive()

    if button_a.was_pressed():
        print("bro")
        if a_time + INTERVAL >= running_time():
            radio.send("FireA")
            display.show(Image.DIAMOND)
            sleep(100)
            print("bro1")
        if a_time > 0:
            a += 1
            print(
                (
                    a,
                    b,
                    ab,
                )
            )
        a_time = running_time()
    if button_a.is_pressed() and button_b.is_pressed():
        radio.send("accelerateA")
        display.show(Image.ARROW_N)
    elif button_a.is_pressed():
        radio.send("leftA")
        display.show(Image.ARROW_W)
    elif button_b.is_pressed():
        radio.send("rightA")
        display.show(Image.ARROW_E)
    else:
        display.clear()
