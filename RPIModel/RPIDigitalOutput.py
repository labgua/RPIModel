
import RPi.GPIO as GPIO

class RPIDigitalOutput:

	pinValues = {}

	def setOutput(self, pin, value) :
		self.pinValues[pin] = value
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, value)

	def removeOutput(self, pin) :
		self.pinValues.pop(pin, None)
		GPIO.cleanup(pin)

	def isset(self, pin) :
		return self.pinValues.has_key(pin)

	def getValue(self, pin) :
		return self.pinValues.get(pin, None)


	def getModel(self) :
		return self.pinValues


	def cleanup(self) :
		for pin in self.pinValues.keys() :
			self.removeOutput(pin)