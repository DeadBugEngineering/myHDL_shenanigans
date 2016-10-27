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
def downcounter(value, decrement, clk, reset):
    @always_seq(clk.posedge, reset=reset)
    def freedowncounter():
        value.next = value - decrement
    return freedowncounter

@block
def upcounter(value, increment, clk, reset):
    @always_seq(clk.posedge, reset=reset)
    def freeupcounter():
        value.next = value + increment
    return freeupcounter

@block
def constant(signal, const):
    @always_seq(clk.posedge, reset=reset)
    def const_driver():
        signal.next = const
    return const_driver


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

    val0 = Signal(intbv(0)[64:])
    val1 = Signal(intbv(0)[64:])
    val2 = Signal(intbv(0)[64:])
    val3 = Signal(intbv(0)[64:])
    val4 = Signal(intbv(0)[64:])
    val5 = Signal(intbv(0)[64:])
    val6 = Signal(intbv(0)[64:])
    val7 = Signal(intbv(0)[64:])
    control_contrast = Signal(intbv(255)[8:])
    control_inversion = Signal(bool(1))


    # we instantiate one counter for each row, with different increments
    counter_0 = upcounter(  val0, 10, clk, reset )
    counter_1 = upcounter(  val1,  5, clk, reset )
    counter_2 = upcounter(  val2,  2, clk, reset )
    counter_3 = upcounter(  val3,  1, clk, reset )
    counter_4 = downcounter(val4,  1, clk, reset )
    counter_5 = downcounter(val5,  2, clk, reset )
    counter_6 = downcounter(val6,  5, clk, reset )
    counter_7 = downcounter(val7, 10, clk, reset )

    constant_0 = constant(control_contrast, 255)
    constant_1 = constant(control_inversion, 0)
    

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
        

    return driver, counter_0, counter_1, counter_2, counter_3, counter_4, counter_5, counter_6, counter_7, constant_0, constant_1
            
            
clk = Signal(bool(0))
reset = ResetSignal(1, active=0, async=True)
spi_csn = Signal(bool(0))
spi_clk = Signal(bool(0))
spi_dcn = Signal(bool(0))
spi_mosi = Signal(bool(0))
reset_out = Signal(bool(0))

inst = oled_demo (clk, reset, reset_out, spi_csn, spi_clk, spi_dcn, spi_mosi)
inst.convert(hdl='Verilog')






   
