#!/usr/bin/env python

from bottle import static_file, route, run
from threading import Thread

import asyncio
import websockets

import json
from bot import Bot

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

# Get hash from command-data pair
@asyncio.coroutine
def get_hash(command, data):
  param = {"command": command,
           "data": data}
  bot = Bot(param)
  bot.generate_hash()
  return bot.hash

# Connection List
connected = set()

# Generate JSON data from message
# Then send data to all connected client
@asyncio.coroutine
def send_message(message):
  global connected

  jsoncontents = {"data": message}
  jsondata = json.dumps(jsoncontents)
  yield from asyncio.wait([ws.send(jsondata) for ws in connected])

@asyncio.coroutine
def receive_send(websocket, path):
  # Please write your code here

  # Connection List
  global connected

  try:
    # Add connection to list
    connected.add(websocket)

    # Loop until connection close or Ctrl-C
    while True:
      print("Receiving ...")
      
      # Receive message
      message = yield from websocket.recv()

      # Echo message
      yield from send_message(message)

      # Send hash when receive three words starts with "bot"
      wordlist = message.split(" ")
      if ((len(wordlist) == 3) and (wordlist[0] == "bot")):
        hash = yield from get_hash(wordlist[1], wordlist[2])
        yield from send_message(hash)

      # Sleep 1 second
      yield from asyncio.sleep(1)

  except websockets.ConnectionClosed:
    print('disconnected')

  except KeyboardInterrupt:
    print('\nCtrl-C (SIGINT) caught. Exiting...')  

  finally:
    # Remove connection from list
    connected.remove(websocket)

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
