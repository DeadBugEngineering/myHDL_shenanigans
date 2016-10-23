from myhdl import *
from spi4 import *
from ssd1306_8x64bit_fsm import *
from font_rom import *
'''
This python script models the top level of the design.

'''
@block
def ssd1306_8x64bit_driver( clk, 
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
                            spi_mosi ):


# internal signals  
    spi_data = Signal(intbv(0)[8:])
    latch = Signal(bool(0))
    spi_busy = Signal(bool(0))
    spi_latch = Signal(bool(0))
    dcn = Signal(bool(0))
    char_rom_address = Signal(intbv(0)[7:])
    char_rom_data = Signal(intbv(0)[8:])    
    

    # create an instance of the oled driver
    driver_inst =  ssd1306_8x64bit_fsm( #driver_state, 
                                        clk, 
                                        reset, 
                                        reset_out,
                                        spi_data, 
                                        spi_latch, 
                                        spi_busy,
                                        control_contrast, 
                                        control_inversion, 
                                        dcn, 
                                        val0, 
                                        val1, 
                                        val2, 
                                        val3, 
                                        val4, 
                                        val5, 
                                        val6, 
                                        val7, 
                                        char_rom_address, 
                                        char_rom_data )
                                            
                                            
                                            
                                            
    spi4_inst = ssd1306_spi_4(  clk, 
                                reset, 
                                spi_busy, 
                                spi_latch, 
                                dcn, 
                                spi_data, 
                                spi_clk, 
                                spi_mosi, 
                                spi_dcn,
                                spi_csn )  

                                
    rom_inst = rom(char_rom_data, char_rom_address, CONTENT)                     
                                         
    return driver_inst, spi4_inst,rom_inst
                                            
                                            
                                            
                                                                              
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                            
                                            
