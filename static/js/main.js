
/////////////// GESTIONE COMUNICAZIONE WEBSOCKET ///////////////

var ws;

function init(){
	var url = document.getElementById('url').value;
	ws = new WebSocket(url);
	
	ws.onopen = function() {
	   console.log("Connected!");
	};
	ws.onmessage = function (evt) {

		var msg = JSON.parse(evt.data);
		console.log(msg);
		///wslog(msg);

		// caso init_state
		if( msg['input'] && msg['output'] ){
			inputPins = Object.keys(msg['input']);
			outputPins = Object.keys(msg['output']);
			pwmPins = Object.keys(msg['pwm'])

			for( i in inputPins ){
				pin = inputPins[i];
				updateDigital(pin, msg['input'][pin], "INPUT");
			}
			for( j in outputPins ){
				pin = outputPins[j];
				updateDigital(pin, msg['output'][pin], "OUTPUT");
			}
			for( k in pwmPins ){
				pin = pwmPins[k];
				updateAnalog(pin, msg['pwm'][pin], "PWM");
			}

		}

		// caso update
		else{

			pin = msg['pin'];
			value = msg['value'];
			mode = msg['mode'];

			if( mode == "PWM" )
				updateAnalog(pin, value, mode);
			else
				updateDigital(pin, value, mode);

		}

	};			
}

function send(msg){
	ws.send( JSON.stringify(msg) );
}

function wslog(msg, txt = null){
	ref = document.querySelector('.rpiws_log > textarea');

	d = new Date();
	t = d.getTime();

	line = "";
	line += t + " ";
	if( txt != null ) line += txt + " ";
	line += JSON.stringify(msg);
	line += "\n";


	ref.value += line;
}

////////////////////////////////////////////////////////////////////

////////////////// CALLBACK AGGIORNAMENTO PAGINA ///////////////////

function updateDigital(pin, status, mode){

	var ref = document.querySelector('[pin="'+ pin +'"]');
	ref.setAttribute("type", "button");

	if(status == 1) status = "ON";
	else if(status == 0 || status == null) status = "OFF";
	ref.setAttribute("status", status);

	if(mode != null){
		ref.setAttribute("mode", mode);
		if( mode == "INPUT" ) ref.value = "IN";
		else if( mode == "OUTPUT" ) ref.value = "OUT";
		else if( mode == "PWM" ){
			ref.setAttribute("type", "range");
			ref.value = status;
		}
	}
}

function updateAnalog(pin, value, mode){
	ref = document.querySelector('[pin="'+ pin +'"]');
	ref.setAttribute("type", "range");
	ref.setAttribute("mode", mode);
	ref.removeAttribute("status");
	ref.value = value;
}

///////////////////////////////////////////////////////////////////////




/////////////// LISTENER INTERAZIONE INPUT DELLA PAGINA ///////////////

function updateModePin(){
	pin = document.querySelector(".rpi_settings .pin").value;
	mode = document.querySelector(".rpi_settings .mode").value;

	msg = new Object();
	msg.pin = pin;
	msg.mode = mode;

	if( mode == "OUTPUT"  )
		msg.value = "OFF";
	else if( mode == "PWM" )
		msg.value = 100

	send(msg);
}



function toggleChange(ref){

	mode = ref.getAttribute("mode");

	if( mode == "INPUT" )
		return;

	var msg = new Object();
	var pin = ref.getAttribute("pin");
	msg["pin"] = pin;
	msg['mode'] = mode;


	if( mode == "OUTPUT" ){
		var status = ref.getAttribute("status");

		if( status == "ON"){
			msg["value"] = "OFF"
		}
		else if( status == "OFF" || status == "UNKNOWN" ){
			msg["value"] = "ON";
		}
	}

	else if( mode == "PWM" ){
		msg['value'] = ref.value;
	}

	send(msg);
}

