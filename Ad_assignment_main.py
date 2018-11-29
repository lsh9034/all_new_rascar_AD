#########################################################################
# Date: 2018/11/07
# file name: 3st_assignment_main.py
# Purpose: this code has been generated for the 4 wheels drive body
# moving object to perform the project with ultra sensor
# this code is used for the student only
#########################################################################

from car import Car
import time
import numpy
import constant_setting
from GPIO_PWM_Buzzer_thread import Buzzer

class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)
        self.STOP = 0
        self.EVADING = 1
        self.T_PARKING = 2

        self.buzzer = None

    def drive_parking(self):
        self.buzzer.stop()
        self.car.drive_parking()

    # move front when speed is positive, else move back
    def move(self, speed):
        speed = int(speed)
        if speed < 0:
            self.car.accelerator.go_backward(abs(speed))
        else:
            self.car.accelerator.go_forward(speed)

    # stop
    def stop(self):
        self.car.accelerator.stop()

    # get distance by accpeted error for stable distance
    def get_distance(self):
        distances = sorted([self.car.distance_detector.get_distance() for i in range(5)])
        return distances[2]

    def read_digit(self):
        return numpy.array(self.car.line_detector.read_digital())
    
    def turn(self, degree):
        min_degree = -35
        max_degree = 35
        degree = max(min_degree, min(max_degree, degree))
        self.car.steering.turn(90 + degree)

    # evading obstacle
    def evading(self):
        print("evading")
        speed = constant_setting.evading_speed
        turn_left_angle = -23
        turn_right_angle = 23

        self.move(speed)
        self.turn(turn_left_angle)
        while numpy.sum(self.read_digit()) > 0:
            time.sleep(0.01)
        
        while numpy.sum(self.read_digit()) == 0:
            time.sleep(0.01)

        self.turn(turn_right_angle)
        while numpy.sum(self.read_digit()) > 0:
            time.sleep(0.01)

        while numpy.sum(self.read_digit()) == 0:
            time.sleep(0.01)
        self.turn(turn_left_angle)
        time.sleep(0.2)
    
    # T parking
    def T_parking(self):
        print("T_parking")
        speed = constant_setting.T_parking_speed
        vector = numpy.array([-3, -1, 0, 1, 3])
        turning_rate = constant_setting.turning_rate

        self.stop()
        self.turn(0)
        self.move(-speed)
        time.sleep(0.6)
        self.turn(25)
        self.move(speed)
        time.sleep(0.6)
        self.move(-speed)
        self.turn(0)

        lines = self.read_digit()
        while( (lines != [0,0,0,0,0]).all() ):
            lines = self.read_digit()
            lines_sum = numpy.sum(lines)
            dot = numpy.dot(vector, lines)
            turning_angle = dot * turning_rate / lines_sum
            self.turn(turning_angle)
        self.move(speed)
        time.sleep(0.4)


    def driving(self):
        print("driving")
        case = self.STOP
        speed = constant_setting.driving_speed
        count = 0
        stop_condition = 2
        
        # evading setting
        obstacle_count = 0
        obstacle_detected_distance = 40
        evading_condition = 2

        # T parking setting
        T_parking_condition = numpy.array([1, 0, 0, 0, 1])
        
        vector = numpy.array([-3, -1, 0, 1, 3])
        turning_rate = constant_setting.turning_rate
        before_turning_angle = -25
        before_lines_sum = 0
        self.move(speed)
        while True:
            lines = self.read_digit()
            lines_sum = numpy.sum(lines)
            if lines_sum >= 5:
                count += 1
                if count >= stop_condition:
                    break
            else:
                count = 0
                is_turning = False
                if lines_sum == 0:
                    self.turn(-before_turning_angle)
                    self.move(-speed)
                    is_turning = True
                elif before_lines_sum == 0:
                    self.turn(before_turning_angle)
                    self.move(speed)
                    is_turning = True
                before_lines_sum = lines_sum
                if is_turning:
                    continue

            distance = self.get_distance()
            if distance > 70:
                obstacle_count = 0
            if 0 < distance and distance < obstacle_detected_distance:
                obstacle_count += 1
                if obstacle_count > evading_condition:
                    obstacle_count = 0
                    case = self.EVADING
                    break
            
            if (lines == T_parking_condition).all():
                case =  self.T_PARKING
                break

            dot = numpy.dot(vector, lines)
            turning_angle = dot * turning_rate / lines_sum if lines_sum else before_turning_angle
            if before_turning_angle == turning_angle:
                continue
            before_turning_angle = turning_angle
            self.turn(turning_angle)
            self.move(speed)
            
        self.stop()
        return case

    # assignment code
    def assign(self):
        while True :
            case = self.driving()
            if case == self.STOP:
                return
            elif case == self.EVADING:
                self.evading()
            elif case == self.T_PARKING:
                self.T_parking()
                break
        
        self.driving()

    # =======================================================================
    # 3RD_ASSIGNMENT_CODE
    # Complete the code to perform First Assignment
    # =======================================================================
    def car_startup(self):
        # Implement the assignment code here.
        try:
            self.buzzer = Buzzer(self.get_distance)
            self.buzzer.start()
            self.assign()
        except Exception as e:
            print(e)
            self.buzzer.stop()
            self.stop()


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        while True:
            input("Press Enter to Start")
            myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
