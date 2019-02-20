import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

rows = [17,27,22,5,6,13]
cols = [19,26,14,15,23,24]
keys = [
        ["a1","a2","a3","a4","a5","a6"],
        ["b1","b2","b3","b4","b5","b6"],
        ["c1","c2","c3","c4","c5","c6"],
        ["d1","d2","d3","d4","d5","d6"],
        ["e1","e2","e3","e4","e5","e6"],
        ["f1","f2","f3","f4","f5","f6"]
        ]

for row_pin in rows:
    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for col_pin in cols:
    GPIO.setup(col_pin, GPIO.OUT)

def get_key():
    key = 0
    for col_num, col_pin in enumerate(cols):
        GPIO.output(col_pin, 1)
        for row_num, row_pin in enumerate(rows):
            if GPIO.input(row_pin):
               key = keys[row_num][col_num]
        GPIO.output(col_pin, 0)
    return key

while True:
    key = get_key()
    if key :
        print(key)
    time.sleep(0.2)