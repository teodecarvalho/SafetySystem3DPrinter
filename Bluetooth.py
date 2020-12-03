from jnius import autoclass

class Bluetooth():
    def __init__(self, device_name = "HC-05", device_address = "98:D3:11:FC:39:81"):
        self.connect_bluetooth(device_name = device_name, device_address = device_address)

    def setup_bluetooth(self):
        self._BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
        self._UUID = autoclass('java.util.UUID')

    def get_socket_stream(self, name, address):
        paired_devices = self._BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        self.socket = None
        for device in paired_devices:
            if device.getName() == name and device.getAddress() == address:
                print("[BLUETOOTH CONNECTION] Device found!")
                UUID = self._UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
                self.socket = device.createRfcommSocketToServiceRecord(UUID)
                self.receiver = self.socket.getInputStream()
                self.sender = self.socket.getOutputStream()
                break
        self.socket.connect()

    def connect_bluetooth(self, device_name = "HC-05", device_address = "98:D3:11:FC:39:81"):
        try:
            self.setup_bluetooth()
            self.get_socket_stream(name = device_name, address = device_address)
            print("[BLUETOOTH CONNECTION] Bluetooth connected!")
        except:
            self.show_popup(title="Ops!", msg="Can't connect!")

    def send_cmd(self, cmd):
        self.sender.write(cmd.encode())
        self.sender.flush()