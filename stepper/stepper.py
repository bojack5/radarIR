# It works on the Raspberry Pi computer with the standard Debian Wheezy OS and
# the 28BJY-48 stepper motor with ULN2003 control board.

from time import sleep
import RPi.GPIO as GPIO

class Motor(object):
    def __init__(self, pins, mode=3):
        """Initialise the motor object.

        pins -- a list of 4 integers referring to the GPIO pins that the IN1, IN2
                IN3 and IN4 pins of the ULN2003 board are wired to
        mode -- the stepping mode to use:
                1: wave drive (not yet implemented)
                2: full step drive
                3: half step drive (default)

        """
        self.P1 = pins[0]
        self.P2 = pins[1]
        self.P3 = pins[2]
        self.P4 = pins[3]
        self.mode = mode
        self.deg_per_step = 5.625 / 64  # for half-step drive (mode 3)
        self.steps_per_rev = int(360 / self.deg_per_step)  # 4096
        self.step_angle = 0  # Assume the way it is pointing is zero degrees
        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)

    def _set_rpm(self, rpm):
        """Set the turn speed in RPM."""
        self._rpm = rpm
        # T is the amount of time to stop between signals
        self._T = (60.0 / rpm) / self.steps_per_rev

    # This means you can set "rpm" as if it is an attribute and
    # behind the scenes it sets the _T attribute
    rpm = property(lambda self: self._rpm, _set_rpm)



    def __clear(self):
        GPIO.output(self.P1, 0)
        GPIO.output(self.P2, 0)
        GPIO.output(self.P3, 0)
        GPIO.output(self.P4, 0)

        sleep(self._T * 2)

    def _move_acw_3(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P1, 0)
            sleep(self._T/4.)
            GPIO.output(self.P3, 1)
            sleep(self._T/4.)
            GPIO.output(self.P4, 0)
            sleep(self._T/4.)
            GPIO.output(self.P2, 1)
            sleep(self._T/4.)
            GPIO.output(self.P3, 0)
            sleep(self._T/4.)
            GPIO.output(self.P1, 1)
            sleep(self._T/4.)
            GPIO.output(self.P2, 0)
            sleep(self._T/4.)
            GPIO.output(self.P4, 1)
            sleep(self._T/4.)

    def _move_cw_3(self, big_steps):
        self.__clear()
        try:
            while True:
                GPIO.output(self.P3, 0)
                sleep(self._T/4.)
                GPIO.output(self.P1, 1)
                sleep(self._T/4.)
                GPIO.output(self.P4, 0)
                sleep(self._T/4.)
                GPIO.output(self.P2, 1)
                sleep(self._T/4.)
                GPIO.output(self.P1, 0)
                sleep(self._T/4.)
                GPIO.output(self.P3, 1)
                sleep(self._T/4.)
                GPIO.output(self.P2, 0)
                sleep(self._T/4.)
                GPIO.output(self.P4, 1)
                sleep(self._T/4.)
        except KeyboardInterrupt:
            print "Secuencia interrumpida por operador!"
            GPIO.cleanup()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    m = Motor([24,25,8,7])
    m.rpm = 5
    print "Pause in seconds: " + `m._T`
    m. _move_cw_3(1000)
    sleep(1)
