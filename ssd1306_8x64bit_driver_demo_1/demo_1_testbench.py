import sys
sys.path.append('../ssd1306_8x64bit_driver')



from myhdl import *
from ssd1306_8x64bit_driver import *
from spi4 import *
from font_rom import *
from ssd1306_8x64bit_fsm import *

"""
This script generates an application example of core#1.

"""


@block
def const_driver(val, clk, reset ):
    @always_seq(clk.posedge, reset=reset)
    def set_value():
        val.next = val
    return set_value

@block
def counter(value, clk, reset):
    @always_seq(clk.posedge, reset=reset)
    def freeCounter():
        value.next = value + 1
    return freeCounter


@block
def oled_demo ( clk,
                reset,
                reset_out,
                spi_csn,
                spi_clk,
                spi_dcn,
                spi_mosi ):

    # internal signals
    # the eight 64bit counters get different initialization values
    # modbv is used here so that the counters start at zero after a overflow

    val0 = Signal(modbv(0)[64:])
    val1 = Signal(modbv(5000)[64:])
    val2 = Signal(modbv(123123)[64:])
    val3 = Signal(modbv(2123)[64:])
    val4 = Signal(modbv(3232)[64:])
    val5 = Signal(modbv(45765)[64:])
    val6 = Signal(modbv(3)[64:])
    val7 = Signal(modbv(2342342)[64:])
    control_contrast = Signal(intbv(127)[8:])
    control_inversion = Signal(bool(1))

    const_0 = const_driver(control_contrast, clk, reset)
    const_1 = const_driver(control_inversion, clk, reset)


    counter_0 = counter(val0, clk, reset )
    counter_1 = counter(val1, clk, reset )
    counter_2 = counter(val2, clk, reset )
    counter_3 = counter(val3, clk, reset )
    counter_4 = counter(val4, clk, reset )
    counter_5 = counter(val5, clk, reset )
    counter_6 = counter(val6, clk, reset )
    counter_7 = counter(val7, clk, reset )
    

    driver = ssd1306_8x64bit_driver(    clk, 
                                        reset, 
                                        reset_out,
                                        val0, 
                                        val1, 
                                        val2,
                                        val3,
                                        val4,
                                        val5,
                                        val6,
                                        val7,
                                        control_contrast,
                                        control_inversion,
                                        spi_csn,
                                        spi_clk,
                                        spi_dcn,
                                        spi_mosi )
    @always(delay(25))
    def clkgen():
        clk.next = not clk
        

    return driver, counter_0, counter_1, counter_2, counter_3,counter_4, counter_5, counter_6, counter_7, const_0, const_1, clkgen
            
            
clk = Signal(bool(0))
reset = ResetSignal(1, active=0, async=True)
spi_csn = Signal(bool(0))
spi_clk = Signal(bool(0))
spi_dcn = Signal(bool(0))
spi_mosi = Signal(bool(0))
reset_out = Signal(bool(0))

inst = oled_demo (clk, reset, reset_out, spi_csn, spi_clk, spi_dcn, spi_mosi)
inst.config_sim(trace=True)
inst.run_sim(duration=800000)







   
