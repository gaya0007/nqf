var http = require('http');
var fs = require('fs');
var io = require('socket.io');
var url = require('url');
var spawn = require('child_process').spawn
//server to recieve OHLC data 

var bt = spawn('python',["backtest.py"]);

bt.stdout.on('data',function(data){
	console.log("data :" + data);
});

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
					res.write("opps this doesn't exist - 404");
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

listner.on('connection', function (socket) {
    socket.on('start_bt', function (msg) {
        console.log('Message Received: ', msg);
		bt.stdin.write(JSON.stringify(msg));
		bt.stdin.end();
    });
});



