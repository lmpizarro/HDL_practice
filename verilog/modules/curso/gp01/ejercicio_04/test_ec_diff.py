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

    dut.i_x = 0
    dut.i_rst <= 1
    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

    dut.i_rst <= 0
    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

    dut._log.info(f"my_signal_1 is  {dut.o_y.value}")

    dut.i_x = 4
    output = []
    for i in range(40):
        await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
        dut.i_x = 4
        output.append(dut.o_y.value)
    
    print(output)
