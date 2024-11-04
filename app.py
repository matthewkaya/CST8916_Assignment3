from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import time

# Socket.IO instance initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Route for serving HTML page
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket connection event handler
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit("message", {"data": "Connected to WebSocket server!"})

# Background process for retrieving temperature data and emitting it to clients
def emit_temperature_data():
    while True:
        # Generate random temperature data
        temperature_data = {
            'timestamp': time.time(),
            'temperature': round(random.uniform(20.0, 30.0), 2),
            'location': 'MyHome'
        }
        # Emit the temperature data to the connected clients
        socketio.emit('temperature_data', temperature_data)
        # Wait for 5 seconds before sending the next data
        socketio.sleep(5)

# Run the Flask application with Socket.IO
if __name__ == '__main__':
    # Start the background task for emitting temperature data
    socketio.start_background_task(emit_temperature_data)
    socketio.run(app, debug=True)