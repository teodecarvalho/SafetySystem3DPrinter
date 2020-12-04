from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.clock import Clock
import time

from Bluetooth import Bluetooth
class MainWindow(FloatLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        try:
           self.bluetooth = Bluetooth(device_name = "HC-05", device_address = "98:D3:11:FC:39:81")
        except:
            pass
            self.show_popup(title = "Ops!", msg = "Could not connect to device!")

    time_rem = ObjectProperty(None)
    time_slider = ObjectProperty(None)
    time = None

    class P(FloatLayout):
        pass

    def show_popup(self, title, msg):
        popup_window = Popup(title = title,
                             content = Label(text = msg, font_size = 20),
                             size_hint = (None, None), size = (400, 150))
        popup_window.open()

    def send_cmd(self, cmd):
        self.bluetooth.send_cmd(cmd)

    def read_msg(self):
        return self.bluetooth.read_msg()

    def get_remaining_time(self):
        self.read_msg() # Empty the buffer if there is anything there
        self.send_cmd("<dt>")
        time.sleep(1)
        msg_time = float(self.read_msg()[2:])
        return msg_time

    def set_time(self):
        self.time = int(self.time_slider.value)
        self.time_last_set = time.monotonic()
        self.send_cmd(f'<st{self.time}>')

class Control3DPrinterApp(App):
    def on_start(self):
        Clock.schedule_interval(callback=self.update_rem_time, timeout=2)

    def update_rem_time(self, *args):
        self.root.ids.time_rem.text = str(self.root.get_remaining_time())

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    Control3DPrinterApp().run()