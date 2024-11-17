print("servo")
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) #GPIO.BOARD for servo, GPIO.BCM for vibration
GPIO.setup(11,GPIO.OUT) #Pin 11 for Servo, Pin 27 for vibration, change all to match
servo1=GPIO.PWM(11,50) #11 is pin, 50 is 50Hz pulse
#pulse off, no rotation
print("servo off")
servo1.start(0)
#def vibrate():
	#GPIO.output(27,GPIO.HIGH)
	#time.sleep(1)
	#GPIO.output(27,GPIO.LOW)
	#function not needed for servo
def move(bend):
	print(bend)
	#pulse on, rotate servo to bend finger
	print("servo on")
	if bend:
		duty = 2.2
		#vibrate()
		servo1.ChangeDutyCycle(duty)

		time.sleep(0.2)
		servo1.ChangeDutyCycle(0)
		#degrees of rotation 2-12 = 0-180degrees			servo1.ChangeDutyCycle(duty)
		print("finger bending")
	else:
		#rotate servo back, straighten finger
		servo1.ChangeDutyCycle(12)
		time.sleep(0.5)
		servo1.ChangeDutyCycle(0)
		print("finger straightening")

if __name__ == "__main__":
	try:
		while True:
			bend = eval(input('Bend finger True or False:'))
			move(bend)
	finally:
		#turn off
		servo1.stop()
		GPIO.cleanup()
		print("Off")
