
	yosys -p "synth_ice40  -json ram.json" ram.v  -l yosys.log -Q -T
	nextpnr-ice40 --hx4k  --package tq144  --json ram.json --pcf ram.pcf --asc ram.asc # --pcf-allow-unconstrained