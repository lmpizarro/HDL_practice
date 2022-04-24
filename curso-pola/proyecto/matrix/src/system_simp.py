from migen import Signal, Module, If, Array, run_simulation
from migen.fhdl import verilog
from pathlib import Path


class Estimator(Module):
    def __init__(self, width=16, n_out=1, n_inp=1, n_stt=2):

        self.register_size = n_stt**2 + n_stt * 3
        self.en_wr_data = Signal(name='en_wr_data')
        self.data = Signal((width, True),name='data')
        self.addr_data = Signal(4, name='addr_data')

        self.en_wr_meas = Signal()
        self.inp_d = Signal((width, True))

        self.end_cycle = Signal(reset=1)
        self.out_q = Signal((width, True))

        self.mr0 = Signal((2*width, True))
        self.mr1 = Signal((2*width, True))
        self.xestimate0 = Signal((2*width+1, True))
        self.xestimate1 = Signal((2*width+1, True))
        self.yestimate = Signal((2*width+1, True))
        self.yerror = Signal((2*width+1, True))
        
        self.SystemM = Array(Signal((width, True)) for _ in range(self.register_size))
        # matrix A
        a0 = self.SystemM[0]
        a1 = self.SystemM[1]
        a2= self.SystemM[2]
        a3 = self.SystemM[3]
        # matrix H
        h0= self.SystemM[4]
        h1 = self.SystemM[5]
        # Gain
        k0= self.SystemM[6]
        k1 = self.SystemM[7]
        # states        
        x0 = self.SystemM[8]
        x1 = self.SystemM[9]

        self.y_meas = Signal((width, True))

        begin_cycle = Signal()
        counter_steps_process = Signal(5)
        self.sync += If(
                            self.en_wr_meas & self.end_cycle, 
                            self.y_meas.eq(self.inp_d),
                            begin_cycle.eq(1), 
                            self.end_cycle.eq(0)
                        )

        self.sync += If(
                            begin_cycle==1, 
                            counter_steps_process.eq(counter_steps_process+1)
                        )

        self.sync += If(
                            self.en_wr_data,
                            self.SystemM[self.addr_data].eq(self.data)
                        )

        # Multiply Ax0 row1 x0
        self.sync += If(
                            counter_steps_process==1, 
                            self.mr0.eq(a0*x0), 
                            self.mr1.eq(a1*x1)
                        )
        # xestimate0
        self.sync += If(
                            counter_steps_process==2, 
                            self.xestimate0.eq(self.mr0+self.mr1)
                        )
        # Multiply Ax0 row1 x0
        self.sync += If(
                            counter_steps_process==3,
                            self.mr0.eq(a2*x0), 
                            self.mr1.eq(a3*x1)
                        )
        # xestimate1
        self.sync += If(
                            counter_steps_process==4,
                            self.xestimate1.eq(self.mr0+self.mr1)
                        )
            
        self.sync += If(
                            counter_steps_process==5,
                            self.mr0.eq(h0*self.xestimate0), 
                            self.mr1.eq(h1*self.xestimate1)
                        )

        self.sync += If(
                            counter_steps_process==6,
                            self.yestimate.eq(self.mr0+self.mr1)
                        )

        self.sync += If(
                            counter_steps_process==7,
                            self.yerror.eq(self.y_meas-self.yestimate)
                        )
 
        self.sync += If(
                            counter_steps_process==8,
                            self.mr0.eq(k0*self.yerror), 
                            self.mr1.eq(k1*self.yerror)
                        )

        self.sync += If(
                            counter_steps_process==9,
                            x0.eq(self.xestimate0 + self.mr0), 
                            x1.eq(self.xestimate1 + self.mr1)
                        )
        
        self.sync += If(
                            counter_steps_process == 10, 
                            counter_steps_process.eq(0), 
                            begin_cycle.eq(0), 
                            self.end_cycle.eq(1)
                        )

        self.ios = {
                    self.en_wr_meas, 
                    self.inp_d,

                    self.end_cycle,
                    self.out_q,

                    self.en_wr_data,
                    self.addr_data,
                    self.data
                    }       

def estimator_tb(estmtr: Estimator):
    yield estmtr.en_wr_data.eq(0)
    yield estmtr.en_wr_meas.eq(0)
    for i in range(estmtr.register_size):
        print(f'addr {i}')
        yield estmtr.addr_data.eq(i)
        yield estmtr.data.eq(1)
        yield estmtr.en_wr_data.eq(0)
        yield
        yield estmtr.en_wr_data.eq(1)
        yield 
    yield    
    yield    
    yield    
    yield    
    yield    
    yield
    yield estmtr.inp_d.eq(1)
    yield estmtr.en_wr_meas.eq(1)
    yield
    yield estmtr.en_wr_meas.eq(0)
    yield
    yield
    yield
    yield
    yield
    yield
    yield
    yield
    yield
    yield

if __name__ == "__main__":
    convert = True
    
    dut = Estimator()
    path = Path(__file__).resolve().parent
    
    file_path = f'{path}/simple.v'
    if convert:
        verilog.convert(dut, dut.ios).write(file_path)
    else:
        tb = estimator_tb(dut)
        run_simulation(dut, tb, vcd_name=f"{path}/sum.vcd")

    print()