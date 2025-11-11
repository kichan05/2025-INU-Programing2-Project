import time
from typing import Iterable

import pyfirmata2

class Arduino:
    def __init__(self, PORT: str):
        self.PORT = PORT
        self.board = pyfirmata2.Arduino(PORT)

        self.SAMPLING_INTERVAL = 100
        self.LED_ON = 0
        self.LED_OFF = 1
        self.LED_PINS = [10, 11, 12, 13]

        self.BUZZER_PIN = 3

        self.board.samplingOn(self.SAMPLING_INTERVAL)

        self.is_prev_clicked: dict[str, bool] = {}

    def __del__(self):
        if (self.board):
            self.board.exit();

    def led_on(self, pins: Iterable[int], gap: float = 0):
        for i in pins:
            self.board.digital[i].write(self.LED_ON)
            time.sleep(gap)

    def led_off(self, pins: Iterable[int], gap: float = 0):
        for i in pins:
            self.board.digital[i].write(self.LED_OFF)
            time.sleep(gap)

    def all_led_on(self, gap: float = 0):
        self.led_on(pins=self.LED_PINS, gap=gap)

    def all_led_off(self, gap: float = 0):
        self.led_off(pins=self.LED_PINS, gap=gap)

    def lef_blink(self, pins: Iterable[int], repeat: int, gap: float):
        self.led_off(pins=pins)

        for _ in range(repeat):
            self.led_on(pins)
            time.sleep(gap)

            self.led_off(pins)
            time.sleep(gap)

    def add_on_click_event(self, pin: str, call_back):
        def clicked(v):
            is_pressed = v < 0.5
            if (is_pressed):
                self.is_prev_clicked[pin] = True
            else:
                if (not self.is_prev_clicked[pin]):
                    return

                self.is_prev_clicked[pin] = False
                call_back()

        self.is_prev_clicked[pin] = False
        analog_1 = self.board.get_pin(pin)
        analog_1.register_callback(clicked)
        analog_1.enable_reporting()

    def buzzer_sound(self, length : float):
        self.board.digital[self.BUZZER_PIN].write(self.LED_ON)
        time.sleep(length)
        self.board.digital[self.BUZZER_PIN].write(self.LED_OFF)

    def buzzer_dot(self):
        self.buzzer_sound(0.1)

    def buzzer_dash(self):
        self.buzzer_sound(0.5)
