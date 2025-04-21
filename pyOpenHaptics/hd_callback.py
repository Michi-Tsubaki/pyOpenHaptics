from ctypes import *
from .hd_define import *
import functools
from .hd import *
from sys import platform

if platform == "linux" or platform == "linux2":
    _lib_hd = CDLL("libHD.so")
elif platform == "win32":
    _lib_hd = CDLL("HD.dll")

def hd_callback(input_function):
    @functools.wraps(input_function)
    @CFUNCTYPE(HDCallbackCode, POINTER(c_void_p))
    def _callback(pUserData):
        """Callback function for the haptic device."""
        current_device = get_current_device()
        begin_frame(current_device)
        input_function(current_device)  # Pass the device ID to your function
        end_frame(current_device)
        if get_error():
            return HD_CALLBACK_DONE
        return HD_CALLBACK_CONTINUE
    
    return _callback

def hdAsyncSheduler(callback, device_id=None):
    if device_id is None:
        device_id = get_current_device()
    make_current_device(device_id)  # Ensure we're operating on the right device
    pUserData = c_void_p()
    _lib_hd.hdScheduleAsynchronous(callback, byref(pUserData), HD_MAX_SCHEDULER_PRIORITY)

def hdSyncSheduler(callback, device_id=None):
    if device_id is None:
        device_id = get_current_device()
    make_current_device(device_id)  # Ensure we're operating on the right device
    pUserData = c_void_p()
    _lib_hd.hdScheduleSynchronous(callback, byref(pUserData), HD_MAX_SCHEDULER_PRIORITY)