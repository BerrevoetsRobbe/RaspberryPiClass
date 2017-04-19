import argparse
import logging
import os

from time import sleep
from threading import Thread
from tornado.gen import coroutine, Task
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, url, asynchronous

from Actuators.BaseActuators.Camera import Camera


class Server(Thread):

    def __init__(self, port):
        super(Server, self).__init__()
        self.__exit_flag = False
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

    def stop(self):
        logging.info("Stopping HTTPServer")
        self.__exit_flag = True

    def run(self):
        logging.info("Starting HTPPServer")
        self.start_server()


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
        logging.info("Get image of boef")
        loop = IOLoop.current()
        self.set_status(200)
        self.set_header('Content-type', 'multipart/x-mixed-replace; boundary=--boundary')
        last_image = None
        _try = 0
        while True:
            if Camera.get_instance():
                image = Camera.get_instance().get_last_image_jpg()
                if image is not None and image != last_image and _try < 2:
                    _try+=1
                    if _try > 1:
                        _try = 0
                        last_image = image
                    with open(image, 'rb') as f:
                        logging.info("Loading image {image}".format(image=image))
                        data = f.read()
                        self.write('--boundary')
                        self.write('\r\n')
                        self.write('Content-length: %s\r\n' % str(len(data)))
                        self.write('Content-type: image/jpeg\r\n')
                        self.write('\r\n')
                        self.write(str(data))
                    yield Task(self.flush)
                    yield Task(loop.add_timeout, loop.time() + 1)
                else:
                    yield Task(loop.add_timeout, loop.time() + 1)
                    pass


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