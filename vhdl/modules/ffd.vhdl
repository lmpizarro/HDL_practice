
entity REGCE is
    port (
            d: in bit; 
            clk: in bit;
            q: out bit;
            en: in bit
         );
end REGCE;

-- https://www.fpga4student.com/p/vhdl-project.html

architecture behave of REGCE is
begin
    process (clk)
        begin
            if (clk'event and clk='1') then
                if (en = '1') then
                    q <= d;
                end if;
            end if;
    end process;
end behave;


-- C2

entity REGCE4 is
    port( 
            d: in bit_vector(0 to 3);
            clk: in bit;
            q: out bit_vector(0 to 3);
            en: in bit
        );
end REGCE4;

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

-- REGCE16

entity REGCE16 is
    port( 
            d: in bit_vector(0 to 15);
            clk: in bit;
            q: out bit_vector(0 to 15);
            en: in bit
        );
end REGCE16;

architecture STRUCT of REGCE16 is
component REGCE4
    port(
            d: in bit_vector(0 to 3); 
            clk: in bit;
            q: out bit_vector(0 to 3);
            en: in bit
        );
end component;

begin
    u1: REGCE4 port map (d(0 to 3), clk, q(0 to 3), en);
    u2: REGCE4 port map (d(4 to 7), clk, q(4 to 7), en);
    u3: REGCE4 port map (d(8 to 11), clk, q(8 to 11), en);
    u4: REGCE4 port map (d(12 to 15), clk, q(12 to 15), en);
end STRUCT;

-- REGCE32

entity REGCE32 is
    port( 
            d: in bit_vector(0 to 31);
            clk: in bit;
            q: out bit_vector(0 to 31);
            en: in bit
        );
end REGCE32;

architecture STRUCT of REGCE32 is
component REGCE16
    port(
            d: in bit_vector(0 to 15); 
            clk: in bit;
            q: out bit_vector(0 to 15);
            en: in bit
        );
end component;

begin
    u1: REGCE16 port map (d(0 to 15), clk, q(0 to 15), en);
    u2: REGCE16 port map (d(16 to 31), clk, q(16 to 31), en);
end STRUCT;


-- DECODER_3_8

library ieee;
use ieee.std_logic_1164.all;
entity DECODER_3_8 is
    port( 
        dec_in: in std_logic_vector(0 to 2);
        dec_out: out std_logic_vector(0 to 7)
    );
end DECODER_3_8;

architecture rtl of DECODER_3_8 is
begin
    with dec_in select
    dec_out <= "00000001" when "000",
        "00000010" when "001",
        "00000100" when "010",
        "00001000" when "011",
        "00010000" when "100",
        "00100000" when "101",
        "01000000" when "110",
        "10000000" when "111",
        "--------" when others;
end rtl;

-- PRI_ENC

library ieee;
use ieee.std_logic_1164.all;
entity PRI_ENC is
    port(
            enc_in: in std_logic_vector(0 to 5);
            enc_out: out std_logic_vector(0 to 2)
    );
end PRI_ENC; 

architecture rtl of PRI_ENC is
begin
    with enc_in select
    enc_out <= "000" when "000000",
        "001" when "000001",
        "010" when "00001-",
        "011" when "0001--",
        "100" when "001---",
        "101" when "01----",
        "110" when "1-----",
        "---" when others;
end rtl;

-- MUX_4_1_8BIT

library ieee;
use ieee.std_logic_1164.all;
entity MUX_4_1_8BIT is
    port(
        s0, s1: in std_logic;
        a, b, c, d: in std_logic_vector(0 to 7);
        y: out std_logic_vector(0 to 7)
    );
end MUX_4_1_8BIT;

architecture rtl of MUX_4_1_8BIT is
    signal sel: std_logic_vector(0 to 1);
begin
    with sel select
        y <= a when "00",
        b when "01",
        c when "10",
        d when "11",
        "--------" when others;
end rtl;

-- MUX_4_1_NBIT

library ieee;
use ieee.std_logic_1164.all;
entity MUX_4_1_NBIT is
    generic( N: integer );
    port(
        s0, s1: in std_logic;
        a, b, c, d: in std_logic_vector(0 to N-1);
        y: out std_logic_vector(0 to N-1)
    );
end MUX_4_1_NBIT;

architecture rtl of MUX_4_1_NBIT is
    signal sel: std_logic_vector(0 to 1);
begin
    with sel select
        y <= a when "00",
        b when "01",
        c when "10",
        d when "11",
        "--------" when others;
end rtl;


-- DEMUX_1_4_NBIT


library ieee;
use ieee.std_logic_1164.all;
entity DEMUX_1_4_NBIT is
    generic( N: integer );
    port(
            sel: in std_logic_vector;
            x: in std_logic_vector(0 to N-1);
            y0, y1, y2, y3: out std_logic_vector(0 to N-1)
    );
end demux_1_4_Nbit;

architecture rtl of demux_1_4_Nbit is
begin
    y0 <= x when sel="00" else (others => '-');
    y1 <= x when sel="01" else (others => '-');
    y2 <= x when sel="10" else (others => '-');
    y3 <= x when sel="11" else (others => '-');
end rtl;
