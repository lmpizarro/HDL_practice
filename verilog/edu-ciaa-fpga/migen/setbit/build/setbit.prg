yosys -p "synth_ice40  -json /home/lmpizarro/devel/project/HDL/verilog/verilog/edu-ciaa-fpga/migen/setbit/build/setbit.json" /home/lmpizarro/devel/project/HDL/verilog/verilog/edu-ciaa-fpga/migen/setbit/build/setbit.v
nextpnr-ice40 --hx4k  --package tq144 --json /home/lmpizarro/devel/project/HDL/verilog/verilog/edu-ciaa-fpga/migen/setbit/build/setbit.json --pcf /home/lmpizarro/devel/project/HDL/verilog/verilog/edu-ciaa-fpga/migen/setbit/build/setbit.pcf --asc /home/lmpizarro/devel/project/HDL/verilog/verilog/edu-ciaa-fpga/migen/setbit/build/setbit.asc
icepack /home/lmpizarro/devel/project/HDL/verilog/verilog/edu-ciaa-fpga/migen/setbit/build/setbit.asc /home/lmpizarro/devel/project/HDL/verilog/verilog/edu-ciaa-fpga/migen/setbit/build/setbit.bin
iceprog /home/lmpizarro/devel/project/HDL/verilog/verilog/edu-ciaa-fpga/migen/setbit/build/setbit.bin
