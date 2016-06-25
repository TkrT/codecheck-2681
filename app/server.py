#!/usr/bin/env python

from bottle import static_file, route, run
from threading import Thread

import asyncio
import websockets

#serving index.html file on "http://localhost:9000"
def httpHandler():
  while True:
    @route('/')
    def index():
      static_file('index.css', root='./app')
      static_file('client.js', root='./app')
      return static_file("index.html", root='./app')

    @route('/<filename>')
    def server_static(filename):
      return static_file(filename, root='./app')    

    run(host='localhost', port=9000)


@asyncio.coroutine
def receive_send(websocket, path):
  # Please write your code here
  try:
    print("Receiving ...")
  except KeyboardInterrupt:
    print('\nCtrl-C (SIGINT) caught. Exiting...')  

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  start_server = websockets.serve(receive_send, '127.0.0.1', 3000)
  server = loop.run_until_complete(start_server)
  print('Listen')

  t = Thread(target=httpHandler)
  t.daemon = True
  t.start()

  try:
    loop.run_forever()
  finally:
    server.close()
    start_server.close()
    loop.close()
