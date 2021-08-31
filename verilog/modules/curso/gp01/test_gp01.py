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
async def my_second_test(dut):
    """Try accessing the design."""

    dut._log.info("Running test...")

    cocotb.fork(generate_clock(dut))  # run the clock "in the background"

    await Timer(2, units="ns")  # wait a bit
    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

    dut._log.info("Resetting DUT")

    dut.i_rst_n <= 0
    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

    dut.i_rst_n <= 1
    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

    dut._log.info(f"my_signal_1 is  {dut.o_data.value}")
    assert dut.o_overflow.value == 0, "my_signal_2[0] is not 0!"

    dut._log.info("Running test...done")

    dut.i_data1 = 1
    dut.i_data2 = 1
    dut.i_sel = 0
    for i in range(10):
        await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
        dut.i_sel = 1
        await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
        dut.i_sel = 2


