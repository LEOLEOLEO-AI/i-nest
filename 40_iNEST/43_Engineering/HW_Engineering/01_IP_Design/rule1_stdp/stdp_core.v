// ============================================================
// SA-STDP Core (Rule1-v6) — 惊讶度调制STDP
// iNEST Hardware Engineering | 2026-06-07
// 规范：SDI_Rules_v6_Hardware_Spec.md
// ============================================================
// 参数基础：
//   Bi & Poo 1998：τ_STDP=20ms
//   Song 2000：η_LTP=0.005, η_LTD=0.004
//   Friston 2005：惊讶度调制 α=0.4, β=0.3, γ=0.5
// ============================================================

module stdp_core #(
    parameter N_SYN       = 256,    // 突触数
    parameter W_WIDTH     = 8,      // 权重位宽（定点8bit）
    parameter SURP_WIDTH  = 8,      // 惊讶度位宽
    parameter TAU_STDP    = 20,     // STDP时间窗口（ms，离散化）
    parameter ETA_LTP     = 5,      // 基础LTP速率（×0.001）
    parameter ETA_LTD     = 4,      // 基础LTD速率（×0.001）
    parameter THETA_BASE  = 15      // 基础LTP阈值
)(
    input  wire                     clk,
    input  wire                     rst_n,

    // 脉冲输入
    input  wire [N_SYN-1:0]         pre_spike,       // 突触前脉冲
    input  wire [N_SYN-1:0]         post_spike,      // 突触后脉冲

    // 惊讶度输入（来自Rule3 FEP收敛检测）
    input  wire [N_SYN*SURP_WIDTH-1:0] surprise_in, // 每突触惊讶度

    // 权重读写接口
    input  wire [$clog2(N_SYN)-1:0] w_addr,
    output reg  [W_WIDTH-1:0]        w_out,          // 权重读出
    output reg  [N_SYN-1:0]          w_update_en,    // 权重更新使能

    // 更新量输出
    output reg  signed [W_WIDTH:0]   delta_w [N_SYN-1:0], // 权重变化量

    // 状态输出
    output reg  [N_SYN-1:0]          ltp_event,      // LTP事件标志
    output reg  [N_SYN-1:0]          ltd_event       // LTD事件标志
);

// -------------------------------------------------------
// 内部寄存器
// -------------------------------------------------------
reg [W_WIDTH-1:0]   weights    [N_SYN-1:0];  // 突触权重
reg [4:0]           pre_trace  [N_SYN-1:0];  // 突触前脉冲trace（5bit计数器）
reg [4:0]           post_trace [N_SYN-1:0];  // 突触后脉冲trace
reg [SURP_WIDTH-1:0] surprise  [N_SYN-1:0];  // 惊讶度寄存器

// 调制后的学习速率（10bit定点）
reg [9:0] eta_ltp_eff [N_SYN-1:0];
reg [9:0] eta_ltd_eff [N_SYN-1:0];

// -------------------------------------------------------
// 惊讶度解包
// -------------------------------------------------------
integer k;
always @(posedge clk) begin
    for (k = 0; k < N_SYN; k = k + 1) begin
        surprise[k] <= surprise_in[k*SURP_WIDTH +: SURP_WIDTH];
    end
end

// -------------------------------------------------------
// Rule1-v6 核心：惊讶度调制学习速率
// η_LTP_eff = η_LTP_base × (1 + α_FEP × surprise_i / 255)
// η_LTD_eff = η_LTD_base × (1 - β_FEP × surprise_i / 255)
// α_FEP = 0.4 ≈ 4/10, β_FEP = 0.3 ≈ 3/10
// -------------------------------------------------------
integer i;
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        for (i = 0; i < N_SYN; i = i + 1) begin
            eta_ltp_eff[i] <= ETA_LTP;
            eta_ltd_eff[i] <= ETA_LTD;
        end
    end else begin
        for (i = 0; i < N_SYN; i = i + 1) begin
            // LTP速率：× (1 + 0.4 × surprise/255)
            eta_ltp_eff[i] <= ETA_LTP + (ETA_LTP * 4 * surprise[i]) / (10 * 255);
            // LTD速率：× (1 - 0.3 × surprise/255)，最小为0
            eta_ltd_eff[i] <= (ETA_LTD * 255 > ETA_LTD * 3 * surprise[i] / 10) ?
                               ETA_LTD - (ETA_LTD * 3 * surprise[i]) / (10 * 255) : 0;
        end
    end
end

// -------------------------------------------------------
// Trace 衰减（模拟STDP时间窗口）
// 每周期trace × (1 - 1/TAU_STDP)
// -------------------------------------------------------
integer j;
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        for (j = 0; j < N_SYN; j = j + 1) begin
            pre_trace[j]  <= 0;
            post_trace[j] <= 0;
        end
    end else begin
        for (j = 0; j < N_SYN; j = j + 1) begin
            // 脉冲到达时trace置1，否则衰减
            pre_trace[j]  <= pre_spike[j]  ? 5'd31 : (pre_trace[j]  > 0 ? pre_trace[j]  - 1 : 0);
            post_trace[j] <= post_spike[j] ? 5'd31 : (post_trace[j] > 0 ? post_trace[j] - 1 : 0);
        end
    end
end

// -------------------------------------------------------
// STDP权重更新
// LTP：post_spike && pre_trace>0  → Δw = +η_ltp_eff × pre_trace
// LTD：pre_spike  && post_trace>0 → Δw = -η_ltd_eff × post_trace
// -------------------------------------------------------
integer m;
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        for (m = 0; m < N_SYN; m = m + 1) begin
            weights[m]    <= 8'd128;  // 初始化中间值
            delta_w[m]    <= 0;
            w_update_en[m] <= 0;
            ltp_event[m]  <= 0;
            ltd_event[m]  <= 0;
        end
    end else begin
        for (m = 0; m < N_SYN; m = m + 1) begin
            ltp_event[m] <= 0;
            ltd_event[m] <= 0;
            w_update_en[m] <= 0;

            if (post_spike[m] && pre_trace[m] > 0) begin
                // LTP：Δw = +η_ltp_eff × pre_trace / 31
                delta_w[m]    <= $signed({1'b0, (eta_ltp_eff[m] * pre_trace[m]) >> 5});
                w_update_en[m] <= 1;
                ltp_event[m]  <= 1;
                // 权重更新（饱和到[0,255]）
                weights[m] <= (weights[m] + ((eta_ltp_eff[m] * pre_trace[m]) >> 5) > 255) ?
                               8'd255 : weights[m] + ((eta_ltp_eff[m] * pre_trace[m]) >> 5);

            end else if (pre_spike[m] && post_trace[m] > 0) begin
                // LTD：Δw = -η_ltd_eff × post_trace / 31
                delta_w[m]    <= -$signed({1'b0, (eta_ltd_eff[m] * post_trace[m]) >> 5});
                w_update_en[m] <= 1;
                ltd_event[m]  <= 1;
                // 权重更新（下限为0）
                weights[m] <= (weights[m] < (eta_ltd_eff[m] * post_trace[m]) >> 5) ?
                               8'd0 : weights[m] - ((eta_ltd_eff[m] * post_trace[m]) >> 5);
            end
        end
    end
end

// -------------------------------------------------------
// 权重读接口
// -------------------------------------------------------
always @(posedge clk) begin
    w_out <= weights[w_addr];
end

endmodule
// ============================================================
// END OF SA-STDP Core v1.0
// TODO：
//   1. 添加testbench（见 02_Verification/tb/stdp_core_tb.v）
//   2. FPGA综合脚本（见 04_FPGA_Proto/）
//   3. 与BF-Homeo-IP的surprise接口对齐
// ============================================================
