from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS, cross_origin
import requests


app = Flask(__name__)
app.secret_key = 'random secret key!'
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
@app.route("/index.html")
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    return render_template('index.html', forwarded=ip)

@app.route("/ip/location")
@cross_origin()
def ip_location():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    r = requests.get(url='http://ip-api.com/json/' + ip +
                     '?fields=country,regionName,city,isp', timeout=60)
    response = app.response_class(
        response=r.text,
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/ip/location/<ip>")
@cross_origin()
def ip_locationWithIp(ip):
    r = requests.get(url='http://ip-api.com/json/' + ip +
                     '?fields=country,regionName,city,isp', timeout=60)
    response = app.response_class(
        response=r.text,
        status=200,
        mimetype='application/json'
    )
    return response


@socketio.on('join')
def join(message):
    username = message['username']
    room = message['room']
    join_room(room)
    print('RoomEvent: {} has joined the room {}\n'.format(username, room))
    emit('ready', {username: username}, to=room, skip_sid=request.sid)


@socketio.on('data')
def transfer_data(message):
    username = message['username']
    room = message['room']
    data = message['data']
    print('DataEvent: {} has sent the data:\n {}\n'.format(username, data))
    emit('data', data, to=room, skip_sid=request.sid)


@socketio.on_error_default
def default_error_handler(e):
    print("Error: {}".format(e))
    socketio.stop()


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
