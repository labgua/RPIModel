
from RPIDigitalInput import RPIDigitalInput
from RPIDigitalOutput import RPIDigitalOutput
from RPIPWM import RPIPWM

class RPIModel:

	def __init__(self) :
		self.input = RPIDigitalInput()
		self.output = RPIDigitalOutput()
		self.pwm = RPIPWM()


	# wrap di RPIDigitalOutput

	def setOutput(self, pin, value) :
		if self.input.isset(pin) :
			self.removeInput(pin)
		elif self.pwm.isset(pin) :
			self.removePWM(pin)
		
		self.output.setOutput(pin, value)

	def removeOutput(self, pin) :
		self.output.removeOutput(pin)

	def issetOutput(self, pin) :
		return self.output.isset(pin)

	def getValueOutput(self, pin) :
		return self.output.getValue(pin)



	# wrap di RPIDigitalInput

	def setInput(self, pin) :
		if self.output.isset(pin) :
			self.removeOutput(pin)
		elif self.pwm.isset(pin) :
			self.removePWM(pin)

		self.input.setInput(pin)

	def removeInput(self, pin) :
		self.input.removeInput(pin)

	def issetInput(self, pin) :
		return self.input.isset(pin)

	def getValueInput(self, pin) :
		return self.input.getValue(pin)

	def setObserver(self, observer) :
		self.input.setObserver(observer)



	# wrap di RPIPWM
	def setPWM(self, pin, value) :
		if self.output.isset(pin) :
			self.removeOutput(pin)
		elif self.input.isset(pin) :
			self.removeInput(pin)

		self.pwm.setPWM(pin, value)

	def removePWM(self, pin) :
		self.pwm.removePWM(pin)

	def issetPWM(self, pin) :
		return self.pwm.isset(pin)

	def getValuePWM(self, pin) :
		return self.pwm.getValue(pin)





	def getInitState(self) :
		init_state = {
			"input" : {},
			"output" : {},
			"pwm" : {}
		}


		in_state = self.input.getModel()
		out_state = self.output.getModel()
		pwm_state = self.pwm.getModel()

		for pin in in_state.keys() :
			init_state['input'][pin] = self.dval( in_state[pin] )

		for pin in out_state.keys() :
			init_state['output'][pin] = self.dval( out_state[pin] )

		for pin in pwm_state.keys() :
			init_state['pwm'][pin] = pwm_state[pin]


		return init_state 


	def cleanup(self) :
		self.input.cleanup()
		self.output.cleanup()
		self.pwm.cleanup()


	def dval(self, val) :
		if val == 0 : return "OFF"
		if val == 1 : return "ON"