from nmigen.back.pysim import *
from modules import ALU, MUX, MUX4, REG
from nmigen.cli import main

if __name__ == "__main__":
    alu = ALU(width=16)
    main(alu, ports=[alu.op, alu.a, alu.b, alu.o])

    def print_alu(i, j, out):
        print(i, j, out)

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

    mux = MUX(width=16)

    sim =  Simulator(mux, vcd_file = open( 'test.vcd', 'w' ) )
    def proc():
        for i in range( 4 ):
            yield mux.op.eq(0)
            yield mux.a.eq(i)
            yield mux.b.eq(9)
            yield Delay()
            print_alu(i, 9, (yield mux.o))

            yield mux.op.eq(1)
            yield mux.a.eq(i)
            yield mux.b.eq(9)
            yield Delay()
            print_alu(i, 9, (yield mux.o))


    sim.add_process( proc )
    sim.run()

    mux4 = MUX4(width=16)
    main(mux4, ports=[mux4.sel, mux4.a, mux4.b, mux4.c, mux4.d, mux4.o])

    print()
    print("....")
    sim =  Simulator(mux4, vcd_file = open( 'test.vcd', 'w' ) )
    def proc2():
        for i in range( 4 ):
            yield mux4.sel.eq(1)

            yield mux4.a.eq(i)
            yield mux4.b.eq(2)
            yield mux4.c.eq(5)
            yield mux4.d.eq(9)

            yield Delay()
            print_alu(i, 3, (yield mux4.o))

    sim.add_process( proc2 )
    sim.run()

    reg = REG(width=16)
    main(reg, ports=[reg.en, reg.data, reg.q])

    print()
    print(".uuu...")
    sim =  Simulator(reg, vcd_file = open( 'test.vcd', 'w' ) )
    def proc2():
        yield reg.en.eq(0)
        yield reg.data.eq(9)

        yield Tick()
        print_alu(0, 3, (yield reg.q))
        yield

        yield reg.en.eq(1)
        yield reg.data.eq(4)

        yield Tick()
        print_alu(0, 3, (yield reg.q))
        yield

        yield reg.en.eq(1)
        yield reg.data.eq(4)

        yield Tick()
        print_alu(0, 3, (yield reg.q))
        yield

        yield reg.en.eq(1)
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
        yield ResetInserter()
        yield reg.data.eq(0)

        yield Tick()
        print_alu(0, 3, (yield reg.q))
        yield





    sim.add_clock(1e-6)
    sim.add_sync_process( proc2 )
    sim.run()


