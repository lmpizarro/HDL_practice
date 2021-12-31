import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.triggers import FallingEdge

async def generate_clock(dut):
    """Generate clock pulses."""

    for cycle in range(40):
        dut.clk <= 0
        await Timer(1, units="ns")
        dut.clk <= 1
        await Timer(1, units="ns")

@cocotb.test()
async def test_multiplier(dut):
    """Try accessing the design."""

    dut._log.info("Running test...")

    cocotb.fork(generate_clock(dut))  # run the clock "in the background"

    await Timer(2, units="ns")  # wait a bit
    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

    dut._log.info("Resetting DUT")

    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

    dut._log.info(f"out is  {dut.out.value}")

    dut._log.info("Running test...done")

    dut.A = 127
    dut.B = 127
    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
    dut._log.info(f"out is  {dut.out.value}")
    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"


