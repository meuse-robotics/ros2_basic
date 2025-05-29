from gpiozero import PWMOutputDevice #RaspiのGPIOを使うためのライブラリ
from time import sleep # sleepを使う

MOT_R_1 = PWMOutputDevice(pin=23, frequency=60) #GPIO23 60HzでPWM
MOT_R_2 = PWMOutputDevice(pin=22, frequency=60) #GPIO22 60HzでPWM
MOT_L_1 = PWMOutputDevice(pin=18, frequency=60) #GPIO18 60HzでPWM
MOT_L_2 = PWMOutputDevice(pin=17, frequency=60) #GPIO17 60HzでPWM

MOT_R_1.value = 0.5 #duty50%でPWM出力
MOT_R_2.value = 0
MOT_L_1.value = 0.5 #duty50%でPWM出力
MOT_L_2.value = 0
sleep(5)
MOT_R_1.value = 0 #PWM出力停止
MOT_R_2.value = 0
MOT_L_1.value = 0 #PWM出力停止
MOT_L_2.value = 0
