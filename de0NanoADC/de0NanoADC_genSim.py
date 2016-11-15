from myhdl import *
from scheduler_fsm_model import *
from scheduler_rom_model import *

'''
This python script simulates the design and generates
a trace-file which can be opened with gtkwave.
'''


@block
def DE0NanoADC_driver_sim():

    clk = Signal(bool(0))
    reset = ResetSignal(1, active=0, async=True)
    spi_csn = Signal(bool(0))
    spi_din = Signal(bool(0))
    spi_dout = Signal(bool(0))
    spi_sck = Signal(bool(0))
    flag_fifo_full = Signal(bool(0))
    data_packet = Signal(intbv(0)[64:])
    push_fifo = Signal(bool(0))
    error = Signal(bool(0))
    ROM_sample_slot = Signal(intbv(0)[16:])
    ROM_channel = Signal(intbv(0)[3:])
    
    driver = DE0NanoADC_driver( clk,
                                reset, 
                                spi_csn, 
                                spi_din, 
                                spi_dout, 
                                spi_sck,
                                flag_fifo_full, 
                                data_packet, 
                                push_fifo, 
                                error,
                                ROM_sample_slot,
                                ROM_channel )
                                
    seq_rom = rom(  ROM_channel,
                    ROM_sample_slot,
                    SAMPLE_SEQUENCE)
                                
    @always(delay(39)) # we need a 12M8Hz clock
    def clkgen():
        clk.next = not clk
        
    @instance
    def stim_sim():
        yield delay(1)
        flag_fifo_full.next = 0
    
    return driver, seq_rom, clkgen, stim_sim
    
    
inst = DE0NanoADC_driver_sim()
inst.config_sim(trace=True)
inst.run_sim(duration=500000) # simulation duration in ns







