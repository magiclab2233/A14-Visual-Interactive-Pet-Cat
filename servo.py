#-*- coding:UTF-8 -*-
#本次舵机控制七彩灯采用的是自己定义的脉冲函数来
#产生pwm波形
import RPi.GPIO as GPIO
import time

#舵机引脚定义
ServoPin = 12

#定义一个脉冲函数，用来模拟方式产生pwm值
#时基脉冲为20ms，该脉冲高电平部分在0.5-
#2.5ms控制0-180度
def servo_pulse(myangle):
    pulsewidth = (myangle * 11) + 500
    GPIO.output(ServoPin, GPIO.HIGH)
    time.sleep(pulsewidth/1000000.0)
    GPIO.output(ServoPin, GPIO.LOW)
    time.sleep(20.0/1000-pulsewidth/1000000.0)
	
#舵机来回转动
def servo_control():
    #设置GPIO口为BCM编码方式
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ServoPin, GPIO.OUT)
    for pos in range(20):
        servo_pulse(pos)
    # time.sleep(0.5)
    for pos in reversed(range(20)):
        servo_pulse(pos)

def servo_off():
    GPIO.cleanup()

def servo_move_slow(cur_angle, target_angle, step=1, delay=0.02):
    if target_angle > cur_angle:
        angle_range = range(cur_angle, target_angle + 1, step)
    else:
        angle_range = range(cur_angle, target_angle - 1, -step)

    for ang in angle_range:
        servo_pulse(ang)
        time.sleep(delay)   # 控制“速度”：delay 越大，转越慢

    return target_angle

def servo_control_slow():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ServoPin, GPIO.OUT)
        current = 0
        current = servo_move_slow(current, 25, step=1, delay=0.05)  
        print("return")
        current = servo_move_slow(current, 0, step=1, delay=0.05)
    finally:
        GPIO.cleanup()
