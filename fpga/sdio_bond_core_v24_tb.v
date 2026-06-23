// ============================================================
// sdio_bond_core_v24_tb.v — 功能仿真 Testbench
// ============================================================
// 验证 v24 FEP-STDP 融合 IP 核的:
//   1. NCL 双轨编码握手
//   2. LTP/LTD 衰减式计数器
//   3. FEP 盆地追踪
//   4. 周期固化逻辑
//   5. FEP 调制 STDP 速率
// ============================================================

`timescale 1ns / 1ps

module sdio_bond_core_v24_tb;

    // Parameters
    parameter DATA_WIDTH = 16;
    parameter CLK_PERIOD = 5;  // 200 MHz equivalent

    // DUT signals
    reg  pre_data0, pre_data1;
    reg  post_data0, post_data1;
    reg  fep_converged_src;
    reg  fep_converged_tgt;
    reg  consolidate_enable;
    reg  rst_n;
    reg  clk_equiv;

    wire [DATA_WIDTH-1:0] weight_out;
    wire [2:0] bond_type;
    wire consolidate_event;
    wire [DATA_WIDTH-1:0] fep_out;
    wire done;

    // Instantiate DUT
    sdio_bond_core_v24 #(
        .DATA_WIDTH(DATA_WIDTH),
        .FRAC_BITS(8),
        .THETA_LTP(15),
        .FEP_LTP_BOOST(16'h0166),     // 1.4
        .FEP_LTD_SUPPRESS(16'h009A),  // 0.6
        .CONSOLIDATE_PERIOD(25),
        .BASIN_WINDOW(20),
        .MIN_OUT_DEG(3)
    ) dut (
        .pre_data0(pre_data0),
        .pre_data1(pre_data1),
        .post_data0(post_data0),
        .post_data1(post_data1),
        .fep_converged_src(fep_converged_src),
        .fep_converged_tgt(fep_converged_tgt),
        .consolidate_enable(consolidate_enable),
        .rst_n(rst_n),
        .clk_equiv(clk_equiv),
        .weight_out(weight_out),
        .bond_type(bond_type),
        .consolidate_event(consolidate_event),
        .fep_out(fep_out),
        .done(done)
    );

    // Clock generation
    always #(CLK_PERIOD/2) clk_equiv = ~clk_equiv;

    // NCL helper: set DATA0 on pre rail
    task ncl_pre_data(input int value);
        begin
            if (value == 0) begin
                pre_data0 = 1; pre_data1 = 0;
            end else begin
                pre_data0 = 0; pre_data1 = 1;
            end
            #CLK_PERIOD;
            pre_data0 = 0; pre_data1 = 0;  // NULL phase
            #CLK_PERIOD;
        end
    endtask

    // NCL helper: set DATA0 on post rail
    task ncl_post_data(input int value);
        begin
            if (value == 0) begin
                post_data0 = 1; post_data1 = 0;
            end else begin
                post_data0 = 0; post_data1 = 1;
            end
            #CLK_PERIOD;
            post_data0 = 0; post_data1 = 0;  // NULL phase
            #CLK_PERIOD;
        end
    endtask

    // === Test Sequence ===
    initial begin
        $display("========================================");
        $display("sdio_bond_core_v24 Functional Testbench");
        $display("========================================");

        // Initialize
        clk_equiv = 0;
        pre_data0 = 0; pre_data1 = 0;
        post_data0 = 0; post_data1 = 0;
        fep_converged_src = 0;
        fep_converged_tgt = 0;
        consolidate_enable = 0;
        rst_n = 0;
        #(CLK_PERIOD * 3);
        rst_n = 1;
        #(CLK_PERIOD * 2);

        $display("\n--- Test 1: Reset state ---");
        $display("  weight_out = %h (expected 0x0080 = 0.5)", weight_out);
        $display("  bond_type = %b (expected 000 = E-S)", bond_type);
        assert(weight_out == 16'h0080) $display("  PASS: weight initialized"); 
        else $display("  FAIL: weight = %h", weight_out);
        assert(bond_type == 3'b000) $display("  PASS: bond_type = E-S");
        else $display("  FAIL: bond_type = %b", bond_type);

        // ===== Test 2: Pre-post co-activation (LTP) =====
        $display("\n--- Test 2: LTP (pre-post co-activation) ---");
        repeat(10) begin
            ncl_pre_data(1);
            ncl_post_data(1);
            @(posedge clk_equiv);
        end
        $display("  After 10x LTP:");
        $display("  weight_out = %h", weight_out);
        assert(weight_out > 16'h0080) $display("  PASS: weight increased");
        else $display("  FAIL: weight did not increase");

        // ===== Test 3: Pre-only activation (LTD) =====
        $display("\n--- Test 3: LTD (pre-only activation) ---");
        repeat(5) begin
            ncl_pre_data(1);
            ncl_post_data(0);  // post NOT active
            @(posedge clk_equiv);
        end
        $display("  After 5x LTD:");
        $display("  weight_out = %h", weight_out);

        // ===== Test 4: FEP modulation =====
        $display("\n--- Test 4: FEP modulation (converged src) ---");
        fep_converged_src = 1;   // Source neuron converged to FEP basin
        fep_converged_tgt = 0;

        repeat(10) begin
            ncl_pre_data(1);
            ncl_post_data(1);
            @(posedge clk_equiv);
        end
        $display("  After 10x LTP with FEP boost:");
        $display("  weight_out = %h (should be > non-FEP case)", weight_out);
        fep_converged_src = 0;  // Reset

        // ===== Test 5: E-S -> E-L consolidation =====
        $display("\n--- Test 5: Consolidation (E-S -> E-L) ---");
        // Force many LTP events to trigger consolidation
        repeat(20) begin
            ncl_pre_data(1);
            ncl_post_data(1);
            @(posedge clk_equiv);
        end
        $display("  bond_type = %b", bond_type);
        if (bond_type == 3'b010) $display("  PASS: Consolidated to E-L");
        else $display("  NOTE: Need more LTP events (bond_type = %b)", bond_type);

        // ===== Test 6: Periodic consolidation =====
        $display("\n--- Test 6: Periodic FEP consolidation ---");
        fep_converged_src = 1;
        consolidate_enable = 1;
        @(posedge clk_equiv);
        @(posedge clk_equiv);
        $display("  consolidate_event = %b", consolidate_event);
        consolidate_enable = 0;
        fep_converged_src = 0;

        // ===== Test 7: NCL completion detection =====
        $display("\n--- Test 7: NCL completion detection ---");
        ncl_pre_data(1);
        ncl_post_data(1);
        #1;
        $display("  done = %b (expected 1)", done);

        $display("\n========================================");
        $display("Testbench complete");
        $display("========================================");
        $finish;
    end

    // Waveform dump
    initial begin
        $dumpfile("sdio_bond_core_v24_tb.vcd");
        $dumpvars(0, sdio_bond_core_v24_tb);
    end

endmodule


// ============================================================
// bcm_threshold_v28.v — BCM Sliding Threshold Module
// ============================================================
// v28新增: BCM滑动阈值硬件化
//   theta_bcm += eta * h_avg^2 * (h_avg - theta_bcm)
//   惊讶度耦合: eta_eff = BCM_ETA * (1 + 0.8 * tanh(surprise))
// ============================================================

module bcm_threshold_v28 #(
    parameter DATA_WIDTH = 16,
    parameter FRAC_BITS  = 8,
    parameter BCM_ETA_Q  = 16'h0040,  // Q8.8: 0.25
    parameter BCM_MIN_Q  = 16'h0300,  // Q8.8: 3.0
    parameter BCM_MAX_Q  = 16'h1E00   // Q8.8: 30.0
) (
    input  wire clk,
    input  wire rst_n,
    input  wire [DATA_WIDTH-1:0] h_current,    // Current node activity
    input  wire [DATA_WIDTH-1:0] h_avg,        // Rolling average
    input  wire [DATA_WIDTH-1:0] surprise,      // FEP surprise (Q8.8)
    input  wire [DATA_WIDTH-1:0] fep_convergence, // Graded convergence [0,1]
    input  wire update_enable,                   // BCM update strobe

    output reg  [DATA_WIDTH-1:0] theta_bcm,     // BCM threshold
    output reg  [DATA_WIDTH-1:0] theta_eff       // Effective threshold (FEP modulated)
);

    // Internal registers
    reg [DATA_WIDTH-1:0] theta_bcm_reg;
    reg [DATA_WIDTH-1:0] h_avg_sq;    // h_avg^2
    reg [DATA_WIDTH-1:0] h_diff;      // h_avg - theta
    reg [DATA_WIDTH-1:0] delta;       // delta_theta
    reg [DATA_WIDTH-1:0] eta_effective;

    // Surprise coupling: eta_eff = BCM_ETA * (1 + 0.8 * tanh(surprise))
    // Hardware approximation: tanh(x) ~ x/(1+|x|) for Q8.8
    wire [DATA_WIDTH-1:0] tanh_approx;
    wire [DATA_WIDTH-1:0] surprise_coupling;

    // tanh approximation: x / (1 + |x|)
    assign tanh_approx = (surprise > {FRAC_BITS{1'b0}}) ?
        (surprise * 16'h0100) / ({FRAC_BITS{1'b0}, 1'b1} + surprise) :
        (surprise * 16'h0100) / ({FRAC_BITS{1'b0}, 1'b1} - surprise);

    // surprise_factor = 1.0 + 0.8 * tanh(surprise)
    assign surprise_coupling = 16'h0100 + ((tanh_approx * 16'h00CC) >> FRAC_BITS); // *0.8

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            theta_bcm_reg <= 16'h0800;  // initial = 8.0
            theta_bcm <= 16'h0800;
            theta_eff <= 16'h0800;
        end else if (update_enable) begin
            // Compute effective eta: BCM_ETA * surprise_factor * (1 - 0.5*convergence)
            eta_effective <= (BCM_ETA_Q * surprise_coupling) >> FRAC_BITS;
            // FEP convergence dampening
            eta_effective <= (eta_effective * (16'h0100 - {1'b0, fep_convergence[FRAC_BITS-1:1]})) >> FRAC_BITS;

            // h_avg^2
            h_avg_sq <= (h_avg * h_avg) >> FRAC_BITS;

            // h_diff = h_avg - theta_bcm_reg
            h_diff <= h_avg - theta_bcm_reg;

            // delta = eta_eff * h_avg^2 * (h_avg - theta)
            delta <= (eta_effective * ((h_avg_sq * h_diff) >> FRAC_BITS)) >> FRAC_BITS;

            // Update theta with clamping
            if (h_diff[15]) begin  // h_avg < theta (negative delta)
                theta_bcm_reg <= (theta_bcm_reg > (BCM_MIN_Q + delta)) ?
                    theta_bcm_reg + delta : BCM_MIN_Q;
            end else begin  // h_avg > theta (positive delta)
                theta_bcm_reg <= (theta_bcm_reg < (BCM_MAX_Q - delta)) ?
                    theta_bcm_reg + delta : BCM_MAX_Q;
            end

            // Effective theta (FEP modulated): theta * (1 - 0.5 * convergence)
            theta_eff <= (theta_bcm_reg * (16'h0100 - {1'b0, fep_convergence[FRAC_BITS-1:1]})) >> FRAC_BITS;

            theta_bcm <= theta_bcm_reg;
        end
    end

endmodule
