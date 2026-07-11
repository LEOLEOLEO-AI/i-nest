// ============================================================
// BF-Homeo Core (Rule3-v6) — BCM+FEP双层稳态控制
// iNEST Hardware Engineering | 2026-06-07
// ============================================================

module bcm_homeo_core #(
    parameter N_NODE      = 256,    // 节点数
    parameter ACT_WIDTH   = 8,      // 活动值位宽
    parameter THETA_WIDTH = 8,      // BCM阈值位宽
    parameter FEP_HIST    = 500,    // FEP历史深度
    parameter THETA_LO    = 56,     // θ_BCM下限（7.0×8=56，8bit归一化）
    parameter THETA_HI    = 64,     // θ_BCM上限（8.0×8=64）
    parameter EL_LO       = 38,     // EL下限（0.15×255≈38）
    parameter EL_HI       = 89      // EL上限（0.35×255≈89）
)(
    input  wire                         clk,
    input  wire                         rst_n,

    // 节点活动输入
    input  wire [N_NODE*ACT_WIDTH-1:0]  activity_in,

    // 自由能输入（来自外部计算）
    input  wire [N_NODE*ACT_WIDTH-1:0]  fep_local_in,

    // EL比例输入（来自拓扑统计模块）
    input  wire [7:0]                   el_ratio_in,  // 0-255对应0-1

    // 输出：BCM阈值（给Rule1）
    output reg  [N_NODE*THETA_WIDTH-1:0] theta_bcm_out,

    // 输出：FEP收敛标志（给Rule1的惊讶度调制）
    output reg  [N_NODE-1:0]            fep_converged,

    // 输出：EL控制信号
    output reg                          el_too_high,  // EL>上限 → 降固化速率
    output reg                          el_too_low    // EL<下限 → 升固化速率
);

// -------------------------------------------------------
// BCM滑动阈值更新
// θ_BCM_i(t) = θ_BCM_i(t-1) × 0.999 + h_i²(t) × 0.001
// -------------------------------------------------------
reg [THETA_WIDTH-1:0] theta_bcm [N_NODE-1:0];
reg [ACT_WIDTH-1:0]   activity  [N_NODE-1:0];
reg [ACT_WIDTH-1:0]   fep_local [N_NODE-1:0];

integer i;
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        for (i = 0; i < N_NODE; i = i + 1)
            theta_bcm[i] <= 8'd60;  // 初始值 = (7.0+8.0)/2 × 8
    end else begin
        for (i = 0; i < N_NODE; i = i + 1) begin
            activity[i]  <= activity_in[i*ACT_WIDTH +: ACT_WIDTH];
            fep_local[i] <= fep_local_in[i*ACT_WIDTH +: ACT_WIDTH];

            // EMA更新（τ_BCM=0.001 → 近似为 999/1000）
            // θ_new = θ_old - θ_old/1000 + h²/1000
            // 简化：8bit定点，每1000步更新一次
            // TODO：精确EMA乘法器
            if (activity[i] * activity[i] >> 8 > theta_bcm[i])
                theta_bcm[i] <= (theta_bcm[i] < THETA_HI) ? theta_bcm[i] + 1 : THETA_HI;
            else
                theta_bcm[i] <= (theta_bcm[i] > THETA_LO) ? theta_bcm[i] - 1 : THETA_LO;
        end
    end
end

// 输出θ_BCM
integer j;
always @(posedge clk) begin
    for (j = 0; j < N_NODE; j = j + 1)
        theta_bcm_out[j*THETA_WIDTH +: THETA_WIDTH] <= theta_bcm[j];
end

// -------------------------------------------------------
// FEP收敛检测（简化版：比较当前与500步前的变化率）
// TODO：实现完整500深度FIFO
// -------------------------------------------------------
reg [ACT_WIDTH-1:0] fep_prev [N_NODE-1:0]; // 简化：仅保存上一步
integer k;
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        for (k = 0; k < N_NODE; k = k + 1) begin
            fep_prev[k]     <= 8'd128;
            fep_converged[k] <= 0;
        end
    end else begin
        for (k = 0; k < N_NODE; k = k + 1) begin
            fep_prev[k] <= fep_local[k];
            // 变化率<5%视为收敛（8bit：5% × 255 ≈ 13）
            fep_converged[k] <= (fep_local[k] > fep_prev[k]) ?
                                (fep_local[k] - fep_prev[k] < 13) :
                                (fep_prev[k] - fep_local[k] < 13);
        end
    end
end

// -------------------------------------------------------
// EL区间控制
// -------------------------------------------------------
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        el_too_high <= 0;
        el_too_low  <= 0;
    end else begin
        el_too_high <= (el_ratio_in > EL_HI);
        el_too_low  <= (el_ratio_in < EL_LO);
    end
end

endmodule
// ============================================================
// END OF BF-Homeo Core v1.0
// TODO：实现完整500深度FEP历史FIFO
// ============================================================
