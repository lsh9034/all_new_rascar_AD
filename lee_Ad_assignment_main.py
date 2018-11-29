#########################################################################
# Date: 2018/10/02
# file name: 3rd_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import time


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)
        self.default_degree = 10 #기본적으로 꺽어야하는 기본 각도
        self.weight = [-4,-2,0,2,4] #검은 색 선의 위치에 따라 곱해야할 배수

    def drive_parking(self):
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

    def read_digit(self):
        return self.car.line_detector.read_digital()

    def turn(self, degree):
        min_degree = -35
        max_degree = 35
        degree = max(min_degree, min(max_degree, degree))
        self.car.steering.turn(90 + degree)

    # =======================================================================
    # 3RD_ASSIGNMENT_CODE
    # Complete the code to perform Third Assignment
    # =======================================================================

    def Sort_line(self,past_degree,speed):
        print("Sort_line")
        temp = past_degree - 90
        angle = 90 - temp
        self.car.steering.turn(angle)
        self.car.accelerator.go_backward(speed * 0.7) #양쪽 모터 값이 speed로 바뀜
        while (not self.car.line_detector.is_in_line()):
            continue
        time.sleep(0.1)
        self.car.steering.turn(past_degree)
        self.car.accelerator.go_forward(speed)
        #self.set_L_R_speed(past_degree,speed)

    def set_L_R_speed(self,degree,speed):
        temp_degree = 90 - degree
        left_motor_speed = speed
        right_motor_speed = speed
        if temp_degree >= 0 :
            speed_ratio = (1 - temp_degree/50)
            left_motor_speed = left_motor_speed * speed_ratio
        elif temp_degree < 0:
            speed_ratio = (1 + temp_degree/50)
            right_motor_speed = right_motor_speed * speed_ratio

        self.car.accelerator.right_wheel.speed = int(left_motor_speed)
        self.car.accelerator.left_wheel.speed = int(right_motor_speed)

    def Obstacle_detect(self,Limit_distance):
        distance = self.car.distance_detector.get_distance()
        # print(distance)
        if distance < Limit_distance and distance != -1:
            return True
        else:
            return False

    def avoid_Obastacle(self,speed):
        print("avoiding")
        self.move(speed)
        self.turn(-40)
        time.sleep(0.6)
        while(not self.car.line_detector.is_in_line()):
            continue
        self.turn(40)
        time.sleep(1.6)
        while(not self.car.line_detector.is_in_line()):
            continue

        self.turn(-15)
        time.sleep(1.5)
        self.turn(0)
        self.move(-speed)
        time.sleep(1.5)
        self.move(speed)

    def compute_degree(self,lines):
        degree = 0
        check = False
        for i in range(len(lines)):
            if lines[i] == 1:  # 맨 처음 1을 만났을 때는 가중치를 곱해줌
                if check == False:
                    degree += self.weight[i] * self.default_degree
                    check = True
                    # check_start = False
                elif check == True:  # 그 다음 1을 만났을 때는 기본 각도만큼 더해줌
                    degree += self.default_degree
        return check,degree

    #T_parking
    def T_parking(self):
        print("T_parking")
        speed = 30

        self.move(speed)
        self.turn(30)
        time.sleep(1.5)
        self.turn(-15)
        self.move(-(speed))
        time.sleep(1)
        while(not self.car.line_detector.is_in_line()):
            continue
        print("asdf")

        lines = self.read_digit()
        past_degree = 0
        check_Start = True
        start_time = time.time()
        while(time.time() - start_time >= 1.5):
            lines = self.read_digit()
            check,degree = self.compute_degree(lines)
            if(past_degree != degree):
                past_degree = degree
                self.turn(degree)
            if(lines != [0,0,0,0,0]):
                start_time = time.time()


        self.move(speed)
        time.sleep(0.4)
        self.stop()
        while(True):
            continue

    def line_tracing(self):
        print("line_tracing")
        past_degree = 90  # 처음은 정면
        #check_start = True  # 만약 센서가 검은색 선 위에 없이 시작했을 경우에도 작동하기 위해 만든 변수
        speed = 50
        self.car.accelerator.go_forward(speed)  # 전진
        count = 0
        count_obstacle = 0
        pass_obstacle = 0
        check_T = True
        while (True):

            if(pass_obstacle<2):
                if (self.Obstacle_detect(30)):
                    count_obstacle += 1
                    if (count_obstacle >= 3):
                        self.avoid_Obastacle(35)
                        pass_obstacle += 1
                        print(pass_obstacle)
                else:
                    count_obstacle = 0

            status = self.car.line_detector.read_digital()  # 5개의 센서값 받아옴

            check,degree = self.compute_degree(status) #check는 라인밖으로 나갔는지 degree는 꺽어야할 각도

            if pass_obstacle ==1:
                print(status)
            if check == False:
                count=0
                self.Sort_line(past_degree,speed)
            elif degree != past_degree:  # 전에 꺽은 각도와 다른 경우에만 서보모터에 각도 적용
                self.turn(degree)
                past_degree = degree
                #self.set_L_R_speed(degree,speed)

            elif [1,1,1,1,1] == status and count > 4000:
                break
            if (status == [1,1,1,0,0] or status == [1,1,1,1,0] or status == [0,1,1,1,0]) and pass_obstacle==1 and check_T == True:
                self.T_parking()
                check_T = False

            count+=1
        self.car.accelerator.stop()

    def car_startup(self):
        # implement the assignment code here
        self.line_tracing()
        pass


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()
        #myCar.car.accelerator.go_forward(60)
        #myCar.car.accelerator.left_wheel.speed = 30
        #while(1):
         #   continue
    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()