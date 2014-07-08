var net = require('net')

var server = net.createServer(function(sock) {
		sock.write("Hello\r\n");
		//console.log(sock);
		sock.pipe(sock);
		sock.on('data',function(data) {
			console.log(data);
			console.log(data.toString())
		});
});

server.listen(9999,'127.0.0.1');

server.on('data', function(data) {
	console.log('Received: ' + data);
});