import pigpio                     	#pigpioを使う
from time import sleep              	#sleepを使う

MOT_R_1 = 18                       	#GPIO18をMOT_R_1と命名
MOT_R_2 = 17                       	#GPIO17をMOT_R_2と命名
MOT_L_1 = 23                       	#GPIO23をMOT_L_1と命名
MOT_L_2 = 22                       	#GPIO22をMOT_L_2と命名
pi = pigpio.pi()
pi.set_mode(MOT_R_1, pigpio.OUTPUT) 	#MOT_R_1を出力指定
pi.set_mode(MOT_R_2, pigpio.OUTPUT) 	#MOT_R_2を出力指定
pi.set_mode(MOT_L_1, pigpio.OUTPUT) 	#MOT_L_1を出力指定
pi.set_mode(MOT_L_2, pigpio.OUTPUT) 	#MOT_L_2を出力指定
pi.set_PWM_frequency(MOT_R_1, 60)   	#MOT_R_1に60HzでPWM出力
pi.set_PWM_frequency(MOT_R_2, 60)   	#MOT_R_2に60HzでPWM出力
pi.set_PWM_frequency(MOT_L_1, 60)   	#MOT_L_1に60HzでPWM出力
pi.set_PWM_frequency(MOT_L_2, 60)   	#MOT_L_2に60HzでPWM出力
pi.set_PWM_range(MOT_R_1, 100)      	#デューティのレンジ設定
pi.set_PWM_range(MOT_R_2, 100)
pi.set_PWM_range(MOT_L_1, 100)
pi.set_PWM_range(MOT_L_2, 100)
pi.set_PWM_dutycycle(MOT_R_1, 50)   	#MOT_R_1:50/100
pi.set_PWM_dutycycle(MOT_R_2, 0)    	#MOT_R_2:50/0
pi.set_PWM_dutycycle(MOT_L_1, 50)   	#MOT_L_1:50/100
pi.set_PWM_dutycycle(MOT_L_2, 0)    	#MOT_L_2:50/0

sleep(5)                             	#5秒待つ
pi.set_PWM_dutycycle(MOT_R_1, 0)   	#MOT_R_1:0/100
pi.set_PWM_dutycycle(MOT_R_2, 0)    	#MOT_R_2:0/100
pi.set_PWM_dutycycle(MOT_L_1, 0)   	#MOT_L_1:0/100
pi.set_PWM_dutycycle(MOT_L_2, 0)    	#MOT_L_2:0/100
pi.stop()
