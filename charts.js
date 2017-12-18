//var http = require('http');
//var fs = require('fs');
var net = require('net');

var HOST = '127.0.0.1';
var PORT = 6969;

var spawn = require("child_process").spawn;


//http.createServer(function(req, res){
//	
//	fs.readFile('index.html',function(err,data){
//		res.writeHead(200, {'Content-Type': 'text/plain'});
//		res.write(data);
//		res.end();
//	});
//}).listen(8080);

//server to recieve OHLC data 
var server = net.createServer();
server.listen(PORT);
console.log('Server listening on ' + server.address().address +':'+ server.address().port);
server.on('connection', function(sock) {
    
    console.log('CONNECTED: ' + sock.remoteAddress +':'+ sock.remotePort);
    // other stuff is the same from here
    // Add a 'data' event handler to this instance of socket
    sock.on('data', function(data) {
        
        console.log('DATA ' + sock.remoteAddress + ': ' + data);        
    });
    
    // Add a 'close' event handler to this instance of socket
    sock.on('close', function(data) {
        console.log('CLOSED: ' + sock.remoteAddress +' '+ sock.remotePort);
    })    
});


var process = spawn('python',["./main.py", "05/11/2017", "05/11/2017"]);

