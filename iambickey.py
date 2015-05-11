from RPi import GPIO
from time import time
import numpy
from pygame import mixer, sndarray
import math

LEFT_PIN = 23
RIGHT_PIN = 24

BLANK = None
DIT = 0
DAH = 1

WPM = 20.0
DIT_LENGTH = WPM / 200.0
DAH_LENGTH = DIT_LENGTH * 3.0

CHARS = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    ".._.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
}

class Paddles(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def dit_paddle(self):
        return not GPIO.input(LEFT_PIN)

    def dah_paddle(self):
        return not GPIO.input(RIGHT_PIN)


class Decoder(object):
    def __init__(self):
        self.last = time()
        self.current_sequence = ""

    def dit(self):
        self.current_sequence += "."

    def dah(self):
        self.current_sequence += "-"

    def blank(self):
        if time() - self.last > DAH_LENGTH:
            if self.current_sequence in CHARS:
                print CHARS[self.current_sequence]
            elif self.current_sequence != "":
                print "*"
            self.current_sequence = ""

    def decode(self, action):
        if action == DIT:
            self.dit()
        elif action == DAH:
            self.dah()
        else:
            self.blank()


def _make_tone(freq=800, volume=25000, length=1000):
    s = [int(math.sin(n * freq * (6.28218/22050)) * volume)
         for n in range(int(length) * 11)
         ]
    return sndarray.make_sound(numpy.array([[val, val] for val in s]))


class Beeper(object):
    def __init__(self):
        mixer.init()
        print "generating sounds"
        self.dit_snd = _make_tone(length=DIT_LENGTH * 1000)
        self.dah_snd = _make_tone(length=DAH_LENGTH * 1000)

    def _sleep(self, amount):
        start_time = time()
        while time() <= (start_time + amount):
            pass

    def _play_snd(self, snd):
        armed = False
        c = snd.play()
        while c.get_busy() or not armed:
            if c.get_busy():
                armed = True

    def send_dit(self):
        self._play_snd(self.dit_snd)
        self._sleep(DIT_LENGTH)

    def send_dah(self):
        self._play_snd(self.dah_snd)
        self._sleep(DIT_LENGTH)


class Sounder(object):
    def __init__(self):
        self.last = BLANK
        self.beeper = Beeper()

    def send_dit(self):
        self.last = DIT
        self.beeper.send_dit()

    def send_dah(self):
        self.last = DAH
        self.beeper.send_dah()

    def send_blank(self):
        self.last = BLANK

    def send_next(self, left, right):
        if left and right:
            if self.last == DIT:
                self.send_dah()
            elif self.last == DAH:
                self.send_dit()
            else:
                self.send_dah()
        elif left:
            self.send_dit()
        elif right:
            self.send_dah()
        else:
            self.send_blank()


def main():
    p = Paddles()
    s = Sounder()
    d = Decoder()
    while True:
        s.send_next(p.dit_paddle(), p.dah_paddle())
        d.decode(s.last)


if __name__ == "__main__":
    main()
