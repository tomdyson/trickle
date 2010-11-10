"""
Redis-backed pub/sub
"""
import tornado.httpserver
from tornado import websocket
import tornado.ioloop
import tornado.web
import redis
import logging
logging.getLogger().setLevel(logging.DEBUG)

STREAM_LENGTH = 5
listeners = []
red = redis.Redis()

def broadcast(msg):
    # update message stack, broadcast to connected clients
    red.lpush('messages', msg)
    red.ltrim('messages', 0, STREAM_LENGTH -1)
    for listener in listeners:    
        listener.write_message(msg)

class NewMsgHandler(tornado.web.RequestHandler):
    def get(self):
        messages = red.lrange('messages', 0, -1) or []
        messages.reverse()
        self.render("ws-index.html", messages=messages)

    def post(self):
        data = self.request.arguments['data'][0]
        broadcast(data)

class RealtimeHandler(websocket.WebSocketHandler):
    def open(self):
        listeners.append(self)

    def on_message(self, message):
        broadcast(message)

    def on_close(self):
        listeners.remove(self)
        
settings = {
    'auto_reload': True,
}

application = tornado.web.Application([
    (r'/', NewMsgHandler),
    (r'/realtime/', RealtimeHandler),
], **settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    logging.info('serving on http://127.0.0.1:8888/')
    tornado.ioloop.IOLoop.instance().start()