
// SDIO Bond Core v0.1 — 异步脉冲电路 IP 核
// Target: Xilinx Versal ACAP (VCK190)
// Author: iNEST Research Team, Tianjin University
// Date: 2026-06-03

`timescale 1ns / 1ps

module sdio_bond_core #(
    parameter DATA_WIDTH = 8,
    parameter TAU_BASE    = 50,  // 基础延迟 (时钟周期)
    parameter TAU_ALPHA   = 2,   // 惊讶度灵敏度
    parameter THETA_LTP   = 25   // E-S -> E-L 固化阈值
) (
    // NCL 输入 (双轨编码)
    input  wire pre_data0,
    input  wire pre_data1,
    input  wire post_data0,
    input  wire post_data1,

    // 控制
    input  wire rst_n,       // 异步复位 (低有效)
    input  wire mode_sel,    // 0=化学键 1=电突触

    // 权重输出 (8-bit 定点)
    output reg [DATA_WIDTH-1:0] weight_out,

    // 键类型输出
    output reg [2:0] bond_type,  // 000=E-S, 010=E-L, 100=电突触

    // FEP 自由能输出
    output reg [DATA_WIDTH-1:0] fep_error,
    output reg [DATA_WIDTH-1:0] fep_penalty,

    // 完成检测
    output wire done
);

    // ===== Stage 1: NCL 输入缓冲 =====
    reg pre_data, post_data;
    reg pre_valid, post_valid;

    always @(*) begin
        pre_data  = pre_data0 ^ pre_data1 ? pre_data1 : 1'bz;
        post_data = post_data0 ^ post_data1 ? post_data1 : 1'bz;
        pre_valid  = pre_data0 ^ pre_data1;
        post_valid = post_data0 ^ post_data1;
    end

    // ===== Stage 2: STDP 状态机 =====
    reg [7:0] ltp_counter;
    reg [7:0] ltd_counter;
    reg [15:0] last_spike_timer;
    reg [DATA_WIDTH-1:0] weight;
    reg [DATA_WIDTH-1:0] tau_current;

    // STDP 更新逻辑
    always @(posedge pre_valid or posedge post_valid or negedge rst_n) begin
        if (!rst_n) begin
            weight <= 8'd128;      // 0.5 归一化
            ltp_counter <= 0;
            ltd_counter <= 0;
            bond_type <= 3'b000;    // E-S
        end else begin
            if (pre_data && post_data) begin
                // LTP: 赫布增强
                ltp_counter <= ltp_counter + 1;
                ltd_counter <= 0;
                weight <= (weight < 8'd255) ? weight + 2 : 8'd255;
            end else if (pre_data && !post_data) begin
                // LTD: 反赫布减弱
                ltd_counter <= ltd_counter + 1;
                ltp_counter <= 0;
                weight <= (weight > 8'd1) ? weight - 1 : 8'd1;
            end
        end
    end

    // ===== Stage 3: 键类型固化检测 =====
    always @(posedge pre_valid) begin
        if (ltp_counter >= THETA_LTP && bond_type == 3'b000)
            bond_type <= 3'b010;  // E-S -> E-L
    end

    // ===== Stage 4: 自适应 tau 延迟线 =====
    // 使用进位链实现可编程延迟
    (* DONT_TOUCH = "true" *) wire [TAU_BASE-1:0] carry_chain;
    genvar i;
    generate
        for (i = 0; i < TAU_BASE; i = i + 1) begin : delay_line
            if (i == 0)
                CARRY4 carry_inst (
                    .CO(carry_chain[i]),
                    .CI(1'b1),
                    .CYINIT(1'b0),
                    .DI(4'b0000),
                    .S(4'b1111)
                );
            else
                CARRY4 carry_inst (
                    .CO(carry_chain[i]),
                    .CI(carry_chain[i-1]),
                    .CYINIT(1'b0),
                    .DI(4'b0000),
                    .S(4'b1111)
                );
        end
    endgenerate

    // ===== Output =====
    assign weight_out = weight;
    assign done = pre_valid & post_valid;

endmodule
