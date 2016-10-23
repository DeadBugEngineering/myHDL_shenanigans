// File: rom.v
// Generated by MyHDL 1.0dev
// Date: Thu Oct 13 22:12:15 2016


`timescale 1ns/10ps

module rom (
    dout,
    addr
);


output [7:0] dout;
reg [7:0] dout;
input [6:0] addr;




always @(addr) begin: ROM_READ
    case (addr)
        0: dout = 0;
        1: dout = 0;
        2: dout = 62;
        3: dout = 81;
        4: dout = 73;
        5: dout = 69;
        6: dout = 62;
        7: dout = 0;
        8: dout = 0;
        9: dout = 0;
        10: dout = 0;
        11: dout = 66;
        12: dout = 127;
        13: dout = 64;
        14: dout = 0;
        15: dout = 0;
        16: dout = 0;
        17: dout = 0;
        18: dout = 66;
        19: dout = 97;
        20: dout = 81;
        21: dout = 73;
        22: dout = 70;
        23: dout = 0;
        24: dout = 0;
        25: dout = 0;
        26: dout = 34;
        27: dout = 65;
        28: dout = 73;
        29: dout = 73;
        30: dout = 93;
        31: dout = 54;
        32: dout = 0;
        33: dout = 31;
        34: dout = 16;
        35: dout = 16;
        36: dout = 124;
        37: dout = 16;
        38: dout = 16;
        39: dout = 0;
        40: dout = 0;
        41: dout = 0;
        42: dout = 71;
        43: dout = 69;
        44: dout = 69;
        45: dout = 109;
        46: dout = 57;
        47: dout = 0;
        48: dout = 0;
        49: dout = 60;
        50: dout = 110;
        51: dout = 75;
        52: dout = 73;
        53: dout = 73;
        54: dout = 49;
        55: dout = 0;
        56: dout = 0;
        57: dout = 0;
        58: dout = 65;
        59: dout = 97;
        60: dout = 49;
        61: dout = 25;
        62: dout = 15;
        63: dout = 0;
        64: dout = 0;
        65: dout = 0;
        66: dout = 54;
        67: dout = 73;
        68: dout = 73;
        69: dout = 73;
        70: dout = 54;
        71: dout = 0;
        72: dout = 0;
        73: dout = 0;
        74: dout = 70;
        75: dout = 77;
        76: dout = 73;
        77: dout = 105;
        78: dout = 57;
        79: dout = 30;
        80: dout = 0;
        81: dout = 120;
        82: dout = 30;
        83: dout = 9;
        84: dout = 9;
        85: dout = 9;
        86: dout = 30;
        87: dout = 120;
        88: dout = 0;
        89: dout = 127;
        90: dout = 73;
        91: dout = 73;
        92: dout = 73;
        93: dout = 73;
        94: dout = 54;
        95: dout = 0;
        96: dout = 0;
        97: dout = 60;
        98: dout = 102;
        99: dout = 67;
        100: dout = 65;
        101: dout = 65;
        102: dout = 99;
        103: dout = 0;
        104: dout = 0;
        105: dout = 0;
        106: dout = 127;
        107: dout = 65;
        108: dout = 65;
        109: dout = 99;
        110: dout = 62;
        111: dout = 0;
        112: dout = 0;
        113: dout = 0;
        114: dout = 127;
        115: dout = 73;
        116: dout = 73;
        117: dout = 65;
        118: dout = 65;
        119: dout = 0;
        120: dout = 0;
        121: dout = 0;
        122: dout = 127;
        123: dout = 9;
        124: dout = 9;
        125: dout = 1;
        126: dout = 1;
        default: dout = 0;
    endcase
end

endmodule
