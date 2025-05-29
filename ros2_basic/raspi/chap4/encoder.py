from gpiozero import Button

def enc_callback_R(): #右側割り込み関数
    global count_R #グローバル変数count_Rを使う
    count_R += 1 #カウントアップ
    print('R= ' + str(count_R)) #画面出力

def enc_callback_L(): #左側割り込み関数
    global count_L #グローバル変数count_Lを使う
    count_L += 1 #カウントアップ
    print('L= ' + str(count_L)) #画面出力

# encoder settings
ENC_R = Button(10, pull_up=True) #GPIO10をENC_Rと命名
ENC_L = Button(2, pull_up=True) #GPIO2をENC_Lと命名
count_R = 0 #エッジカウント用
count_L = 0 #エッジカウント用
#ENC_Rの立ち上がり、立ち下がり両エッジ検出、コールバック関数指定
ENC_R.when_pressed = enc_callback_R
ENC_R.when_released = enc_callback_R
#ENC_Lの立ち上がり、立ち下がり両エッジ検出、コールバック関数指定
ENC_L.when_pressed = enc_callback_L
ENC_L.when_released = enc_callback_L

try:
    while True:
        pass
except KeyboardInterrupt:
    print("stop")
