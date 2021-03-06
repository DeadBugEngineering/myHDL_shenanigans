# generated by de0NanoADC_genModel.py, manual changes are not recommended.

from myhdl import *

SAMPLE_SEQUENCE = (0,1,2,3,4,5,6,7)

@block
def rom(channel, sample_slot, SAMPLE_SEQUENCE):
    @always_comb
    def read():
        channel.next = SAMPLE_SEQUENCE[int(sample_slot)]
    return read