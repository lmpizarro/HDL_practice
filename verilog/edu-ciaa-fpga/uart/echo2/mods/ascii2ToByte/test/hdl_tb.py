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


@cocotb.test()
async def run_test(dut):

    tb = TB(dut)
    await Timer(1)
    tb.dut._log.info('resetting the module') #logging helpful messages

    await tb.cycle_reset()

    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    tb.dut.i_data <= 0x30 
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    tb.dut.i_load <= 0
    for i in range(2):
        await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    tb.dut.i_data <= 0x32 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    tb.dut.i_data <= 0x00 
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    tb.dut.i_data <= 0x36 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    tb.dut.i_data <= 0x39 
    tb.dut.i_load <= 1
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    tb.dut.i_load <= 0
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"
    await RisingEdge(dut.clk)  # wait for falling edge/"negedge"

    for i in range(20):
          await RisingEdge(dut.clk)  # wait for falling edge/"negedge"

