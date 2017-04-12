var error = 0;
var map = [];
var sensor1Value = 1;
var sensor2Value = 1;
var debugTimer, scrollTimer, buttonTimer;

var ESC = 0;
var UP = 8;
var DOWN = 2;
var UPLEFT = 7;
var UPRIGHT = 9;
var DOWNLEFT = 1;
var DOWNRIGHT = 3;
var LEFT = 4;
var RIGHT = 6;
var STOP = 5;
var AUTO = 10;
var NAUTO = 11;

ws = new WebSocket('ws://192.134.3.1:8888/ws');

ws.onopen = function() {
	console.log('WebSocket Opened');
	$('#statusLabel').addClass('label-success');
	$('#statusLabel').removeClass('label-info');
	$('#statusLabel').removeClass('label-danger');
	$('#statusLabel').removeClass('label-warning');
	$('#statusLabel').text('Connected');
};

ws.onmessage = function (msg) {
	console.log(msg)
	var command = Math.floor(msg.data / 100);
	var data = msg.data % 100;
	if (command == 1) {
		sensor1Value = data;
		setSensor1();
	} else if (command == 2) {
		sensor2Value = data;
		setSensor2();
	} else if (command == 3) {
        enableSend();
    } else if (command == 4) {
        disableSend();
    } else if (command == 5) {
        enableAuto();
    } else if (command == 6) {
        enableManual();
    }
};

setSensor1 = function() {
	if (sensor1Value < 50) {
		$('#sensor1').removeClass('progress-bar-warning');
		$('#sensor1').removeClass('progress-bar-danger');
		$('#sensor1').addClass('progress-bar-success');
		$('#sensor1Label').removeClass('label-warning');
		$('#sensor1Label').removeClass('label-danger');
		$('#sensor1Label').addClass('label-success');
	} else if (50 <= sensor1Value && sensor1Value <= 75) {
		$('#sensor1').removeClass('progress-bar-success');
		$('#sensor1').removeClass('progress-bar-danger');
		$('#sensor1').addClass('progress-bar-warning');
		$('#sensor1Label').removeClass('label-success');
		$('#sensor1Label').removeClass('label-danger');
		$('#sensor1Label').addClass('label-warning');
	} else if (sensor1Value > 75) {
		$('#sensor1').removeClass('progress-bar-success');
		$('#sensor1').removeClass('progress-bar-warning');
		$('#sensor1').addClass('progress-bar-danger');
		$('#sensor1Label').removeClass('label-success');
		$('#sensor1Label').removeClass('label-warning');
		$('#sensor1Label').addClass('label-danger');
	}
	$('#sensor1').css('width', sensor1Value+'%').attr('aria-valuenow', sensor1Value);
	var distance = 100 - sensor1Value;
	$('#sensor1').text(distance + ' cm');
};

setSensor2 = function() {
	if (sensor2Value < 50) {
		$('#sensor2').removeClass('progress-bar-warning');
		$('#sensor2').removeClass('progress-bar-danger');
		$('#sensor2').addClass('progress-bar-success');
		$('#sensor2Label').removeClass('label-warning');
		$('#sensor2Label').removeClass('label-danger');
		$('#sensor2Label').addClass('label-success');
	} else if (50 <= sensor2Value && sensor2Value <= 75) {
		$('#sensor2').removeClass('progress-bar-success');
		$('#sensor2').removeClass('progress-bar-danger');
		$('#sensor2').addClass('progress-bar-warning');
		$('#sensor2Label').removeClass('label-success');
		$('#sensor2Label').removeClass('label-danger');
		$('#sensor2Label').addClass('label-warning');
	} else if (sensor2Value > 75) {
		$('#sensor2').removeClass('progress-bar-success');
		$('#sensor2').removeClass('progress-bar-warning');
		$('#sensor2').addClass('progress-bar-danger');
		$('#sensor2Label').removeClass('label-success');
		$('#sensor2Label').removeClass('label-warning');
		$('#sensor2Label').addClass('label-danger');
	}
	$('#sensor2').css('width', sensor2Value+'%').attr('aria-valuenow', sensor2Value);
	var distance = 100 - sensor2Value;
	$('#sensor2').text(distance + ' cm');
};

enableSend = function() {
    $('#textSendCommand').val('');
    //$('#escapeSend').attr("disabled", "disabled");
    $('#textSendCommand').removeAttr("disabled");
    $('#buttonSend').removeAttr("disabled");
};

disableSend = function() {
    $('#buttonSend').attr("disabled", "disabled");
    $('#textSendCommand').attr("disabled", "disabled");
    //$('#escapeSend').removeAttr("disabled");
};

enableAuto = function() {
	$('#buttonUp').attr("disabled", "disabled");
	$('#buttonDown').attr("disabled", "disabled");
	$('#buttonLeft').attr("disabled", "disabled");
	$('#buttonRight').attr("disabled", "disabled");
	$('#buttonStop').removeAttr("disabled");
    $('#buttonSend').removeAttr("disabled");
    $('#textSendCommand').removeAttr("disabled");
	clearInterval(buttonTimer);
};

enableManual = function() {
    $('#buttonUp').removeAttr("disabled");
	$('#buttonDown').removeAttr("disabled");
	$('#buttonLeft').removeAttr("disabled");
	$('#buttonRight').removeAttr("disabled");
	$('#buttonStop').attr("disabled", "disabled");
    $('#buttonSend').attr("disabled", "disabled");
    $('#textSendCommand').attr("disabled", "disabled");
	buttonTimer = setInterval(checkButtons, 100);
};

sendMessage = function(msg) {
	ws.send(msg);
};

ws.onclose = function(ev) {
	console.log('WebSocket Closed');
	if (!error) {	
		$('#statusLabel').removeClass('label-success');
		$('#statusLabel').removeClass('label-info');
		$('#statusLabel').addClass('label-danger');
		$('#statusLabel').removeClass('label-warning');
		$('#statusLabel').text('No Connection');
	}
};

ws.onerror = function(ev) {
	console.log('WebSocket Error');
	error = 1;
	$('#statusLabel').removeClass('label-success');
	$('#statusLabel').removeClass('label-info');
	$('#statusLabel').removeClass('label-danger');
	$('#statusLabel').addClass('label-warning');
	$('#statusLabel').text('Error Occurred');
	clearInterval(debugTimer);
	clearInterval(scrollTimer);
	clearInterval(buttonTimer);
};

moveForward = function() {
	sendMessage(UP);
};

moveForwardLeft = function() {
	sendMessage(UPLEFT);
};

moveForwardRight = function() {
	sendMessage(UPRIGHT);
};

moveBackward = function() {
	sendMessage(DOWN);
};

moveBackwardLeft = function() {
	sendMessage(DOWNLEFT);
};

moveBackwardRight = function() {
	sendMessage(DOWNRIGHT);
};

moveLeft = function() {
	sendMessage(LEFT);
};

moveRight = function() {
	sendMessage(RIGHT);
};

moveStop = function() {
	sendMessage(STOP);
};

escStop = function() {
	sendMessage(ESC);
};

sendCommand = function() {
	sendMessage($('#textSendCommand').val());
    //$('#textSendCommand').val('');
};

checkButtons = function() {
	if(map[90] && map[68] && map[81]) {
		moveForward();
	} else if(map[90] && map[68]) {
		moveForwardRight();
	} else if(map[90] && map[81]) {
		moveForwardLeft();
	} else if(map[83] && map[68]) {
		moveBackwardRight();
	} else if(map[83] && map[81]) {
		moveBackwardLeft();
	} else if(map[90]) {
		moveForward();
	} else if(map[83]) {
		moveBackward();
	} else if(map[68]) {
		moveRight();
	} else if(map[81]) {
		moveLeft();
	} else {
		//moveStop();
	}
};

download_to_textbox = function(url, el) {
	$.get(url, null, function (data) {
		el.val(data);
	}, 'text');
};

loadDebug = function() {
	reloadDebug();
	var textArea = document.getElementById('debugLog');
	var PositionTextAreaToBottom = function() {
		textArea.scrollTop = textArea.scrollHeight;
	};
	scrollTimer = setInterval(PositionTextAreaToBottom, 100);	
};

reloadDebug = function() {
	download_to_textbox('http://192.134.3.1/car/car.log?rand=' + Math.random(), $('#debugLog'));
};

reloadImage = function() {
	var myImageElement = document.getElementById('myMap');
	myImageElement.src = '../map2.jpg?rand=' + Math.random();
};

setDebugOnOff = function() {
	if($('#debugOn').hasClass('active')) {
		loadDebug();
		debugTimer = setInterval(reloadDebug, 500);
	} else if($('#debugOff').hasClass('active')) {
		clearInterval(debugTimer);
		clearInterval(scrollTimer);
	}
};

setControlOnOff = function() {
	if($('#controlAuto').hasClass('active')) {
		sendMessage(AUTO);
	} else if($('#controlMan').hasClass('active')) {
		sendMessage(NAUTO);
	}
};

$(document).ready(function(){
	$('.btn-toggle').click(function() {
		$(this).find('.btn').toggleClass('active');  
    
		if ($(this).find('.btn-primary').size()>0) {
			$(this).find('.btn').toggleClass('btn-primary');
		}
		/*
		if ($(this).find('.btn-danger').size()>0) {
			$(this).find('.btn').toggleClass('btn-danger');
		}
		if ($(this).find('.btn-success').size()>0) {
			$(this).find('.btn').toggleClass('btn-success');
		}
		if ($(this).find('.btn-info').size()>0) {
			$(this).find('.btn').toggleClass('btn-info');
		}
		*/
		$(this).find('.btn').toggleClass('btn-default');
		
		if($(this).attr('id') == 'debugToggle') {
			setDebugOnOff();
		} else if($(this).attr('id') == 'controlToggle') {
			setControlOnOff();
		}
	});
	/*
	$('#buttonUp').mousedown(function() {
		map[90] = true;
		moveForward();
	});
	
	$('#buttonUp').mouseup(function() {
		map[90] = false;
		moveStop();
	});
	
	$('#buttonDown').mousedown(function() {
		map[83] = true;
		moveBackward();
	});
	
	$('#buttonDown').mouseup(function() {
		map[83] = false;
		moveStop();
	});
	
	$('#buttonLeft').mousedown(function() {
		map[81] = true;
		moveLeft();
	});
	
	$('#buttonLeft').mouseup(function() {
		map[81] = false;
		moveStop();
	});
	
	$('#buttonRight').mousedown(function() {
		map[68] = true;
		moveRight();
	});
	
	$('#buttonRight').mouseup(function() {
		map[68] = false;
		moveStop();
	});
	
	$('#buttonStop').mousedown(escStop);
	
	$('#buttonStop').click(escStop);*/
	
	$('#buttonSend').click(sendCommand);
	
	/*$('#buttonUp').bind('touchstart', function() {
		map[90] = true;
		moveForward();
	});
	
	$('#buttonUp').bind('touchend', function() {
		map[90] = false;
		moveStop();
	});
	
	$('#buttonDown').bind('touchstart', function() {
		map[83] = true;
		moveBackward();
	});
	
	$('#buttonDown').bind('touchend', function() {
		map[83] = false;
		moveStop();
	});
	
	$('#buttonLeft').bind('touchstart', function() {
		map[81] = true;
		moveLeft();
	});
	
	$('#buttonLeft').bind('touchend', function() {
		map[81] = false;
		moveStop();
	});
	
	$('#buttonRight').bind('touchstart', function() {
		map[68] = true;
		moveRight();
	});
	
	$('#buttonRight').bind('touchend', function() {
		map[68] = false;
		moveStop();
	});*/
	
	onkeydown = onkeyup = function(e){
		e = e || event; // to deal with IE
		map[e.keyCode] = e.type == 'keydown';
		
		//console.log(e.keyCode + ' ' + e.type);
		switch(e.keyCode) {
			case 27:
				if(e.type == 'keydown'/* && $('#controlAuto').hasClass('active')*/) {
					/* $('#buttonStop').addClass('active');
					$('#buttonStop').focus(); */
					sendMessage(ESC);
				} /*else {
					$('#buttonStop').removeClass('active');
					$('#buttonStop').blur();
				}*/
				break;
			/*
			case 68:
				if(e.type == 'keydown' && $('#controlMan').hasClass('active')) {
					$('#buttonRight').addClass('active');
					$('#buttonRight').focus();
				} else if($('#controlMan').hasClass('active')) {
					$('#buttonRight').removeClass('active');
					$('#buttonRight').blur();
                    moveStop();
				}
				break;
			case 81:
				if(e.type == 'keydown' && $('#controlMan').hasClass('active')) {
					$('#buttonLeft').addClass('active');
					$('#buttonLeft').focus();
				} else if($('#controlMan').hasClass('active')) {
					$('#buttonLeft').removeClass('active');
					$('#buttonLeft').blur();
					moveStop();
				}
				break;
			case 83:
				if(e.type == 'keydown' && $('#controlMan').hasClass('active')) {
					$('#buttonDown').addClass('active');
					$('#buttonDown').focus();
				} else if($('#controlMan').hasClass('active')) {
					$('#buttonDown').removeClass('active');
					$('#buttonDown').blur();
					moveStop();
				}
				break;
			case 90:
				if(e.type == 'keydown' && $('#controlMan').hasClass('active')) {
					$('#buttonUp').addClass('active');
					$('#buttonUp').focus();
				} else if($('#controlMan').hasClass('active')) {
					$('#buttonUp').removeClass('active');
					$('#buttonUp').blur();
                    moveStop();
				}
				break;
			*/
		}
	}
	
	setSensor1();
	setSensor2();
	
	setDebugOnOff();
	setInterval(reloadImage, 1000);
	//setTimeout(setControlOnOff, 1000);
});
