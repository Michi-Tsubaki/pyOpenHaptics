from .hd import *
from.hd_callback import *
from .hd_define import *

class HapticDevice(object):
    def __init__(self, callback: hd_callback, device_name: str = "Default Device", scheduler_type: str = "async"):
        print("Initializing haptic device with name {}".format(device_name))
        
        # Initialize the device first
        self.id = init_device(device_name)
        if self.id == HD_BAD_HANDLE:
            print("Unable to initialize the device. Check the connection!")
            return
        
        # Make this device current for further operations
        make_current_device(self.id)
        
        print("Initialized device! {}/{}".format(self.__vendor__(), self.__model__()))
        enable_force()
        start_scheduler()
        if get_error():
            raise SystemError("Error initializing device scheduler")
        
        # Set up callback for this specific device
        self.scheduler(callback, scheduler_type)

    def close(self):
        stop_scheduler()
        close_device(self.id)
    
    def scheduler(self, callback, scheduler_type):
        if scheduler_type == "async":
            hdAsyncSheduler(callback, self.id)
        else:
            hdSyncSheduler(callback, self.id)


    @staticmethod
    def __vendor__() -> str:
        return get_vendor()
    
    @staticmethod
    def __model__() -> str:
        return get_model()