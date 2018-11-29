import time
import RPi.GPIO as GPIO
from threading import Thread

distance_arr = [10, 12, 14, 15, 16, 17, 20, 25, 30 , 34, 40 , 50 , 70, 100]

class Buzzer(Thread):
    def __init__(self):
        self.distance = 5000
        # Raspberry pi pin number
        buzzer_pin = 11
        frequency = 100
        GPIO.setmode(GPIO.BOARD)
        self.buzzer = GPIO.setup(buzzer_pin, frequency)
        self.buzzer.ChangeFrequency(523.2)
        self.beforeTime = time.time()
        self.delay = 1E-5
        self.__stop = False
    
    def stop(self, boolean=True):
        self.__stop = boolean
    
    def set_distance(self, distance):
        self.distance = distance

    def run(self):
        buzzerTimeRate = 0.02
        while not self.__stop:
            now = time.time()
            diff = now - self.beforeTime
            if diff < self.delay:
                continue
            self.beforeTime = now
            if self. distance < 50:
                self.buzzer.start(5)
                buzzerTime = buzzerTimeRate * self.distance
                self.delay = buzzerTime * 5
                time.sleep(buzzerTime)
                self.buzzer.stop()
            time.sleep(3E-3)

if __name__ == "__main__":
    buzzer = Buzzer()
    for distance in distance_arr:
        buzzer.set_distance(distance)
