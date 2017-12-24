
import RPi.GPIO as GPIO

class RPIPWM:

	freq = 500
	pinPWM = {}

	def setPWM(self, pin, value) :
		if self.isset(pin) :
			p = self.pinPWM[pin]['ref']
		else :
			GPIO.setup(pin, GPIO.OUT)
			p = GPIO.PWM(pin, self.freq)
		
		p.start(value)
		self.pinPWM[pin] = {
			'ref' : p,
			'value' : value
		}

	def removePWM(self, pin) :
		entry = self.pinPWM.get(pin, None)
		if entry != None :
			entry['ref'].stop()
			self.pinPWM.pop(pin, None)
			GPIO.cleanup(pin)

	def isset(self, pin) :
		return self.pinPWM.has_key(pin)

	def getValue(self, pin) :
		entry = self.pinPWM.get(pin, None)
		if entry != None :
			return entry['value']
		else :
			return None


	def getModel(self) :
		outModel = {}
		for pin in self.pinPWM.keys() :
			outModel[pin] = self.pinPWM[pin]['value']

		return outModel


	def cleanup(self) :
		for pin in self.pinPWM.keys() :
			self.removePWM(pin)