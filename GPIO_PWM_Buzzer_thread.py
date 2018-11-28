import time
import RPI.GPIO as GPIO
from threading import Thread

class Buzzer(Thread):
    def __init__(self, get_distance):
        self.get_distance = get_distance
        # Raspberry pi pin number
        buzzer_pin = 33
        frequency = 100
        self.buzzer = GPIO.setup(buzzer_pin, frequency)