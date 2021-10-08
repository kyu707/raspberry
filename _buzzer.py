import RPi.GPIO as GPIO
from time import sleep

#BUZZER_PIN  = 17
BUZZER_PIN  = 7
ON = 1
OFF = 0

scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]
#scale = [ 523, 587, 659, 698, 784, 880, 987, 1046 ]

#melodySize = 24;
melodyList = [4, 4, 5, 5, 4, 4, 2, 4, 4, 2, 2, 1, 4, 4, 5, 5, 4, 4, 2, 4, 2, 1, 2, 0]
noteDurations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 1,
                 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 1]

openDoorBeep = [2,0,4,7]
noteDurations1= [1,1,1,1]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = GPIO.PWM(BUZZER_PIN, 100)       # frequency = 100 Hz


def playBuzzer(melodyList, noteDurations):
    pwm.start(100)                        # duty cycle = 100
    pwm.ChangeDutyCycle(50)
#    pwm.ChangeDutyCycle(90)
    for i in range(len(melodyList)):
        pwm.ChangeFrequency(scale[melodyList[i]])
        sleep(noteDurations[i])
    pwm.stop()

def controlBuzzer(buzzerStatus):
    if(buzzerStatus):
        pwm.start(100)                        # duty cycle = 100
        pwm.ChangeDutyCycle(50)
#        pwm.ChangeDutyCycle(90)
        for i in range(len(melodyList)):
            pwm.ChangeFrequency(scale[melodyList[i]])
            sleep(noteDurations[i])
    else:
        pwm.stop()

def main():
    print("start buzzer program ...")
#    controlBuzzer(ON)
#    controlBuzzer(OFF)

#    playBuzzer(openDoorBeep, noteDurations1)
    playBuzzer(melodyList, noteDurations)
    pwm.stop()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
