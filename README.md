# RPIModel

## Introduction

This is a simple abstraction of remote control for GPIO RPI.
There is a WebSocket Server that runs on the RPI accessible from any client that support the [WebSocket standard](https://tools.ietf.org/html/rfc6455) known by many modern technologies

The architecture is centralized in the RPI; it receives all messages from the client, updates own status and tells to the remaining connected nodes the new state updated.

RPIModel implements a transmission protocol message-based, where there are two kind of message, *setup* and *update* : the *setup message* are used to set a mode pin and the *update message* are used to update the status of a pin.

For example this is a *setup message* that sets the pin 12 as OUTPUT

```json
{
	'pin' : 12,
	'mode' : 'OUTPUT'
}
``` 

And the next message is used as *update message* :

```json
{
	'pin' : 12,
	'mode' : 'OUTPUT',
	'value' : 'ON'
}
```


## Architecture

### Server

The server architecture is implemented with [Tornado Web Server](http://www.tornadoweb.org/en/stable/), a python implementation of networking library that works on RaspberryPI.
The server class 'RPIWebSocket' extends a 'WebSocketHandler' that use the wrapper-model 'RPIModel' class.
This is an important class that save the state of the ports which is not normally stored by the [RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/) library.


To start the server run the folowing command :
```bash
$ sudo python ws_server.py
```

If there aren't problem you can see the message 'WEBSOCKET RPI!!'.
The server is running on ip of the RaspberryPi on the port 8888.

Assuming that the ip of the RPi is 1.2.3.4, now you can go on the *1.2.3.4:8888/static* with a browser to use the javascript-client and interact with the RPI.

### Client

At the moment the client is a browser, but can be any other node that support the WebSocket protocol.
The browser (desktop or mobile) uses the javascript class 'WebSocket', a client appropriately instantiated via the user-interface.

Once you have visited the page *1.2.3.4:8888/static* :

 - insert the address of the websocket server
 - click on the 'connetti' button
 - send an *update message*, selecting the pin and the mode
 - if the pin is an *digital output*, you can click on the pin to toggle the state
 - else is the pin is an *digital input*, the color of the input change with the signal variation on it 