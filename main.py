from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
import time

from Bluetooth import Bluetooth
class MainWindow(BoxLayout):
     def __init__(self, **kwargs):
         super(MainWindow, self).__init__(**kwargs)
         try:
            self.bluetooth = Bluetooth(device_name = "HC-05", device_address = "98:D3:11:FC:39:81")
         except:
             pass
             self.show_popup(title = "Ops!", msg = "Could not connect to device!")
     time_rem = ObjectProperty(None)
     time_slider = ObjectProperty(None)
     time_last_set = 0
     time = None

     class P(BoxLayout):
         pass

     def show_popup(self, title, msg):
         popup_window = Popup(title = title,
                              content = Label(text = msg, font_size = 20),
                              size_hint = (None, None), size = (400, 150))
         popup_window.open()

     def send_cmd(self, cmd):
         self.bluetooth.send_cmd()

     def set_time(self):
         self.time = int(self.time_slider.value)
         self.time_last_set = time.monotonic()
         try:
             self.send_cmd(f'<st{self.time}>')
             self.show_popup(title="Success", msg=f"Time set to {self.time} minutes!")
         except:
             self.show_popup(title = "Ops!", msg = "No device available!")

     def calculate_rem_time(self):
         now = time.monotonic()
         difference = self.time - (now - self.time_last_set) / 60
         return "%.2f"%max(difference, 0)

     def show_rem_time(self):
         try:
             self.time_rem.text = str(self.calculate_rem_time())
         except AttributeError:
             pass

class Control3DPrinterApp(App):
    def build(self):
        return MainWindow()

if __name__ == '__main__':
    Control3DPrinterApp().run()