from mycroft.util.log import getLogger
from mycroft.skills.core import MycroftSkill
import subprocess
import time
#from os.path import join, abspath, dirname

__author__ = 'aussieW'

LOGGER = getLogger(__name__)

class MycroftPushToListen(MycroftSkill):
    def __init__(self):
        super(MycroftPushToListen, self).__init__(name='MycroftPushToListen')
        self.button_pin = self.settings['gpio']
        self.proc = None
        
        # listen for setting changes
        self.settings.set_changed_callback(self._check_gpio_changed)
        
    def initialize(self):
        # start the button listener
        #subprocess.call(join(abspath(dirname(__file__)), 'button.py'))
        self._start()
        
    def _check_gpio_changed(self):
        # check if the gpio pin has changed
        if self.settings['gpio'] != self.button_pin:
            LOGGER.info("GPIO pin changed")
            # restart button.py with the new pin assigned
            self._stop()
            time.sleep(2)  # chose an arbitrary value
            self.button_pin = self.settings['gpio']
            self.start()
        
    def _start(self):
        self.proc = subprocess.Popen(['python', '/opt/mycroft/skills/mycroft-push-to-listen/button.py', self.button_pin])
        LOGGER.info('button process pid = ' + str(self.proc.pid))
    
    def _stop(self):
        self.proc.kill()
        LOGGER.info('Shutting down button.py')
        
    def shutdown(self):
        # shutdown the button.py process
        self._stop()
        super(MycroftPushToListen, self).shutdown()
        
def create_skill():
    return MycroftPushToListen()
