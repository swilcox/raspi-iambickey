# raspi-iambickey
a very basic Raspberry Pi Iambic Keyer program

## Overview

This is just a quick start on a python-based practice iambic keyer program. I'm sure some of this is wrong for a variety of reasons:

* I have not yet found the right formula for determing dit and dah length relative to the stated WPM
* I have no idea how exactly a real keyer works since I don't have one or a radio that contains one
* I just threw this together over a weekend to play with the key paddle kit I bought
* The decoder doesn't do symbols or extended characters

**note:** the obvious point is don't accept anything I did as necessarily right

## Use Notes

on a Raspberry Pi, you need pygame, numpy and Rpi.GPIO and a few other things that appear to be installed by default in Raspian.

To work with the GPIO pins, seems like running sudo is the way to go for now. So to run the program:

`sudo python iambickey.py`

You'll see it generate the tones (the dit and dah) and then it's ready to go. Have your dit paddle hooked to pin 23 and dah paddle hooked to 24 and ground to ground for the paddle.

It'll attempt to decode the letters/numbers as you key them. If it doesn't know, it will print a "*". Right now it's just putting out a letter per line. Later, I'll try to get fancier with spaces, etc.

## Credits

A shoutout and thanks to `M0XPD` who took a shot at this very thing. I used a few ideas from his code to get me going. Hopefully my code offers a more pythonic and expandable / modular example for doing a basic keyer.
