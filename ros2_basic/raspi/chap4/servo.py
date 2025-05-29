from gpiozero import Button
from gpiozero import PWMOutputDevice
import threading

def enc_callback_R():
	global count_R
	count_R += 1

def enc_callback_L():
	global count_L
	count_L += 1

def drive(): #0.1秒ごとに実行
	global count_R
	global count_L
	global prev_count_R
	global prev_count_L
	global err_I_R
	global err_I_L
	global err_prev_R
	global err_prev_L

	speed_R = (count_R - prev_count_R)/40/DURATION
	err_P = target_speed_R - speed_R
	err_I_R += err_P * DURATION
	err_D = (err_P - err_prev_R)/DURATION
	duty_R = Kp * err_P + Ki * err_I_R + Kd * err_D
	if duty_R > 0:
		if duty_R > 100.0:
			duty_R = 100.0
		MOT_R_1.value = duty_R*0.01
		MOT_R_2.value = 0
	else:
		if duty_R < -100.0:
			duty_R = -100.0
		MOT_R_1.value = 0
		MOT_R_2.value = -duty_R*0.01
	prev_count_R = count_R
	err_prev_R = err_P

	speed_L = (count_L - prev_count_L)/40/DURATION
	err_P = target_speed_L - speed_L
	err_I_L += err_P * DURATION
	err_D = (err_P - err_prev_L)/DURATION
	duty_L = Kp * err_P + Ki * err_I_L + Kd * err_D
	if duty_L > 0:
		if duty_L > 100.0:
			duty_L = 100.0
		MOT_L_1.value = duty_L*0.01
		MOT_L_2.value = 0
	else:
		if duty_L < -100.0:
			duty_L = -100.0
		MOT_L_1.value = 0
		MOT_L_2.value = -duty_L*0.01
	prev_count_L = count_L
	err_prev_L = err_P

	t = threading.Timer(DURATION, drive) #DURATION秒後にdriveを実行
	t.start()

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

DURATION = 0.1 #制御周期（秒）
prev_count_R = 0 #前回カウント
prev_count_L = 0
err_prev_R = 0 #前回誤差
err_prev_L = 0
err_I_R = 0 #誤差の積分
err_I_L = 0
Kp = 20 #比例ゲイン
Ki = 100 #積分ゲイン
Kd = 0.1 #微分ゲイン
target_speed_R = 0.5 #目標速度
target_speed_L = 0.5

drive() #最初の呼び出し

try:
	while True:
		pass
except KeyboardInterrupt:
	MOT_R_1.value = 0
	MOT_R_2.value = 0
	MOT_L_1.value = 0
	MOT_L_2.value = 0
