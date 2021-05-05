from nmigen import *
import math


class ALU(Elaboratable):

    def __init__(self, ccr=False):

        self.ccr_elab = ccr
        self.X = Signal(16, reset=0)
        self.Y = Signal(16, reset=0)
        self.Z = Signal(16, reset=0)
        self.CTR = Signal(6, reset=0)  # zx nx zy ny f no
        if self.ccr_elab:
            self.CND = Signal(2, reset=0)  # zr ng

    def elaborate(self, platform):
        m = Module()

        with m.Switch(self.CTR):
            with m.Case(0b101010): m.d.comb += [self.Z.eq(0)]
            with m.Case(0b111111): m.d.comb += [self.Z.eq(1)] 
            with m.Case(0b111010): m.d.comb += [self.Z.eq(-1)]
            with m.Case(0b001100): m.d.comb += [self.Z.eq(self.X)]
            with m.Case(0b110000): m.d.comb += [self.Z.eq(self.Y)]
            with m.Case(0b001101): m.d.comb += [self.Z.eq(~self.X)]
            with m.Case(0b110001): m.d.comb += [self.Z.eq(~self.Y)]
            with m.Case(0b001111): m.d.comb += [self.Z.eq(-self.X)]
            with m.Case(0b110011): m.d.comb += [self.Z.eq(-self.Y)]
            with m.Case(0b011111): m.d.comb += [self.Z.eq(self.X + 1)]
            with m.Case(0b110111): m.d.comb += [self.Z.eq(self.Y + 1)]
            with m.Case(0b001110): m.d.comb += [self.Z.eq(self.X - 1)]
            with m.Case(0b110010): m.d.comb += [self.Z.eq(self.Y - 1)]
            with m.Case(0b000010): m.d.comb += [self.Z.eq(self.X + self.Y)]
            with m.Case(0b010011): m.d.comb += [self.Z.eq(self.X - self.Y)]
            with m.Case(0b000111): m.d.comb += [self.Z.eq(self.Y - self.X)]
            with m.Case(0b000000): m.d.comb += [self.Z.eq(self.X & self.Y)]
            with m.Case(0b010101): m.d.comb += [self.Z.eq(self.X | self.Y)]
            with m.Case(): m.d.comb += self.Z.eq(0)

        if self.ccr_elab:
            with m.If(self.Z < 0):
                m.d.comb += self.CND.eq(1)
            with m.Elif(self.Z == 0):
                m.d.comb += self.CND.eq(2)
            with m.Else():
                m.d.comb += self.CND.eq(0)
        """
                zr ng
        >  0  ~or cnd
        =  0  cnd_1
        >= 0  cnd_1 or ~ cnd_0
        <  0  cnd_0
        != 0   ~cnd_1
        <= 0  cnd_1 or cnd_0
        """

        return m
        

class Hack(Elaboratable):

    def __init__(self):

        self.enWrtRAM = Signal()       # output enM/writeM

        self.addressRAM = Signal(16)   # output addressM
        self.instruction = Signal(16)  # input
        self.dataReadRAM  = Signal(16) # input     inM
        self.dataWriteRAM = Signal(16) # output    outM
        self.PC = Signal(16)           # output

        self.A = Signal(16)
        self.D = Signal(16)

        self.Alu = ALU()

    def elaborate(self, platform):
        m = Module()

        m.submodules.Alu = self.Alu

        jump_ins = self.instruction[13:16]
        enA = self.instruction[10]
        enM = self.instruction[11]
        enD = self.instruction[12]
        ctralu = self.instruction[4:10]
        inA = Signal(16)
        enPC = Signal()
        jump_cond = Signal()

        m.d.comb += self.Alu.X.eq(self.D)
        m.d.comb += self.enWrtRAM.eq(enM)
        m.d.comb += self.dataWriteRAM.eq(self.Alu.Z)
        m.d.comb += self.addressRAM.eq(self.A)

        # MUX ALU_Y A/Memoria
        with m.If(self.instruction[3] == 1):
            m.d.comb += self.Alu.Y.eq(self.dataReadRAM)
        with m.Else():
            m.d.comb += self.Alu.Y.eq(self.A)

        # MUX A instruction/ALU Z
        with m.If(self.instruction[0] == 1):
            m.d.comb += inA.eq(self.Alu.Z)
        with m.Else():
            m.d.comb += inA.eq(self.instruction)

        # Load D
        with m.If(enD):
            m.d.sync += self.D.eq(self.Alu.Z)
        
        # Load A
        with m.If(enA):
            m.d.sync += self.A.eq(inA)

        with m.If(jump_ins == 0b111):
            m.d.comb += jump_cond.eq(1)
        with m.Elif(jump_ins == 0b000):
            m.d.comb += jump_cond.eq(0)
        with m.Elif(jump_ins == 1):
            with m.If(self.Alu.Z > 0):
                m.d.comb += jump_cond.eq(1)
        with m.Elif(jump_ins == 2):
            with m.If(self.Alu.Z == 0):
                m.d.comb += jump_cond.eq(1)
        with m.Elif(jump_ins == 3):
            with m.If(self.Alu.Z >= 0):
                m.d.comb += jump_cond.eq(1)
        with m.Elif(jump_ins == 4):
            with m.If(self.Alu.Z < 0):
                m.d.comb += jump_cond.eq(1)
        with m.Elif(jump_ins == 5):
            with m.If(self.Alu.Z != 0):
                m.d.comb += jump_cond.eq(1)
        with m.Elif(jump_ins == 6):
            with m.If(self.Alu.Z <= 0):
                m.d.comb += jump_cond.eq(1)
        with m.Else():
            m.d.comb += jump_cond.eq(0)            


        with m.If(jump_cond == 1):
            m.d.comb += enPC.eq(1)
        with m.Else():
            m.d.comb += enPC.eq(0)

        # increment PC or Load PC with register A        
        with m.If(enPC):
            m.d.sync += self.PC.eq(self.A)
        with m.Else():
            m.d.sync += self.PC.eq(self.PC + 1)

        return m

class Soc(Elaboratable):

    def __init__(self):
        self.pcSrc = Signal()

        self.regDest  = Signal()
        self.jump = Signal()
        self.branch = Signal()
        self.memRead = Signal()
        self.memToReg = Signal()
        self.aluOp  = Signal(4)
        self.memWrite = Signal()
        self.aluSrc = Signal()
        self.regWrite = Signal()

if __name__== "__main__":
    alu16 = ALU(ccr=True)
    ports = [alu16.X, alu16.Y, alu16.Z, alu16.CTR, alu16.CND]


    from nmigen.back import verilog
    print(verilog.convert(alu16, strip_internal_attrs=True, ports=ports))

    hack = Hack()
    ports = [hack.addressRAM,
             hack.dataReadRAM,
             hack.dataWriteRAM,
             hack.PC,
             hack.enWrtRAM,
             hack.instruction]
    print(verilog.convert(hack, strip_internal_attrs=True, ports=ports))
