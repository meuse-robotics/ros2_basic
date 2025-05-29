from robot_interfaces.srv import RobotCommand

import rclpy
from rclpy.node import Node
from gpiozero import Button
from gpiozero import PWMOutputDevice
import threading


class RobotService(Node):
    target_speed_R = 0.0
    target_speed_L = 0.0
    def __init__(self):
        super().__init__('robot_service')
        self.srv = self.create_service(RobotCommand, 'robot_command', self.robot_command_callback)

    def robot_command_callback(self, request, response):
        global count_R
        global count_L

        response.done = False
        count_R = 0
        count_L = 0
        self.target_speed_R = 0.3
        self.target_speed_L = 0.3
        while count_R < request.dist:
            #print(count_R)
            pass
        self.target_speed_R = 0.0
        self.target_speed_L = 0.0
        MOT_R_1.value = 0
        MOT_R_2.value = 0
        init_variables_R()
        MOT_L_1.value = 0
        MOT_L_2.value = 0
        init_variables_L()
        response.done = True
        return response


def enc_callback_R():
    global count_R
    global robot_service
    if robot_service.target_speed_R > 0:
        count_R += 1
    else:
        count_R -= 1
    
def enc_callback_L():
    global count_L
    global robot_service
    if robot_service.target_speed_L > 0:
        count_L += 1
    else:
        count_L -= 1
    
def drive():
    global count_R
    global count_L
    global prev_count_R
    global prev_count_L
    global err_I_R
    global err_I_L
    global err_prev_R
    global err_prev_L
    global robot_service
    
    if robot_service.target_speed_R > -0.01 and robot_service.target_speed_R < 0.01:
        MOT_R_1.value = 0
        MOT_R_2.value = 0
        init_variables_R()
    else:
        speed_R = (count_R - prev_count_R)/40/DURATION
        err_P = robot_service.target_speed_R - speed_R
        print(err_P)
        err_I_R += err_P * DURATION
        err_D = (err_P - err_prev_R)/DURATION
        duty_R = Kp * err_P + Ki * err_I_R + Kd * err_D
        if duty_R > 0:
            if duty_R > 100.0:
                duty_R = 100.0
            MOT_R_1.value = duty_R
            MOT_R_2.value = 0
        else:
            if duty_R < -100.0:
                duty_R = -100.0
            MOT_R_1.value = 0
            MOT_R_2.value = -duty_R
        prev_count_R = count_R
        err_prev_R = err_P
    
    if robot_service.target_speed_L > -0.01 and robot_service.target_speed_L < 0.01:
        MOT_L_1.value = 0
        MOT_L_2.value = 0
        init_variables_L()
    else:
        speed_L = (count_L - prev_count_L)/40/DURATION
        err_P = robot_service.target_speed_L - speed_L
        err_I_L += err_P * DURATION
        err_D = (err_P - err_prev_L)/DURATION
        duty_L = Kp * err_P + Ki * err_I_L + Kd * err_D
        if duty_L > 0:
            if duty_L > 100.0:
                duty_L = 100.0
            MOT_L_1.value = duty_L
            MOT_L_2.value = 0
        else:
            if duty_L < -100.0:
                duty_L = -100.0
            MOT_L_1.value = 0
            MOT_L_2.value = -duty_L
        prev_count_L = count_L
        err_prev_L = err_P
    
    t = threading.Timer(DURATION, drive)
    t.start()

def init_variables_R():
    global count_R
    global prev_count_R
    global err_prev_R
    global err_I_R
    count_R = 0
    prev_count_R = 0
    err_prev_R = 0
    err_I_R = 0
    
def init_variables_L():
    global count_L
    global prev_count_L
    global err_prev_L
    global err_I_L
    count_L = 0
    prev_count_L = 0
    err_prev_L = 0
    err_I_L = 0
    
# encoder settings
ENC_R = Button(10, pull_up=True)
ENC_L = Button(2, pull_up=True)
count_R = 0
count_L = 0
ENC_R.when_pressed = enc_callback_R
ENC_R.when_released = enc_callback_R
ENC_L.when_pressed = enc_callback_L
ENC_L.when_released = enc_callback_L

# motor settings
MOT_R_1 = PWMOutputDevice(pin=23, frequency=60)
MOT_R_2 = PWMOutputDevice(pin=22, frequency=60)
MOT_L_1 = PWMOutputDevice(pin=18, frequency=60)
MOT_L_2 = PWMOutputDevice(pin=17, frequency=60)

DURATION = 0.1
prev_count_R = 0
prev_count_L = 0
err_prev_R = 0
err_prev_L = 0
err_I_R = 0
err_I_L = 0
Kp = 20
Ki = 100
Kd = 0.1

robot_service = None

def main(args=None):
    global robot_service
    
    MOT_R_1.value = 0
    MOT_R_2.value = 0
    MOT_L_1.value = 0
    MOT_L_2.value = 0
    
    rclpy.init(args=args)
    robot_service = RobotService()
    drive()
    rclpy.spin(robot_service)
        
    robot_service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()