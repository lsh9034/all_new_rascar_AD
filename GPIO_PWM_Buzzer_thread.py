import time
import RPi.GPIO as GPIO

class Buzzer:
    def __init__(self, get_distance):
        self.get_distance = get_distance
        # Raspberry pi pin number
        buzzer_pin = 8
        frequency = 100
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(buzzer_pin, GPIO.OUT)
        self.buzzer = GPIO.PWM(buzzer_pin, frequency)
        self.buzzer.ChangeFrequency(523.2)
        self.beforeTime = time.time()
        self.delay = 1E-5
        self.__stop = False
    
    def stop(self, boolean=True):
        self.__stop = boolean

    def run(self):
        buzzerTimeRate = 0.001
        while not self.__stop:
            now = time.time()
            diff = now - self.beforeTime
            if diff < self.delay:
                continue
            self.beforeTime = now
            distance = self.get_distance()
            if distance > 0 and distance < 50:
                self.buzzer.start(5)
                buzzerTime = buzzerTimeRate * distance
                self.delay = buzzerTime * 5
                time.sleep(buzzerTime)
                self.buzzer.stop()
            time.sleep(3E-3)
