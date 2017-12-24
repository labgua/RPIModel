
import RPi.GPIO as GPIO
import RPIWebSocket

class RPIDigitalInput:

	pinValues = {}
	#observer = RPIWebSocket

	def setInput(self, pin) :
		self.pinValues[pin] = 0
		GPIO.setup(pin, GPIO.IN)
		GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.updateModel)

	def removeInput(self, pin) :
		self.pinValues.pop(pin, None)
		GPIO.remove_event_detect(pin)
		GPIO.cleanup(pin)

	def isset(self, pin) :
		return self.pinValues.has_key(pin)

	def getValue(self, pin) :
		return self.pinValues.get(pin, None)


	def getModel(self) :
		return self.pinValues


	def cleanup(self) :
		for pin in self.pinValues.keys() :
			self.removeInput(pin)

	def setObserver(self, observer) :
		self.observer = observer


	def updateModel(self, channel) :
		value = GPIO.input(channel)
		self.pinValues[channel] = value
		RPIWebSocket.RPIWebSocket.notify(channel, value)
		#if observer != None :
		#	observer.notify(channel)
		#print("UPDATE from {0} - value:{1}".format(channel, value))


