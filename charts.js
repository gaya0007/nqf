var http = require('http');
var fs = require('fs');
var io = require('socket.io');
var url = require('url');
var  net = require('net');
var spawn = require('child_process').spawn
//server to receive OHLC data 
var STREAM_PORT = 9000


//var stream = net.createServer();
//stream.listen(STREAM_PORT);


var server = http.createServer(function(req, res){	
	var path = url.parse(req.url).pathname;
	switch(path)
	{
		case '/':
			res.writeHead(200, {'Content-Type': 'text/plain'});
			res.end('helooo');
			break;
		case '/charts.html':
			console.log(__dirname + path);
			fs.readFile(__dirname + path, function(error, data){
				if(error){
					res.writeHead(404);
					res.write("oops this doesn't exist - 404");
					res.end();
				}
				else
				{
					res.writeHead(200, {"Content-Type": "text/html"});
					res.write(data, "utf8");
					res.end();					
				}
			});
		break;
		default:
		
			res.writeHead(404);
			res.write("oops this doesn't exist - 404");
			res.end();
		break;		
	}
});

server.listen(8080);

var listner = io.listen(server);
//
listner.on('connection', function(socket){
    socket.on('start_bt', function (msg) {
        console.log('Message Received: ', msg);
	});
});



//server.on('connection', function(sock) {
//	
//	console.log('CONNECTED: ' + sock.remoteAddress +':'+ sock.remotePort);
//	// other stuff is the same from here
//	// Add a 'data' event handler to this instance of socket
//	sock.on('start_bt', function(data) {
//		console.log('DATA : ' + data);		
//	});
//	
//	// Add a 'close' event handler to this instance of socket
//	sock.on('close', function(data) {
//		console.log('CLOSED: ' + sock.remoteAddress +' '+ sock.remotePort);
//	})	
//});
//



