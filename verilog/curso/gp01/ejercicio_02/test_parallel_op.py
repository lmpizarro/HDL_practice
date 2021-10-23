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

 

    dut.i_dataA = 1
    dut.i_dataB = 1
    dut.i_sel = 1

    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
    dut._log.info(f'dut ouput {dut.o_dataC}')


    dut.i_dataA = 1
    dut.i_dataB = 1
    dut.i_sel = 0

    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
    dut._log.info(f'dut ouput {dut.o_dataC}')

    dut.i_dataA = 1
    dut.i_dataB = 0
    dut.i_sel = 2

    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
    dut._log.info(f'dut ouput {dut.o_dataC}')

    dut.i_dataA = 1
    dut.i_dataB = 0
    dut.i_sel = 3

    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"
    dut._log.info(f'dut ouput {dut.o_dataC}')
