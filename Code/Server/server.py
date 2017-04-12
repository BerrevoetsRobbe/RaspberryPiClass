import argparse
import logging
import os

from tornado.gen import coroutine
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, StaticFileHandler, url, asynchronous
from multiprocessing.pool import ThreadPool

from Actuators.BaseActuators.Camera import Camera

IFace = None
workers = ThreadPool(2)
clients = set()
names = {}
positions = {}
orientations = {}
debug = 0


class Server(object):

    def __init__(self, port):
        self.port = port
        self.application = App()

    def start_server(self):
        http_server = HTTPServer(self.application)
        http_server.listen(self.port)
        logging.info('Webserver starting')
        IOLoop.current().start()

    def cleanup(self):
        logging.info('Cleaning up %s' % self.__class__)
        logging.info('Webserver stopping')
        IOLoop.current().stop()


class App(Application):

    def __init__(self):
        handlers = [
            url(r"/", MainHandler),
            url(r'/stream.mjpeg', MJPEGHandler)
        ]
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "www"),
            "template_path": os.path.join(os.path.dirname(__file__), "www")
        }
        Application.__init__(self, handlers, **settings)


class MainHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        self.render("index.html")


class MJPEGHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    @asynchronous
    @coroutine
    def get(self):
        loop = IOLoop.current()
        self.set_status(200)
        self.set_header('Content-type', 'multipart/x-mixed-replace; boundary=--boundary')
        while True:
            image = Camera.get_instance().get_last_image_jpg()
            if image is not None:
                self.write('--boundary')
                self.write('\r\n')
                self.write('Content-length: %s\r\n' % str(image.size))
                self.write('Content-type: image/jpeg\r\n')
                self.write('\r\n')
                self.write(str(image.data))
                yield Task(self.flush)
                yield Task(loop.add_timeout, loop.time() + 0.1)
            else:
                logging.warning('Skipping frame')
                yield Task(loop.add_timeout, loop.time() + 0.1)


def setup():
    log_level = 'WARNING'
    parser = argparse.ArgumentParser(description='starts the server')
    parser.add_argument('-l', '--log', help='indicates the level of logging (INFO, DEBUG)')
    args = parser.parse_args()
    if args.log:
        log_level = args.log

    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logging.basicConfig(level=numeric_level,
                        format='%(asctime)s :: [%(levelname)s] :: %(filename)s :: %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')

if __name__ == '__main__':
    setup()
    logging.info('Starting...')
    server = Server(8080)
    try:
        server.start_server()
    except (KeyboardInterrupt, SystemExit):
        server.cleanup()
        logging.info('Closing...')