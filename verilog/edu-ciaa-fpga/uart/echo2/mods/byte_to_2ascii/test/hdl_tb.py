# -*- coding: utf-8 -*-
import cocotb
from cocotb.triggers import Timer, FallingEdge
from cocotb.regression import TestFactory

async def generate_clock(dut):
    """Generate clock pulses."""

    for cycle in range(10):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")


@cocotb.test()
async def run_test(dut):
  cocotb.fork(generate_clock(dut))  # run the clock "in the background"
  dut.i_next_out = 0
  await Timer(2, units="ns")  # wait a bit
  dut.i_data = 124
  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
  await Timer(2, units="ns")  # wait a bit
  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
  dut.i_next_out = 1
  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
  dut.i_next_out = 0

  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
  await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

  dut.i_next_out = 1
  for i in range(40):
      await FallingEdge(dut.clk)  # wait for falling edge/"negedge"


# Register the test.
factory = TestFactory(run_test)
factory.generate_tests()
    