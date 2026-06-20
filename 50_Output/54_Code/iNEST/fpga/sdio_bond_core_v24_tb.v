
\	imescale 1ns / 1ps
module sdio_bond_core_v24_tb;
    reg clk, rst_n, spike_in;
    wire spike_out;
    wire [15:0] fep_out;
    wire bond_active;
    
    sdio_bond_core_v24 #(
        .DATA_WIDTH(16),
        .FRAC_BITS(8)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .spike_in(spike_in),
        .spike_out(spike_out),
        .fep_out(fep_out),
        .bond_active(bond_active)
    );
    
    always #5 clk = ~clk;
    
    initial begin
        clk = 0; rst_n = 0; spike_in = 0;
        #20 rst_n = 1;
        #50 spike_in = 1; #10 spike_in = 0;
        #500 \;
    end
endmodule
