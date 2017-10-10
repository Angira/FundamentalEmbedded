class SC2004MBS(object):
    """
    The SC2004MBS is a wrapper class. It converts concrete actions as reading out the analog sensors, 
    writing to the display buffer, or clearing the screen to the appropriate modbus queries
    and executes them on the provided serial port. It does not provide any form of caching.
    
    (I've inplemented only the reading of IO-pins, I'd advise to implement additional members)
    """
    lines = 4
    columns = 20

    def __init__(self, instrument):
        """
        @type instrument: minimalmodbus.Instrument
        """
        self._instrument = instrument

    def io_pins(self):
        """
        Reads out the IO pins on Port 2 of the display. Pin cannot be retrieved independently as this functionality is
        not provided by the device.

        @rtype: list[bool]
        @return: A Deferred which eventually returns a L{list} containing eight bools, the first bool corresponds 
        to pin 1, the last to pin 8. True corresponds to an active IO, False to an inactive one.
        """
        state_byte = self._instrument.read_register(0, functioncode=4)
        state_list = self._unpack_to_bools(state_byte)
        state_pt = self.disp(state_list)
       # led_value = self.led_state(state_pt[:-4])

        return state_list





    @staticmethod
    def _unpack_to_bools(value, length=8):
        """
        Unpacks an int value to a list of bools, least significant bit first.
        
        Example: the binary value C{0b00011110} is converted to 
        => C{[False, True, True, True, True, False, False, False]}

        @type value: int
        @param value: The integer to convert
        @type length: int
        @param length: The number of bits to convert

        @rtype: list[bool]
        @return: list of bools, the n-th value in the list corresponds to the n-th least-significant bit
        in value. 1 corresponds to True, 0 to False
        """
        ret = []
        for pos in range(0, length):
            mask = 1 << pos
            bit = mask & value != 0
            ret.append(bit)
        return ret

    def disp(self, value):
        ret = []
        for v in value:
            if v:
                ret.append('X')
            else:
                ret.append('O')
        text = "Switches: {0} {1} {2} {3}".format(*ret)
        d = self._instrument.write_string(20,text,9)
        return ret


    def set_led(self, ledid, value):
        return self._instrument.write_bit(5 + ledid, value)







