entity REGCE is
    port (
            d: in bit; 
            clk: in bit;
            q: out bit;
            en: in bit
         );
end FF_D;

-- https://www.fpga4student.com/p/vhdl-project.html

architecture behav of FF_D is
begin
    process (clk)
        begin
            if (clk’event and clk=’1’) then
                if (en = '1') then
                    q <= d;
                end if;
            end if;
    end process;
end behav;

entity REGCE4 is
    port( 
            d: in bit_vector(0 to 3);
            clk: in bit;
            q: out bit_vector(0 to 3);
            en: in bit
        );
end REG4;

architecture STRUCT of REGCE4 is
component REGCE
    port(
            d: in bit; 
            clk: in bit;
            q: out bit;
            en: in bit
        );
end component;

begin
u1: REGCE port map (d(0), clk, q(0), en);
u2: REGCE port map (d(1), clk, q(1), en);
u3: REGCE port map (d(2), clk, q(2), en);
u4: REGCE port map (d(3), clk, q(3), en);
end STRUCT;