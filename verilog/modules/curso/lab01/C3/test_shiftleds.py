import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.triggers import FallingEdge

async def generate_clock(dut):
    """Generate clock pulses."""

    for cycle in range(40):
        dut.clock <= 0
        await Timer(1, units="ns")
        dut.clock <= 1
        await Timer(1, units="ns")

@cocotb.test()
async def my_second_test(dut):
    """Try accessing the design."""

    dut._log.info("Running test...")

    cocotb.fork(generate_clock(dut))  # run the clock "in the background"

    await Timer(2, units="ns")  # wait a bit
    await FallingEdge(dut.clock)  # wait for falling edge/"negedge"

    dut._log.info("Resetting DUT")

    for i in range(2):
        dut.i_reset <= 1
        await FallingEdge(dut.clock)  # wait for falling edge/"negedge"
        dut.i_reset <= 0
        await FallingEdge(dut.clock)  # wait for falling edge/"negedge"

    dut._log.info(f"my_signal_1 is  {dut.o_led.value}")
    # 
    # assert dut.o_led_b.value == 0, "my_signal_2[0] is not 0!"

    dut._log.info("Running test...done")

    dut.i_sw = 1 # 000x 001 010x 011 100x 101 110x 111
    for i in range(200):
        await FallingEdge(dut.clock)  # wait for falling edge/"negedge"
        dut._log.info(f"o_led is  {dut.o_led.value}")
        dut._log.info(f"o_led_g is  {dut.o_led_g.value}")
        dut._log.info(f"o_led_b is  {dut.o_led_b.value}")



