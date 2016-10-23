from myhdl import *
'''
This python script models a fsm for the spi-transmitter.
'''



st_spi = enum(  'idle',
                'csn_low',
                'd7',
                'sd7',
                'd6',
                'sd6',
                'd5',
                'sd5',
                'd4',
                'sd4',
                'd3',
                'sd3',
                'd2',
                'sd2',
                'd1',
                'sd1',
                'd0',
                'sd0',
                'csn_high'#,
                #encoding= "one_hot" )  
                ) 

@block
def ssd1306_spi_4(  clk, 
                    reset, 
                    spi_busy, 
                    latch, 
                    dcn, 
                    data_in, 
                    spi_clk, 
                    spi_mosi, 
                    spi_dcn,
                    spi_csn ):

    data_buffer = Signal(intbv(0)[8:])
    dcn_buffer = Signal(bool(0))
    
    state = Signal(st_spi.idle)

    @always_seq(clk.posedge, reset=reset)
    def fsm_spi():
        if state == st_spi.idle:
            spi_clk.next = 0
            spi_mosi.next = 0
            spi_busy.next = 0
            spi_csn.next = 1
            if latch == 1:
                data_buffer.next = data_in
                dcn_buffer.next = dcn
                spi_busy.next = 1
                state.next = st_spi.csn_low
        elif state == st_spi.csn_low:
            spi_csn.next = 0
            state.next = st_spi.d7
        elif state == st_spi.d7:
            spi_clk.next = 0
            spi_mosi.next = data_buffer[8:7]
            state.next = st_spi.sd7
        elif state == st_spi.sd7:
            spi_clk.next = 1
            state.next = st_spi.d6
        elif state == st_spi.d6:
            spi_clk.next = 0
            spi_mosi.next = data_buffer[7:6]
            state.next = st_spi.sd6
        elif state == st_spi.sd6:
            spi_clk.next = 1
            state.next = st_spi.d5
        elif state == st_spi.d5:
            spi_clk.next = 0
            spi_mosi.next = data_buffer[6:5]
            state.next = st_spi.sd5
        elif state == st_spi.sd5:
            spi_clk.next = 1
            state.next = st_spi.d4
        elif state == st_spi.d4:
            spi_clk.next = 0
            spi_mosi.next = data_buffer[5:4]
            state.next = st_spi.sd4
        elif state == st_spi.sd4:
            spi_clk.next = 1
            state.next = st_spi.d3
        elif state == st_spi.d3:
            spi_clk.next = 0
            spi_mosi.next = data_buffer[4:3]
            state.next = st_spi.sd3
        elif state == st_spi.sd3:
            spi_clk.next = 1
            state.next = st_spi.d2
        elif state == st_spi.d2:
            spi_clk.next = 0
            spi_mosi.next = data_buffer[3:2]
            state.next = st_spi.sd2
        elif state == st_spi.sd2:
            spi_clk.next = 1
            state.next = st_spi.d1
        elif state == st_spi.d1:
            spi_clk.next = 0
            spi_mosi.next = data_buffer[2:1]
            state.next = st_spi.sd1
        elif state == st_spi.sd1:
            spi_clk.next = 1
            state.next = st_spi.d0
        elif state == st_spi.d0:
            spi_clk.next = 0
            spi_mosi.next = data_buffer[1:0]
            spi_dcn.next = dcn_buffer
            state.next = st_spi.sd0
        elif state == st_spi.sd0:
            spi_clk.next = 1
            state.next = st_spi.csn_high
        elif state == st_spi.csn_high:
            spi_clk.next = 0
            spi_csn.next = 1
            state.next = st_spi.idle
        else:
            raise ValueError("Undefined state")
            
    return fsm_spi
