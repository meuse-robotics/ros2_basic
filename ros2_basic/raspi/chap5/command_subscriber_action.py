import rclpy
from rclpy.node import Node
from gpiozero import Button
from gpiozero import PWMOutputDevice
import threading

from geometry_msgs.msg import Twist


class CommandSubscriberAction(Node):
    target_speed_R = 0.0
    target_speed_L = 0.0
    def __init__(self):
        super().__init__('command_subscriber_action')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
                
    def listener_callback(self, Twist):
        self.get_logger().info(f'並進速度={Twist.linear.x}角速度={Twist.angular.z}')
        self.target_speed_R = Twist.linear.x + Twist.angular.z
        self.target_speed_L = Twist.linear.x - Twist.angular.z
        
def enc_callback_R():
    global count_R
    global command_subscriber_action
    if command_subscriber_action.target_speed_R > 0:
        count_R += 1
    else:
        count_R -= 1
    
def enc_callback_L():
    global count_L
    global command_subscriber_action
    if command_subscriber_action.target_speed_L > 0:
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
    global command_subscriber_action
    
    if command_subscriber_action.target_speed_R > -0.01 and command_subscriber_action.target_speed_R < 0.01:
        MOT_R_1.value = 0
        MOT_R_2.value = 0
        init_variables_R()
    else:
        speed_R = (count_R - prev_count_R)/40/DURATION
        err_P = command_subscriber_action.target_speed_R - speed_R
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
    
    if command_subscriber_action.target_speed_L > -0.01 and command_subscriber_action.target_speed_L < 0.01:
        MOT_L_1.value = 0
        MOT_L_2.value = 0
        init_variables_L()
    else:
        speed_L = (count_L - prev_count_L)/40/DURATION
        err_P = command_subscriber_action.target_speed_L - speed_L
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

command_subscriber_action = None

def main(args=None):
    global command_subscriber_action
    
    MOT_R_1.value = 0
    MOT_R_2.value = 0
    MOT_L_1.value = 0
    MOT_L_2.value = 0
    
    rclpy.init(args=args)
    command_subscriber_action = CommandSubscriberAction()
    drive()
    rclpy.spin(command_subscriber_action)
        
    command_subscriber_action.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()