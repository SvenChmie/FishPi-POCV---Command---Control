#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Entry point to the control software
# - check cmd line args
# - perform self check
#   - last running state
#   - check power level critical
# - configure devices
#   - scan and configure attached devices
#   - check config file
# - run selected mode
#   0: inactive (exits)
#   1: manual with UI (default)
#   2: manual headless
#   3: full auto

import sys
import logging

from Tkinter import Tk
from POCVMainView import *

from POCVMainViewController import *
from FishPiConfig import *

FISH_PI_VERSION = 0.1

class FishPiRunMode:
    Inactive, ManualWithUI, ManualHeadless, FullAuto = range(4)

class FishPi:
    """ Entrypoint and setup class. """
    selected_mode = FishPiRunMode.ManualWithUI
    config = FishPiConfig()

    def __init__(self, args):
        logging.info("Initializing FishPi (v{0})...".format(FISH_PI_VERSION))
        # TODO replace with standard cmd line parsing (eg argparse module)
        if args and len(args) >= 0:
            try:
                self.selected_mode = int(args[0])
            except ValueError:
                logging.warning("Usage 0:inactive, 1:manualWithUI, 2:manualHeadless, 3:fullAuto")
                logging.warning("Defaulting to {0}.".format(self.selected_mode))
        

    def self_check(self):
        # TODO implement check for .lastState file
        # check contents for run mode and stable exit
        logging.info("Checking last running state...")
        
        # TODO check for sufficient power for normal operation
        # otherwise implement eg emergency beacon mode
        logging.info("Checking sufficient power...")


    def configure_devices(self):
        """ Configures eg i2c and other attached devices."""
        self.config.configure_devices()

    def run(self):
        """ Runs selected FishPi mode."""
        logging.info("Starting FishPi in mode: {0}".format(self.selected_mode))
        if self.selected_mode == FishPiRunMode.Inactive:
            sys.exit(0)
        elif self.selected_mode == FishPiRunMode.ManualWithUI:
            self.run_ui()
        elif self.selected_mode == FishPiRunMode.ManualHeadless:
            self.run_headless()
        elif self.selected_mode == FishPiRunMode.FullAuto:
            self.run_auto()
        else:
            logging.error("Invalid mode! Exiting.")
            sys.exit(1)

    def run_ui(self):
        """ Runs in UI mode. """
        # configure
        self.configure_devices()
        
        # create controller
        controller = POCVMainViewController(self.config)

        # run ui loop
        rootWindow = Tk()

        rootWindow.minsize(800,600)
        rootWindow.maxsize(800,600)

        app = Main(rootWindow, controller)

        rootWindow.mainloop()


    def run_headless(self):
        """ Runs in headless (manual) mode. """
        # configure
        self.configure_devices()

        # create controller
        controller = POCVMainViewController(self.config)

        # testing
        controller.list_devices()

        # TODO wait for commands...
        pass

    def run_auto(self):
        """ Runs in full auto mode. """
        self.configure_devices()
        pass

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    fishPi = FishPi(sys.argv[1:])
    fishPi.self_check()
    fishPi.run()

if __name__ == "__main__":
    main()
