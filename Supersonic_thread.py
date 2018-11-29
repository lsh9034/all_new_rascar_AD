from threading import Thread
from SR02 import SR02_Supersonic as Supersonic_Sensor
import time

class Supersonic(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.distance = 5000
        self.beforeTime = time.time()
        self.__stop = False
        try:
            self.distance_detector = Supersonic_Sensor.Supersonic_Sensor(35)
        except Exception as e:
            print("Learn more : " + e)
        
    def stop(self, boolean=True):
        self.__stop = boolean

    # get distance by accpeted error for stable distance
    def get_distance(self):
        distances = sorted([self.distance_detector.get_distance() for i in range(5)])
        return distances[2]

    def run(self):
        while not self.__stop:
            now = time.time()
            diff = now - self.beforeTime
            if diff < 1E-2:
                continue
            self.beforeTime = now
            self.get_distance()
            time.sleep(3E-3)