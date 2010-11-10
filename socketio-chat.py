import tornado.web
from tornad_io import SocketIOHandler
from tornad_io import SocketIOServer

participants = set()

class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render("socketio-index.html")

class ChatHandler(SocketIOHandler):
    """Socket.IO handler"""

    def on_open(self, *args, **kwargs):
        self.send("Welcome!")
        participants.add(self)

    def on_message(self, message):
        for p in participants:
            p.send(message)

    def on_close(self):
        participants.remove(self)
        for p in participants:
            p.send("A user has left.")

chatRoute = ChatHandler.routes("socket.io/*")

application = tornado.web.Application(
    [(r"/", IndexHandler), chatRoute], 
    #enabled_protocols = ['websocket', 'flashsocket', 'xhr-multipart', 'xhr-polling'],
    enabled_protocols = ['websocket', 'flashsocket'],
    flash_policy_port = 8043,
    flash_policy_file = '/etc/lighttpd/flashpolicy.xml',
    socket_io_port = 8888
)

if __name__ == "__main__":
    socketio_server = SocketIOServer(application)