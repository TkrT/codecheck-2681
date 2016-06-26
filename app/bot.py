#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Bot():
  # Please write your code here.

  # Get value from parameter and Initialize
  def __init__(self, param):
    self.command = param["command"]
    self.data = param["data"]
    self.hash = ""

  # Generate hash from command and data pair
  def generate_hash(self):
    try:
      commandASCII = self.string_to_ascii(self.command)
      commandASCII = self.scientificNotation(commandASCII)
      commandASCII = self.extract_value(commandASCII)

      dataASCII = self.string_to_ascii(self.data)
      dataASCII = self.scientificNotation(dataASCII)
      dataASCII = self.extract_value(dataASCII)

      self.hash = "%x" % (commandASCII + dataASCII)
    except OverflowError:
      # command or data is too long to convert
      self.hash = ""
      print("Error in Bot::generate_hash(): Parameter is too long")

  # Convert string into ascii code
  # Then concatenate each ascii code
  def string_to_ascii(self, string):
    buf = ""
    for char in string:
      ascii = ord(char)
      buf += str(ascii)
    return int(buf)
  
  # Extract value from scientific notation
  def extract_value(self, sn):
    if (not isinstance(sn, str)):
      # Parameter is not scientific notation
      return sn

    valuelist = sn.split(".")[1].split("e+")
    result = valuelist[0] + valuelist[1]
    return int(result)

  # Convert the number into scientific notation with 16 digits after "."
  # If power of e is greater than 20, get the number between "." and "e"
  # Else return the number itself
  def scientificNotation(self, num):
    data = "%.16e" % num
    result = data if (int(data.split("e+")[1]) > 20) else num
    return result
  
