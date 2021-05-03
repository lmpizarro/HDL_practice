from nmigen.back.pysim import *
from modules import ALU, REG, REG16
from nmigen.cli import main
from nmigen import ResetSignal
from utils.utils import print_alu

def simulate_alu():

    alu = ALU(width=16)
    main(alu, ports=[alu.op, alu.a, alu.b, alu.o])

    sim =  Simulator(alu, vcd_file = open( 'test.vcd', 'w' ) )
    def proc():
      for i in range( 4 ):
          for j in range(4):
                yield alu.op.eq(1)
                yield alu.a.eq(i)
                yield alu.b.eq(j)
                yield Delay()
                print_alu(i, j, (yield alu.o))

    sim.add_process( proc )
    sim.run()

    print()

def simulate_reg():
    reg = REG(width=16)
    main(reg, ports=[reg.en, reg.data, reg.q])

    print()
    sim =  Simulator(reg, vcd_file = open( 'test.vcd', 'w' ) )
    def proc2():
        yield reg.en.eq(0)
        yield reg.data.eq(9)
        yield Tick()
        
        yield reg.en.eq(1)
        yield Tick()
        yield Tick()

        yield reg.en.eq(0)
        yield Tick()

        print_alu(0, 3, (yield reg.q))

        yield reg.en.eq(1)
        yield reg.data.eq(4)

        yield Tick()
        print_alu(0, 3, (yield reg.q))
        yield Delay(.25e-6)

        yield reg.en.eq(0)
        yield reg.data.eq(0)

        yield Tick()
        print_alu(0, 3, (yield reg.q))
        yield
        yield reg.data.eq(4)

        yield Tick()
        print_alu(0, 3, (yield reg.q))
        yield


        yield reg.en.eq(0)
        yield reg.data.eq(0)

        yield Tick()
        print_alu(0, 3, (yield reg.q))
        yield

        yield reg.en.eq(1)
        yield reg.data.eq(0)

        yield Tick()
        print_alu(0, 3, (yield reg.q))
        yield


        yield reg.en.eq(1)
        
        yield reg.data.eq(0)

        yield Tick()
        print_alu(0, 3, (yield reg.q))
        yield


    sim.add_clock(1e-6)
    sim.add_sync_process( proc2 )
    sim.run()



if __name__ == "__main__":
    reg16 = REG16()
    main(reg16, ports=[reg16.wen, reg16.wdata, reg16.qq])

    print()
    sim =  Simulator(reg16, vcd_file = open( 'test.vcd', 'w' ) )

    def proc2():
        yield reg16.wen[0].eq(0)
        yield reg16.wdata[0].eq(9)
        yield Tick()

        print('0 9', (yield reg16.qq[0]))
        yield reg16.wen[0].eq(1)
        
        yield Tick()
        yield Tick()
        print('1 9', (yield reg16.qq[0]))

        yield reg16.wen[3].eq(0)
        yield reg16.wdata[3].eq(99)
        yield Tick()

        print((yield reg16.qq[3]))
        yield reg16.wen[3].eq(1)
        
        yield Tick()
        yield Tick()
        print((yield reg16.qq[3]))
        print((yield reg16.qq[0]))


    sim.add_clock(1e-6)
    sim.add_sync_process( proc2 )
    sim.run()

