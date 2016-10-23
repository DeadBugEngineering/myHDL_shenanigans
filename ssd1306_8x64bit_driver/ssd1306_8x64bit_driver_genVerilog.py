from myhdl import *
from ssd1306_8x64bit_driver import *

"""
This script instanciates the top level design of the oled driver and generates its Verilog-file.
"""

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




inst = ssd1306_8x64bit_driver(  clk, 
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

inst.convert(hdl='Verilog')                               
