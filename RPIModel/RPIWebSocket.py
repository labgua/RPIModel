# coding=utf-8

import tornado.websocket

from RPIModel import RPIModel

from pprint import pprint
import json
        

""" 
RPIWebSocket
- Questo è un socket che gestisce messaggi di tipo JSON
- Sostanzialmente su di questo canale si scamabiano due tipi di messaggi
  che sono UPDATE. A seconda del mittene e ricevente assumono significati
  differenti.

- Un UPDATE dal client verso il RPI è un comando che può avere una funzione
  di settaggio del pin oppure di aggiornamento di stato di un pin
- Un UPDATE dal RPI ai client è da considerarsi un aggiornamento di stato
  che segnala un cambiamento operativo (digital, analog, input, output) del
  pin, oppure del valore associato    
"""
class RPIWebSocket(tornado.websocket.WebSocketHandler):

    clients = []
    rpi = RPIModel()
    ##rpi.setObserver(RPIWebSocket)

    #def __init__(self, application, request, **kwargs):
    #    super(RPIWebSocket, self).__init__(application, request, **kwargs)
    #    self.rpi.setObserver(self)




    def check_origin(self, origin):
        return True

    def open(self):
        RPIWebSocket.clients.append(self)
        print("WebSocket opened")

        init_state = RPIWebSocket.rpi.getInitState()
        self.write_message(init_state)


    def on_message(self, message):
    	print("recived: " + message)

        msg = json.loads(message)
        pprint(msg)

        pin = int(msg['pin'])
        value = msg.get('value', None)
        mode = msg.get('mode', None)

        if value != None :
            if value == "ON" :
                value = 1
            elif value == "OFF" :
                value = 0
            else :
                value = float(value)

        if mode == "INPUT" :
            RPIWebSocket.rpi.setInput(pin)

        elif mode == "PWM" :
            RPIWebSocket.rpi.setPWM(pin, value)

        elif mode == "OUTPUT" or mode == None :
            RPIWebSocket.rpi.setOutput(pin, value)


        # Segnala a tutti i client il cambiamento
        self.publishEvent(msg)



    def on_close(self):
    	RPIWebSocket.clients.remove(self)
        print("WebSocket closed")





    @staticmethod
    def notify(pin, value) :
        #print("UPDATE in WebSocket : input pin {0}".format(pin))
        msg = {}
        msg["pin"] = pin
        msg["mode"] = "INPUT"
        msg["value"] = value

        for c in RPIWebSocket.clients:
            c.write_message(msg)







    """ informa gli altri dell'evento scatenato da un COMMAND
        - evt : il messaggio di tipo UPDATE da spedire a tutti i client connessi
    """
    def publishEvent(self, evt):
        for c in RPIWebSocket.clients:
            c.write_message(evt)
