// connect to websocket at localhost:3001
const socket = new WebSocket('ws://localhost:8000/ws');

// Path: backend/websockets.js
// send a message to the server
// receive
socket.onmessage = function(event) {
  console.log('Message from server ', event.data);
};

socket.send('Hello, server!');
