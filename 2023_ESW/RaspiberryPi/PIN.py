import RPi.GPIO as GPIO
import pigpio

GPIO.setwarnings(False)

FAN = 26
INSIDE_WATERSPRAY = 4
SERVO_MOTOR1 = 18
SERVO_MOTOR2 = 17
pi = pigpio.pi()

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN, GPIO.OUT)
GPIO.setup(INSIDE_WATERSPRAY, GPIO.OUT)
