from microbit import *
import radio
import neopixel
from utime import ticks_us, sleep_us

neopixels = neopixel.NeoPixel(pin13, 12)

radio.config(channel=1)
radio.on()

ANALOG_MAX = 1023

SONAR = pin15

def sonar( ):
    SONAR.write_digital(1) # Send 10us Ping pulse
    sleep_us(10)
    SONAR.write_digital(0)
    SONAR.set_pull(SONAR.NO_PULL)
    while SONAR.read_digital() == 0: # ensure Ping pulse has cleared
        pass
    start = ticks_us() # define starting time
    while SONAR.read_digital() == 1: # wait for Echo pulse to return
        pass
    end = ticks_us() # define ending time
    echo = end-start
    distance = int(0.01715 * echo) # Calculate cm distance
    return distance


# Converting values into a valid int between
# 0-1023 for valid analog signals
def to_analog(value):
    global ANALOG_MAX
    analog_val = int(value * ANALOG_MAX)
    return analog_val


# Checking that the user has entered a valid
# speed before we can set the motors to that
# speed. Raises an error if invalid speed is entered
def check_speed(speed):
    if speed < 0 or speed > 1:
        raise ValueError("Invalid speed value for motors")


# Class for controlling Bit:bot motors
class Motors:
    # accelerate() moves the Bit:bot forward at a speed
    # set by the user. The speed must be between 0 - 1
    def accelerate(self, speed):
        # Setting our bit:bot motors direction
        # to go forwards before sending it forwards
        pin8.write_digital(0)
        pin12.write_digital(0)

        # Checking that the user has entered a valid
        # speed before we can set the motors to that
        # speed
        check_speed(speed)

        analog_val = to_analog(speed)
        pin0.write_analog(analog_val)
        pin1.write_analog(analog_val)

    # Halting to a complete stop
    def stop(self):
        # Setting our bit:bot motors direction
        # to go forwards before stopping by default
        pin8.write_digital(0)
        pin12.write_digital(0)

        pin0.write_digital(0)
        pin1.write_digital(0)

    # spin_left() spins the Bit:bot left at a certain speed
    def spin_left(self, speed):
        check_speed(speed)
        analog_val = to_analog(speed)

        pin0.write_analog(0)
        pin1.write_analog(analog_val)

    # spin_right() spins the Bit:bot right at a certain speed
    def spin_right(self, speed):
        check_speed(speed)
        analog_val = to_analog(speed)

        pin0.write_analog(analog_val)
        pin1.write_analog(0)

    # reverse() will reverse the bit:bot at a
    # certain speed
    def reverse(self, speed):
        check_speed(speed)
        analog_val = ANALOG_MAX - to_analog(speed)

        # Setting our bit:bot motors direction
        # to go backwards before sending it backwards
        pin8.write_digital(1)
        pin12.write_digital(1)

        pin0.write_analog(analog_val)
        pin1.write_analog(analog_val)


# Class for dealing with Line following
class Line:
    # detecting whether on a line on right sensor
    # return true if on line otherwise false
    def is_right_line(self):
        right_ln_val = not bool(pin5.read_digital())
        return right_ln_val

    # detecting whether on a line on left sensor
    # return true if on line otherwise false
    def is_left_line(self):
        left_ln_val = not bool(pin11.read_digital())
        return left_ln_val


class Light:
    def get_light_val(self):
        light_val = pin2.read_digital()
        print(light_val)


class Animation:
    def neoRainbow():
        for i in range(12):
            if i == 0 or i == 6:
                neopixels[i] = (255, 0, 0)
            if i == 1 or i == 7:
                neopixels[i] = (255, 122, 0)
            if i == 2 or i == 8:
                neopixels[i] = (255, 255, 0)
            if i == 3 or i == 9:
                neopixels[i] = (0, 255, 0)
            if i == 4 or i == 10:
                neopixels[i] = (0, 0, 255)
            if i == 5 or i == 11:
                neopixels[i] = (255, 0, 255)
            neopixels.show()
            sleep(10)

    def fire():
        for i in range(6):
            neopixels[i] = (255, 0, 0)
            neopixels[i + 6] = (255, 0, 0)
            sleep(30)
            neopixels.show()
        pin14.write_digital(1)
        sleep(10)
        pin14.write_digital(0)
        for i in range(6):
            neopixels[i] = (255, 255, 255)
            neopixels[i + 6] = (255, 255, 255)
            sleep(30)
            neopixels.show()
        sleep(30)
        Animation.neoRainbow()


motors = Motors()

Animation.neoRainbow()

while True:
    msg = radio.receive()
    if msg:
        if msg == "leftA":
            motors.spin_left(0.7)
            display.show(Image.ARROW_W)
            print("left")
        if msg == "rightA":
            motors.spin_right(0.7)
            display.show(Image.ARROW_E)
            print("right")
        if msg == "accelerateA":
            motors.accelerate(0.7)
            print("forward")
        if msg == "FireA":
            Animation.fire()
            print("Fire!")
            display.scroll(sonar())
            sleep(500)
    else:
        motors.stop()
        print("stop")
