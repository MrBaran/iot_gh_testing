from time import sleep
from datetime import datetime
from iot_gh.IoTGreenhouseService import IoTGreenhouseService

class IntegrationTests():
    """Provides component testing for IoT Greenhouse.
    """
    ghs = None

    def __init__(self, debug = False):
        if debug:
            import sys
            sys.path.append("..\iot_gh_unittests")
            #from uni iot_gh_unittests import pigpio_mock, spi_mock
            from iot_gh.GHService import GHService
            from pigpio_mock import pi_mock
            from spi_mock import spidev_mock
            pi = pi_mock()
            spi = spidev_mock()
            self.ghs = GHService(pi, spi)
        else:
            self.ghs = IoTGreenhouseService()

    def test_lamps(self):
        LAMP_ON_DELAY = 3
        LAMP_OFF_DELAY = 3
        print()
        print("Testing lamps...")
        print("Note: jumper must be positioned on J1 for Red LED to light.")
        print("Use Ctrl+C to end test.")
        try:
            while True:
                print()
                self.ghs.lamps.red.on() 
                print("Red", self.ghs.lamps.red.get_status())
                sleep(LAMP_ON_DELAY)
                self.ghs.lamps.red.off() 
                print("Red", self.ghs.lamps.red.get_status())
                sleep(LAMP_OFF_DELAY)
                self.ghs.lamps.white.on() 
                print("White", self.ghs.lamps.white.get_status())
                sleep(LAMP_ON_DELAY)
                self.ghs.lamps.white.off() 
                print("White", self.ghs.lamps.white.get_status())
                sleep(LAMP_OFF_DELAY)
                self.ghs.lamps.dual.on_green() 
                print("Dual", self.ghs.lamps.dual.get_status())
                sleep(LAMP_ON_DELAY)
                self.ghs.lamps.dual.off() 
                print("Dual", self.ghs.lamps.dual.get_status())
                sleep(LAMP_OFF_DELAY)
                self.ghs.lamps.dual.on_yellow() 
                print("Dual", self.ghs.lamps.dual.get_status())
                sleep(LAMP_ON_DELAY)
                self.ghs.lamps.dual.off() 
                print("Dual", self.ghs.lamps.dual.get_status())
                sleep(LAMP_OFF_DELAY)
        except KeyboardInterrupt:
            self.ghs.lamps.dual.off()
            self.ghs.lamps.red.off() 
            self.ghs.lamps.white.off() 
        print("Lamp test done.")
        print()

    def test_switches(self):
        from iot_gh.GHSwitches import GHSwitch
        print()
        print("Testing switches. PB activates Red LED, Toggle activates White LED.")
        print("Use Ctrl+C to end test.")
        last_pb_state = None
        last_toggle_state = None
        print()    
        try:
            while True:
                new_pb_state = self.ghs.switches.push_button.get_state()
                if new_pb_state != last_pb_state:
                    print("PB Switch", self.ghs.switches.push_button.get_status())
                    last_pb_state = new_pb_state

                new_toggle_state = self.ghs.switches.toggle.get_state()
                if new_toggle_state != last_toggle_state:
                    print("Toggle Switch", self.ghs.switches.toggle.get_status())
                    last_toggle_state = new_toggle_state

                sleep(.5)
        except KeyboardInterrupt:
            pass
        print("Switch test done.")
        print()

    def test_fan(self):
        print()
        print("Testing fan.")
        print("Use Ctrl+C to end test.")
        try:
            while True:
                print()
                self.ghs.fan.on()
                print("Fan", self.ghs.fan.get_status())
                sleep(5)
                self.ghs.fan.off()
                print("Fan", self.ghs.fan.get_status())
                sleep(5)
        except KeyboardInterrupt:
            self.ghs.fan.off()
        print("Fan test done.")
        print()

    def test_buzzer(self):
        print()
        print("Testing buzzer.")
        print("Use Ctrl+C to end test.")
        try:
            while True:
                print()
                self.ghs.buzzer.on()
                print("Buzzer", self.ghs.buzzer.get_status())
                sleep(1)
                self.ghs.buzzer.off()
                print("Buzzer", self.ghs.buzzer.get_status())
                sleep(1)
        except KeyboardInterrupt:
            self.ghs.buzzer.off()
        print("Buzzer test done.")
        print()

    def test_servo(self):
        print()
        print("Testing servo.")
        print("Use Ctrl+C to end test.")
        try:
            while True:
                print()
                pos = .5
                self.ghs.servo.move(pos)
                print("Servo", self.ghs.servo.get_status())
                sleep(1)
                pos = 1
                self.ghs.servo.move(pos)
                print("Servo", self.ghs.servo.get_status())
                sleep(1)
                pos = .5
                self.ghs.servo.move(pos)
                print("Servo", self.ghs.servo.get_status())
                sleep(1)
                pos = 0
                self.ghs.servo.move(pos)
                print("Servo", self.ghs.servo.get_status())
                sleep(1)
        except KeyboardInterrupt:
            pos = 0
            self.ghs.servo.move(pos)
        print("Servo test done.")
        print()

    def test_temperature(self):
        print()
        print("Testing temp sensor.")
        print("Use Ctrl+C to end test.")
        try:
            while True:
                print()
                print("i temp F: %d" % self.ghs.temperature.get_inside_temp_F())
                print("o temp F: %d" % self.ghs.temperature.get_outside_temp_F())
                sleep(1)
        except KeyboardInterrupt:
            pass
        print("Temp sensor test done.")
        print()    

    def test_analog(self):
        print()
        print("Testing analog inputs")
        print("Use Ctrl+C to end test.")
        try:
            while True:
                print()
                print("Pot value: %i" % self.ghs.analog.pot.get_value())
                print("Light value:" + str(self.ghs.analog.light.get_value()))
                print("Aux value:" + str(self.ghs.analog.aux.get_value()))
                sleep(1)
        except KeyboardInterrupt:
            pass
        print("Analog test done.")
        print()
        
    def show_menu(self):
        print("IoT Greenhouse integration testing.")
        print()
        print("\t0\tExit Tests")
        print("\t1\tTest Lamps")
        print("\t2\tTest Switches")
        print("\t3\tTest Fan")
        print("\t4\tTest Buzzer")
        print("\t5\tTest Servo")
        print("\t6\tTest Temperature")
        print("\t7\tTest Analog")
        

    def test_all(self):
        test_complete = False
        while not test_complete:
            self.show_menu()
            user_entry = input("Enter test number: ")
            if not user_entry.isdigit():
                print("Invalid entry. Try again.\n")
            else:
                user_choice = int(user_entry)
                if user_choice == 0:
                    test_complete = True
                elif user_choice == 1:
                    self.test_lamps()
                elif user_choice == 2:
                    self.test_switches()
                elif user_choice == 3:
                    self.test_fan()
                elif user_choice == 4:
                    self.test_buzzer()
                elif user_choice == 5:
                    self.test_servo()
                elif user_choice == 6:
                    self.test_temperature()
                elif user_choice == 7:
                    self.test_analog()
                elif user_choice == 8:
                    pass
                elif user_choice == 9:
                    pass
                else:
                    print("Invalid entry.")

        print("Done.")



