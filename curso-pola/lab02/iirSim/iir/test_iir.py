import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.triggers import FallingEdge
from signal_mgmt import read_mem
import os


async def generate_clk(dut, length=200):
    """Generate clk pulses."""

    for cycle in range(length):
        dut.i_clk <= 0
        await Timer(1, units="ns")
        dut.i_clk <= 1
        await Timer(1, units="ns")


@cocotb.test()
async def test_filtro_iir(dut):
    """Try accessing the design."""

    folder = '/home/lmpizarro/devel/project/HDL/verilog/verilog/modules/curso/lab02/lab/rtl/'
    mem_values = read_mem(folder, file='sig.hex')
    dut._log.info("Running test...")

    cocotb.fork(generate_clk(dut, len(mem_values) + 10))  # run the clk "in the background"

    await Timer(2, units="ns")  # wait a bit
    await FallingEdge(dut.i_clk)  # wait for falling edge/"negedge"

    dut._log.info("Resetting DUT")

    for i in range(2):
        dut.i_rst <= 1
        await FallingEdge(dut.i_clk)  # wait for falling edge/"negedge"
        dut.i_rst <= 0
        await FallingEdge(dut.i_clk)  # wait for falling edge/"negedge"
        dut.i_rst <= 1
        await FallingEdge(dut.i_clk)  # wait for falling edge/"negedge"


    dut._log.info(f"o_data =  {dut.o_data.value}")
    # 
    # assert dut.o_led_b.value == 0, "my_signal_2[0] is not 0!"

    dut._log.info("Running test...done")

    # dut.i_en = 1 # 000x 001 010x 011 100x 101 110x 111
    dut.i_data = 0
    output_values = []
    mem_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    for val in mem_values:
        await FallingEdge(dut.i_clk)  # wait for falling edge/"negedge"
        o_data = dut.o_data.value
        dut._log.info(f"o_data =  {o_data}")
        dut.i_data = val
        try:
            output_values.append(f'{hex(int(o_data))[2:].upper()}\n')
        except Exception as e:
            pass

    with open(os.path.join(folder, 'out.hex'), 'w') as fp:
        for o in output_values:
            fp.write(o)






