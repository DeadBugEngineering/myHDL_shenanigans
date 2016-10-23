from myhdl import *
from ssd1306_8x64bit_driver import *
'''
This python script simulates the design and generates
a trace-file which can be opened with gtkwave.

As a side-note: This is NOT sufficient to verify the design.
I'm new to myHDL and digital hardware design/verification in general
and don't know any better, yet.

to run:
python ssd1306_8x64bit_driver

(It may take some seconds to run the simulation because I have a 6ms long reset delay...)

'''




@block
def ssd1306_8x64bit_driver_testbench():
            
    clk = Signal(bool(0))
    reset = ResetSignal(1, active=0, async=True)
    reset_out = Signal(bool(0))
    val0 = Signal(intbv(0)[64:])
    val1 = Signal(intbv(0)[64:])
    val2 = Signal(intbv(0)[64:])
    val3 = Signal(intbv(0)[64:])
    val4 = Signal(intbv(0)[64:])
    val5 = Signal(intbv(0)[64:])
    val6 = Signal(intbv(0)[64:])
    val7 = Signal(intbv(0)[64:])
    control_contrast = Signal(intbv(0)[8:])
    control_inversion = Signal(bool(0))
    spi_csn = Signal(bool(0))
    spi_clk = Signal(bool(0))
    spi_dcn = Signal(bool(0))
    spi_mosi = Signal(bool(0))

    
    driver =  ssd1306_8x64bit_driver(   clk, 
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
    
   
    @instance
    def stim_val0():
        yield delay(500)
        val0.next = 0xFFFFFFFFFFFFFFFF
    return driver, clkgen, stim_val0

inst = ssd1306_8x64bit_driver_testbench()
inst.config_sim(trace=True)
inst.run_sim(duration=8000000)











    
