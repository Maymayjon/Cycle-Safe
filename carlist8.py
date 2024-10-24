from carcoordinates8 import car_coord
import cv2
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import the RFM69 radio module.
import adafruit_rfm69

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Configure Packet Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
prev_packet = None
# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
rfm69.encryption_key = (
    b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
)
# BGR
color_list = [
    (0, 0, 255),
    (0, 128, 255),
    (0, 255, 255),
    (0, 255, 128),
    (0, 255, 0),
    (128, 255, 0),
    (255, 255, 0),
    (255, 128, 0),
    (255, 0, 0),
    (255, 128, 0),
    (255, 255, 0),
    (128, 255, 0),
]

class car_list:
    def __init__(self, retire_age=10, hide_age=24):
        self.car_coordinate_list = []
        self.retire_age = retire_age
        # self.hide_age = hide_age
        self._count = 0

    def increment_frame(self):
        for car_coordinate in self.car_coordinate_list:
            car_coordinate.incr_age()

    def retire_coords(self):
        for car_coordinate in self.car_coordinate_list:
            time = car_coordinate.age - car_coordinate.last_update
            if time > self.retire_age:
                self.car_coordinate_list.remove(car_coordinate)

    def add_car(self, x, y, w, h):
        for car_coordinate in self.car_coordinate_list:
            existing_car = car_coordinate.compare(x, y, w, h, radius=100)
            if existing_car:
                car_coordinate.set_coord(x, y, w, h)
                return

        color = color_list[self._count % len(color_list)]
        new_car_coord = car_coord(x, y, w, h, name=str(self._count), color=color)
        self._count = self._count + 1
        self.car_coordinate_list.append(new_car_coord)

    def clear_coords(self):
        self.car_coordinate_list.clear()

    def determine_increase(self, width):
        for car_coordinate in self.car_coordinate_list:
            if car_coordinate.age > 45:
                car_coordinate.check_increasing()
            if car_coordinate.increasing:
                if car_coordinate.x > (width * 3) // 5:
                    button_a_data = bytes("Button A!\r\n", "utf-8")
                    rfm69.send(button_a_data)
                    # print("increasing on left")
                elif car_coordinate.x < (width * 2) // 5:
                    button_c_data = bytes("Button C!\r\n", "utf-8")
                    rfm69.send(button_c_data)
                    # print("increasing on right")
                else:
                    button_b_data = bytes("Button B!\r\n", "utf-8")
                    rfm69.send(button_b_data)
                    # print("increasing on behind")


    def draw_boxes(self, frame, border_size=2, font_size=2):
        for coord in self.car_coordinate_list:
            x, y, w, h = coord.get_box()
            color = coord.color
            name = coord.name

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, border_size)
            cv2.putText(
                frame,
                name,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color
            )
