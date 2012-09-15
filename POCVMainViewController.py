
#
# FishPi - An autonomous drop in the ocean
#
# View Controller for POCV MainView
#  - control logic split out from UI, providing:
#    - access to device configuration and drivers
#    - basic control systems eg power and steering
#    - sensory systems eg GPS and Compass
#    - route planning and navigation
#

import logging
import os
from time import localtime

from PIL import Image

from FishPiConfig import FishPiConfig
from NavigationUnit import NavigationUnit
from PerceptionUnit import PerceptionUnit

class POCVMainViewController:
    """ Coordinator between UI and main control layers. """
    
    def __init__(self, config):
        self.config = config
        
        # setup controllers and coordinating services
        
        # CameraController
        try:
            from CameraController import CameraController
            self.camera_controller = CameraController(self.config)
        except ImportError:
            logging.info("pygame package not found, camera support unavailable.")
            self.camera_controller = DummyCameraController()
        
        # DriveController
        if os.getuid() == 0:
            try:
                from DriveController import DriveController
                self.drive_controller = DriveController(self.config)
            except ImportError:
                logging.info("drive controller not loaded, drive support unavailable.")
                self.drive_controller = DummyDriveController()
        else:
            logging.info("not running as root, drive support unavailable.")
            self.drive_controller = DummyDriveController()

        self.perception_unit = PerceptionUnit()
        self.navigation_unit = NavigationUnit(self.drive_controller, self.perception_unit)

    # Devices

    def list_devices(self):
        for device in self.config.devices:
            print device

    def capture_img(self):
        self.camera_controller.capture_now()

    @property
    def last_img(self):
        self.camera_controller.last_img

    # Control Systems
    # temporary direct access to DriveController to test hardware.
    # ...

    # Sensors

    def read_time(self):
        return localtime()

    def read_GPS(self):
        pass

    def read_compass(self):
        pass


    # Route Planning and Navigation

    def navigate_to(self):
        """ Commands the NavigationUnit to commence navigation of a route. """
        #self.navigation_unit.NavigateTo(route)
        pass

    def halt(self):
        """ Commands the NavigationUnit to Halt! """
        self.navigation_unit.Halt()

class DummyCameraController(object):
    
    def __init__(self):
        self._last_img = Image.open("cam.jpg")

    def capture_now(self):
        pass

    @property
    def last_img(self):
        return self._last_img

class DummyDriveController(object):
    def __init__(self):
         pass

    def set_drive(self):
        pass

    def set_heading(self):
        pass

    def halt(self):
        pass
