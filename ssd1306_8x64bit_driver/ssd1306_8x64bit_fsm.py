from myhdl import *


'''
This core accepts eight 64bit unsigned integer values and pushes them via 
the spi core named ssd1306_spi_4 onto the 128x64 pixel oled display.
Two config parameters can also be supplied via uint values, namely for "contrast(uint8)"
and "inversion(bool)".

'''
            
# the states of the driver state machine
st_dr = enum  ( 'init',
                'reset',
                'setup_mem_address_1',
                'latch_mem_address_1',
                'setup_mem_address_2',
                'latch_mem_address_2',
                'setup_display_A4',
                'latch_display_A4',
                'setup_ena_charge_reg_1',
                'latch_ena_charge_reg_1',
                'setup_ena_charge_reg_2',
                'latch_ena_charge_reg_2',
                'setup_disp_on',
                'latch_disp_on',
                'setup_contrast_control_1', # begin refresh parameter
                'latch_contrast_control_1',
                'setup_contrast_control_2',
                'latch_contrast_control_2',
                'setup_inversion',
                'latch_inversion',
                'buffer_frame', # res. transmit_frame_counter latching input values
                'load_char', # buffering next char to send to the slicer
                'rom_char_slice', # loading rom_address for next char slice
                'load_char_slice', # driving next char slice on data output
                'latch_char_slice', # drive latch signal when spi is not busy
                 encoding= "one_hot" 
                 )
            
@block            
def ssd1306_8x64bit_fsm(   clk, reset, reset_out, data_out, latch_out, spi_busy_in,
                           control_contrast, control_inversion, dcn_out, 
                           val0, val1, val2, val3, val4, val5, val6, val7, 
                           char_rom_address, char_rom_data):

    val0_buffer = Signal(intbv(0)[64:])
    val1_buffer = Signal(intbv(0)[64:])
    val2_buffer = Signal(intbv(0)[64:])
    val3_buffer = Signal(intbv(0)[64:])
    val4_buffer = Signal(intbv(0)[64:])
    val5_buffer = Signal(intbv(0)[64:])
    val6_buffer = Signal(intbv(0)[64:])
    val7_buffer = Signal(intbv(0)[64:])
    char_buffer = Signal(intbv(0)[8:])
    con_contrast_buffer = Signal(intbv(0)[8:])
    con_inversion_buffer = Signal(bool(0))
    reset_delay = Signal(intbv(0)[64:])
    
    # control counter to push 128 hex values to the graph-slicer
   # char_counter = Signal(intbv(0, min=0, max=128))
    char_counter = Signal(intbv(0, min=0, max=130))    
    # the graph-slicer sends eight column-slices per hex value to the display,
    # see page 25 in the manual of the ssd1306.
    #char_slice_counter = Signal(intbv(0, min=0, max=9)) # each char has eight slices of pixel data.
    char_slice_counter = Signal(intbv(0, min=0, max=13)) # each char has eight slices of pixel data.
    
    state = Signal(st_dr.init)

    @always_seq(clk.posedge, reset=reset)
    def fsm_dr():
        if state == st_dr.init:
            state.next = st_dr.reset
            latch_out.next = 0
            reset_delay.next = 0
        elif state == st_dr.reset:
            reset_delay.next = reset_delay + 1
            reset_out.next = 0
            # reset_delay_max should be 120000 for normal operation.
            if reset_delay > 120000: # @clk==20MHz the delay should be approx. 6ms long
                state.next = st_dr.setup_mem_address_1
            else:
                state.next = st_dr.reset
        elif state == st_dr.setup_mem_address_1:
            reset_out.next = 1
            data_out.next = 32 # set memory addressing mode 0x20
            dcn_out.next = 0 # the next byte is a command, not a display value
            state.next = st_dr.latch_mem_address_1
            
        elif state == st_dr.latch_mem_address_1:
            if spi_busy_in == 0:
                latch_out.next = 1
                state.next = st_dr.setup_mem_address_2
            else:
                latch_out.next = 0
                state.next = st_dr.latch_mem_address_1

        elif state == st_dr.setup_mem_address_2:
            data_out.next = 0 # we want the horizontal addressing mode
            dcn_out.next = 0
            latch_out.next = 0
            state.next = st_dr.latch_mem_address_2
            
        elif state == st_dr.latch_mem_address_2:
            if spi_busy_in == 0:
                latch_out.next = 1
                state.next = st_dr.setup_display_A4
            else:
                latch_out.next = 0
                state.next = st_dr.latch_mem_address_2
                
        elif state == st_dr.setup_display_A4:
            data_out.next = 164 # 0xA4, entire display on
            dcn_out.next = 0
            latch_out.next = 0
            state.next = st_dr.latch_display_A4

        elif state == st_dr.latch_display_A4:
            if spi_busy_in == 0:
                latch_out.next = 1
                state.next = st_dr.setup_ena_charge_reg_1
            else:
                latch_out.next = 0
                state.next = st_dr.latch_display_A4

        elif state == st_dr.setup_ena_charge_reg_1:
            data_out.next = 141 # 0x8D, config charge pump reg.
            dcn_out.next = 0
            latch_out.next = 0
            state.next = st_dr.latch_ena_charge_reg_1

        elif state == st_dr.latch_ena_charge_reg_1:
            if spi_busy_in == 0:
                latch_out.next = 1
                state.next = st_dr.setup_ena_charge_reg_2
            else:
                latch_out.next = 0
                state.next = st_dr.latch_ena_charge_reg_1

        elif state == st_dr.setup_ena_charge_reg_2:
            data_out.next =  20 # 0x14, activate charge pump
            dcn_out.next = 0
            latch_out.next = 0
            state.next = st_dr.latch_ena_charge_reg_2

        elif state == st_dr.latch_ena_charge_reg_2:
            if spi_busy_in == 0:
                latch_out.next = 1
                state.next = st_dr.setup_disp_on
            else:
                latch_out.next = 0
                state.next = st_dr.latch_ena_charge_reg_2

        elif state == st_dr.setup_disp_on:
            data_out.next =  175 # 0xAF, display on
            dcn_out.next = 0
            latch_out.next = 0
            state.next = st_dr.latch_disp_on

        elif state == st_dr.latch_disp_on:
            if spi_busy_in == 0:
                latch_out.next = 1
                state.next = st_dr.setup_contrast_control_1
            else:
                latch_out.next = 0
                state.next = st_dr.latch_disp_on

        elif state == st_dr.setup_contrast_control_1:
            # sampling the contrast control value for later use
            con_contrast_buffer.next = control_contrast
            data_out.next =  129 # 0x81, contrast control
            dcn_out.next = 0
            latch_out.next = 0
            state.next = st_dr.latch_contrast_control_1


        elif state == st_dr.latch_contrast_control_1:
            if spi_busy_in == 0:
                latch_out.next = 1
                state.next = st_dr.setup_contrast_control_2
            else:
                latch_out.next = 0
                state.next = st_dr.latch_contrast_control_1

        elif state == st_dr.setup_contrast_control_2:
            data_out.next =  con_contrast_buffer
            dcn_out.next = 0
            latch_out.next = 0
            state.next = st_dr.latch_contrast_control_2

        elif state == st_dr.latch_contrast_control_2:
            if spi_busy_in == 0:
                latch_out.next = 1
                con_inversion_buffer.next = control_inversion
                state.next = st_dr.setup_inversion
            else:
                latch_out.next = 0
                state.next = st_dr.latch_contrast_control_2
        
        elif state == st_dr.setup_inversion:
            data_out.next =  con_inversion_buffer
            dcn_out.next = 0
            latch_out.next = 0
            state.next = st_dr.latch_inversion

        elif state == st_dr.latch_inversion:
            if spi_busy_in == 0:
                latch_out.next = 1
                state.next = st_dr.buffer_frame
            else:
                latch_out.next = 0
                state.next = st_dr.latch_inversion

        elif state == st_dr.buffer_frame:
            # latching all eight 64bit values into the buffer
            val0_buffer.next = val0
            val1_buffer.next = val1
            val2_buffer.next = val2
            val3_buffer.next = val3
            val4_buffer.next = val4
            val5_buffer.next = val5
            val6_buffer.next = val6
            val7_buffer.next = val7
            # resetting counters for frame transmission
            char_counter.next = 0
            char_slice_counter.next = 0
            state.next = st_dr.load_char
            
        elif state == st_dr.load_char:
            char_slice_counter.next = 0
            if char_counter == 0:
                char_buffer.next = val0_buffer[64:60]
            elif char_counter == 1:
                char_buffer.next = val0_buffer[60:56]
            elif char_counter == 2:
                char_buffer.next = val0_buffer[56:52]
            elif char_counter == 3:
                char_buffer.next = val0_buffer[52:48]
            elif char_counter == 4:
                char_buffer.next = val0_buffer[48:44]
            elif char_counter == 5:
                char_buffer.next = val0_buffer[44:40]
            elif char_counter == 6:
                char_buffer.next = val0_buffer[40:36]
            elif char_counter == 7:
                char_buffer.next = val0_buffer[36:32]
            elif char_counter == 8:
                char_buffer.next = val0_buffer[32:28]
            elif char_counter == 9:
                char_buffer.next = val0_buffer[28:24]
            elif char_counter == 10:
                char_buffer.next = val0_buffer[24:20]
            elif char_counter == 11:
                char_buffer.next = val0_buffer[20:16]
            elif char_counter == 12:
                char_buffer.next = val0_buffer[16:12]
            elif char_counter == 13:
                char_buffer.next = val0_buffer[12:8]
            elif char_counter == 14:
                char_buffer.next = val0_buffer[8:4]
            elif char_counter == 15:
                char_buffer.next = val0_buffer[4:0]
            elif char_counter == 16:
                char_buffer.next = val1_buffer[64:60]
            elif char_counter == 17:
                char_buffer.next = val1_buffer[60:56]
            elif char_counter == 18:
                char_buffer.next = val1_buffer[56:52]
            elif char_counter == 19:
                char_buffer.next = val1_buffer[52:48]
            elif char_counter == 20:
                char_buffer.next = val1_buffer[48:44]
            elif char_counter == 21:
                char_buffer.next = val1_buffer[44:40]
            elif char_counter == 22:
                char_buffer.next = val1_buffer[40:36]
            elif char_counter == 23:
                char_buffer.next = val1_buffer[36:32]
            elif char_counter == 24:
                char_buffer.next = val1_buffer[32:28]
            elif char_counter == 25:
                char_buffer.next = val1_buffer[28:24]
            elif char_counter == 26:
                char_buffer.next = val1_buffer[24:20]
            elif char_counter == 27:
                char_buffer.next = val1_buffer[20:16]
            elif char_counter == 28:
                char_buffer.next = val1_buffer[16:12]
            elif char_counter == 29:
                char_buffer.next = val1_buffer[12:8]
            elif char_counter == 30:
                char_buffer.next = val1_buffer[8:4]
            elif char_counter == 31:
                char_buffer.next = val1_buffer[4:0]
            elif char_counter == 32:
                char_buffer.next = val2_buffer[64:60]
            elif char_counter == 33:
                char_buffer.next = val2_buffer[60:56]
            elif char_counter == 34:
                char_buffer.next = val2_buffer[56:52]
            elif char_counter == 35:
                char_buffer.next = val2_buffer[52:48]
            elif char_counter == 36:
                char_buffer.next = val2_buffer[48:44]
            elif char_counter == 37:
                char_buffer.next = val2_buffer[44:40]
            elif char_counter == 38:
                char_buffer.next = val2_buffer[40:36]
            elif char_counter == 39:
                char_buffer.next = val2_buffer[36:32]
            elif char_counter == 40:
                char_buffer.next = val2_buffer[32:28]
            elif char_counter == 41:
                char_buffer.next = val2_buffer[28:24]
            elif char_counter == 42:
                char_buffer.next = val2_buffer[24:20]
            elif char_counter == 43:
                char_buffer.next = val2_buffer[20:16]
            elif char_counter == 44:
                char_buffer.next = val2_buffer[16:12]
            elif char_counter == 45:
                char_buffer.next = val2_buffer[12:8]
            elif char_counter == 46:
                char_buffer.next = val2_buffer[8:4]
            elif char_counter == 47:
                char_buffer.next = val2_buffer[4:0]
            elif char_counter == 48:
                char_buffer.next = val3_buffer[64:60]
            elif char_counter == 49:
                char_buffer.next = val3_buffer[60:56]
            elif char_counter == 50:
                char_buffer.next = val3_buffer[56:52]
            elif char_counter == 51:
                char_buffer.next = val3_buffer[52:48]
            elif char_counter == 52:
                char_buffer.next = val3_buffer[48:44]
            elif char_counter == 53:
                char_buffer.next = val3_buffer[44:40]
            elif char_counter == 54:
                char_buffer.next = val3_buffer[40:36]
            elif char_counter == 55:
                char_buffer.next = val3_buffer[36:32]
            elif char_counter == 56:
                char_buffer.next = val3_buffer[32:28]
            elif char_counter == 57:
                char_buffer.next = val3_buffer[28:24]
            elif char_counter == 58:
                char_buffer.next = val3_buffer[24:20]
            elif char_counter == 59:
                char_buffer.next = val3_buffer[20:16]
            elif char_counter == 60:
                char_buffer.next = val3_buffer[16:12]
            elif char_counter == 61:
                char_buffer.next = val3_buffer[12:8]
            elif char_counter == 62:
                char_buffer.next = val3_buffer[8:4]
            elif char_counter == 63:
                char_buffer.next = val3_buffer[4:0]
            elif char_counter == 64:
                char_buffer.next = val4_buffer[64:60]
            elif char_counter == 65:
                char_buffer.next = val4_buffer[60:56]
            elif char_counter == 66:
                char_buffer.next = val4_buffer[56:52]
            elif char_counter == 67:
                char_buffer.next = val4_buffer[52:48]
            elif char_counter == 68:
                char_buffer.next = val4_buffer[48:44]
            elif char_counter == 69:
                char_buffer.next = val4_buffer[44:40]
            elif char_counter == 70:
                char_buffer.next = val4_buffer[40:36]
            elif char_counter == 71:
                char_buffer.next = val4_buffer[36:32]
            elif char_counter == 72:
                char_buffer.next = val4_buffer[32:28]
            elif char_counter == 73:
                char_buffer.next = val4_buffer[28:24]
            elif char_counter == 74:
                char_buffer.next = val4_buffer[24:20]
            elif char_counter == 75:
                char_buffer.next = val4_buffer[20:16]
            elif char_counter == 76:
                char_buffer.next = val4_buffer[16:12]
            elif char_counter == 77:
                char_buffer.next = val4_buffer[12:8]
            elif char_counter == 78:
                char_buffer.next = val4_buffer[8:4]
            elif char_counter == 79:
                char_buffer.next = val4_buffer[4:0]
            elif char_counter == 80:
                char_buffer.next = val5_buffer[64:60]
            elif char_counter == 81:
                char_buffer.next = val5_buffer[60:56]
            elif char_counter == 82:
                char_buffer.next = val5_buffer[56:52]
            elif char_counter == 83:
                char_buffer.next = val5_buffer[52:48]
            elif char_counter == 84:
                char_buffer.next = val5_buffer[48:44]
            elif char_counter == 85:
                char_buffer.next = val5_buffer[44:40]
            elif char_counter == 86:
                char_buffer.next = val5_buffer[40:36]
            elif char_counter == 87:
                char_buffer.next = val5_buffer[36:32]
            elif char_counter == 88:
                char_buffer.next = val5_buffer[32:28]
            elif char_counter == 89:
                char_buffer.next = val5_buffer[28:24]
            elif char_counter == 90:
                char_buffer.next = val5_buffer[24:20]
            elif char_counter == 91:
                char_buffer.next = val5_buffer[20:16]
            elif char_counter == 92:
                char_buffer.next = val5_buffer[16:12]
            elif char_counter == 93:
                char_buffer.next = val5_buffer[12:8]
            elif char_counter == 94:
                char_buffer.next = val5_buffer[8:4]
            elif char_counter == 95:
                char_buffer.next = val5_buffer[4:0]
            elif char_counter == 96:
                char_buffer.next = val6_buffer[64:60]
            elif char_counter == 97:
                char_buffer.next = val6_buffer[60:56]
            elif char_counter == 98:
                char_buffer.next = val6_buffer[56:52]
            elif char_counter == 99:
                char_buffer.next = val6_buffer[52:48]
            elif char_counter == 100:
                char_buffer.next = val6_buffer[48:44]
            elif char_counter == 101:
                char_buffer.next = val6_buffer[44:40]
            elif char_counter == 102:
                char_buffer.next = val6_buffer[40:36]
            elif char_counter == 103:
                char_buffer.next = val6_buffer[36:32]
            elif char_counter == 104:
                char_buffer.next = val6_buffer[32:28]
            elif char_counter == 105:
                char_buffer.next = val6_buffer[28:24]
            elif char_counter == 106:
                char_buffer.next = val6_buffer[24:20]
            elif char_counter == 107:
                char_buffer.next = val6_buffer[20:16]
            elif char_counter == 108:
                char_buffer.next = val6_buffer[16:12]
            elif char_counter == 109:
                char_buffer.next = val6_buffer[12:8]
            elif char_counter == 110:
                char_buffer.next = val6_buffer[8:4]
            elif char_counter == 111:
                char_buffer.next = val6_buffer[4:0]
            elif char_counter == 112:
                char_buffer.next = val7_buffer[64:60]
            elif char_counter == 113:
                char_buffer.next = val7_buffer[60:56]
            elif char_counter == 114:
                char_buffer.next = val7_buffer[56:52]
            elif char_counter == 115:
                char_buffer.next = val7_buffer[52:48]
            elif char_counter == 116:
                char_buffer.next = val7_buffer[48:44]
            elif char_counter == 117:
                char_buffer.next = val7_buffer[44:40]
            elif char_counter == 118:
                char_buffer.next = val7_buffer[40:36]
            elif char_counter == 119:
                char_buffer.next = val7_buffer[36:32]
            elif char_counter == 120:
                char_buffer.next = val7_buffer[32:28]
            elif char_counter == 121:
                char_buffer.next = val7_buffer[28:24]
            elif char_counter == 122:
                char_buffer.next = val7_buffer[24:20]
            elif char_counter == 123:
                char_buffer.next = val7_buffer[20:16]
            elif char_counter == 124:
                char_buffer.next = val7_buffer[16:12]
            elif char_counter == 125:
                char_buffer.next = val7_buffer[12:8]
            elif char_counter == 126:
                char_buffer.next = val7_buffer[8:4]
            elif char_counter == 127:
                char_buffer.next = val7_buffer[4:0]

            state.next = st_dr.rom_char_slice
            
        elif state == st_dr.rom_char_slice:
            char_rom_address.next = char_buffer * 8 + char_slice_counter
            state.next = st_dr.load_char_slice
        elif state == st_dr.load_char_slice:
            latch_out.next = 0
            data_out.next = char_rom_data
            dcn_out.next = 1 # sending data, not a command
            state.next = st_dr.latch_char_slice
        elif state == st_dr.latch_char_slice:
            if spi_busy_in == 0: # spi is idle, push next byte to the spi
                latch_out.next = 1
                if char_slice_counter < 7:
                    char_slice_counter.next = char_slice_counter + 1
                    state.next = st_dr.rom_char_slice
                else:
                    char_slice_counter.next = 0
                    if char_counter < 127:
                        char_counter.next = char_counter + 1
                        state.next = st_dr.load_char
                    else:
                        state.next = st_dr.setup_contrast_control_1
                        char_counter.next = 0
            else:
                state.next = st_dr.latch_char_slice
        else:
            raise ValueError("Undefined state")
            
    return fsm_dr


