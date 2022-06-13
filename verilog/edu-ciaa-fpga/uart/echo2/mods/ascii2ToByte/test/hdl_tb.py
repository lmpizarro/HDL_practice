# -*- coding: utf-8 -*-
import cocotb
from cocotb.triggers import Timer, FallingEdge, RisingEdge
import logging
from cocotb.clock import Clock

class TB(object):
#The init method of this class can be used to do some setup like logging etc, start the 
#toggling of the clock and also initialize the internal to their pre-reset vlaue.
    def __init__(self, dut):
        self.dut = dut
        self.log = logging.getLogger('cocotb_tb')
        self.log.setLevel(logging.DEBUG)
				
				#start the clock as a parallel process.
        cocotb.fork(Clock(dut.clk, 10, units="us").start())

    async def cycle_reset(self):
        self.dut.i_clr = 0
        self.dut.i_load = 0
        await RisingEdge(self.dut.clk)
        await RisingEdge(self.dut.clk)
        self.dut.i_clr = 1
        								#signal inside the design
        await RisingEdge(self.dut.clk)
        await RisingEdge(self.dut.clk)
        self.dut.i_clr = 0


async def run_test_streamDecoder(dut:TB):

    tb = TB(dut)
    await Timer(1)
    tb.dut._log.info('resetting the module') #logging helpful messages

    await tb.cycle_reset()

    # tb.dut.i_data <= 0x57 
    # tb.dut.i_load <= 1
    # await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    # tb.dut.i_load <= 0
    # await RisingEdge(dut.clk)  # wait for rising edge/"negedge"


    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    # Address
    tb.dut.i_data <= 0x30 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x32 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    # Data
    tb.dut.i_data <= 0x36 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x39 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    

    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"

    for i in range(20):
          await RisingEdge(dut.clk)  # wait for rising edge/"negedge"

async def run_test_cmd_deco(dut:TB):
    tb = TB(dut)
    await Timer(1)
    tb.dut._log.info('resetting the module') #logging helpful messages

    # await tb.cycle_reset()

    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"

    tb.dut.i_data <= 0x57 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    # 
    tb.dut.i_data <= 0x52
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    # 
    tb.dut.i_data <= 0x58 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    
    tb.dut.i_data <= 0x3a 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x2e 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x44 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x40 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"

@cocotb.test()
async def run_test_top(dut:TB):
    tb = TB(dut)
    await Timer(1)
    tb.dut._log.info('resetting the module') #logging helpful messages

    tb.dut.i_load <= 0 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x57 
    tb.dut.i_load <= 1 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"

    tb.dut.i_load <= 0 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x30 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x32 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x36 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x38 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x00 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x00 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
 
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x52 
    tb.dut.i_load <= 1 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"

    tb.dut.i_load <= 0 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x30 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x36 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"

    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x00 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"

    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x00 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
 
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
 
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x3a 
    tb.dut.i_load <= 1
    
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x2e 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    tb.dut.i_data <= 0x44 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
    await RisingEdge(dut.clk)  # wait for rising edge/"negedge"
 