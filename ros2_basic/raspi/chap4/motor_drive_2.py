import pigpio					#pigpioを使う

def enc_callback_R(gpio,level, tick): 	#右側割り込み関数
    global count_R				#グローバル変数count_Rを使う
    count_R += 1				#カウントアップ
    print('R= ' + str(count_R)) 		#画面出力

def enc_callback_L(gpio,level, tick):	#左側割り込み関数
    global count_L				#グローバル変数count_Lを使う
    count_L += 1				#カウントアップ
    print('L= ' + str(count_L))		#画面出力

pi = pigpio.pi()
# encoder settings
ENC_R = 10					#GPIO10をENC_Rと命名
ENC_L = 2					#GPIO10をENC_Rと命名
count_R = 0					#エッジカウント用
count_L = 0					#エッジカウント用
pi.set_mode(ENC_R, pigpio.INPUT) 		#ENC_Rを入力指定
pi.set_pull_up_down(ENC_R, pigpio.PUD_UP)	#プルアップ指定
pi.set_mode(ENC_L, pigpio.INPUT)		#ENC_Lを入力指定
pi.set_pull_up_down(ENC_L, pigpio.PUD_UP)	#プルアップ指定
#ENC_Rの立ち上がり、立ち下がり両エッジ検出、コールバック関数指定
cbR = pi.callback(ENC_R, pigpio.EITHER_EDGE, enc_callback_R)
#ENC_Lの立ち上がり、立ち下がり両エッジ検出、コールバック関数指定
cbR = pi.callback(ENC_L, pigpio.EITHER_EDGE, enc_callback_L)

try:
    while True:
        pass
except KeyboardInterrupt:
    pi.stop()
