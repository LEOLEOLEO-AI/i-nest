---
title: "基于 FPGA 的 伊辛机 (Ising Machine) 仿真与实验平台"
created: 2025-10-10
note_id: "1889905541834248752"
tags:
  - "get-笔记"
  - "技术实践"
---

# 基于 FPGA 的 伊辛机 (Ising Machine) 仿真与实验平台

## 摘要

---  ```markdown # FPGA Ising Machine Experiment Platform  本工程实现了一个基于 FPGA 的 **伊辛机 (Ising Machine)** 仿真与实验平台，支持 **Metropolis 更新规则** 和 **模拟退火过程**，并配套 *

## 正文

---

```markdown
# FPGA Ising Machine Experiment Platform

本工程实现了一个基于 FPGA 的 **伊辛机 (Ising Machine)** 仿真与实验平台，支持 **Metropolis 更新规则** 和 **模拟退火过程**，并配套 **Python 工具链** 实现自动化实验、批量分析和报告生成。

---

## 📂 工程目录结构
```

![image.png](https://get-notes.umiwi.com/get_notes_prod%2F202510102329%2Fgetnotes_img_1a3a499d40085214o8j1MKfN.png?Expires=1780065610&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=1qeeH4KVAoRwcMSivWVv67uVGzA%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)

````auto

---

# 📜 源代码汇总

## 🔹 Verilog 部分

### 顶层系统（`verilog/ising_fpga_system.v`）
```verilog
module ising_fpga_system #(
    parameter N = 8,
    parameter WIDTH = 16
)(
    input                   clk,
    input                   rst_n,
    input  [7:0]            adc0_data,
    input  [7:0]            adc1_data,
    output [7:0]            dac_data,
    output                  pulse_out
);

    reg  signed [WIDTH-1:0] spin_state [0:N-1];
    reg  signed [WIDTH-1:0] J_matrix   [0:N-1][0:N-1];
    wire signed [2*WIDTH-1:0] energy;
    wire signed [WIDTH-1:0]   new_state [0:N-1];

    // Metropolis 更新模块
    ising_metropolis #(.N(N), .WIDTH(WIDTH)) u_metropolis (
        .clk(clk),
        .rst_n(rst_n),
        .spin_state(spin_state),
        .J_matrix(J_matrix),
        .new_state(new_state)
    );

    // 输出能量低 8 位到 DAC
    assign dac_data = energy[7:0];

    // 状态更新
    integer i;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i=0; i<N; i=i+1)
                spin_state[i] <= (i%2==0)? 1 : -1;
        end else begin
            for (i=0; i<N; i=i+1)
                spin_state[i] <= new_state[i];
        end
    end

    // 简单能量计算
    integer j;
    reg signed [2*WIDTH-1:0] sum;
    always @(*) begin
        sum = 0;
        for (i=0; i<N; i=i+1)
            for (j=0; j<N; j=j+1)
                sum = sum + J_matrix[i][j]*spin_state[i]*spin_state[j];
    end
    assign energy = -sum;

    // 脉冲发生器
    reg [7:0] cnt;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) cnt <= 0;
        else cnt <= cnt + 1;
    end
    assign pulse_out = cnt[7];

endmodule
````

### Metropolis 更新模块（`verilog/ising_metropolis.v`）

```verilog
module ising_metropolis #(
    parameter N = 8,
    parameter WIDTH = 16,
    parameter TEMP = 4
)(
    input clk,
    input rst_n,
    input  signed [WIDTH-1:0] spin_state [0:N-1],
    input  signed [WIDTH-1:0] J_matrix   [0:N-1][0:N-1],
    output reg signed [WIDTH-1:0] new_state [0:N-1]
);

    integer i,j;
    reg signed [2*WIDTH-1:0] sum;
    reg signed [2*WIDTH-1:0] deltaE;

    // LFSR 随机数
    reg [15:0] lfsr;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) lfsr <= 16'hACE1;
        else lfsr <= {lfsr[14:0], lfsr[15]^lfsr[13]^lfsr[12]^lfsr[10]};
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i=0; i<N; i=i+1) new_state[i] <= 1;
        end else begin
            for (i=0; i<N; i=i+1) begin
                sum = 0;
                for (j=0; j<N; j=j+1)
                    sum = sum + J_matrix[i][j]*spin_state[j];
                deltaE = 2*spin_state[i]*sum;
                if (deltaE <= 0) new_state[i] <= -spin_state[i];
                else if (lfsr[7:0] < TEMP*16) new_state[i] <= -spin_state[i];
                else new_state[i] <= spin_state[i];
            end
        end
    end
endmodule
```

### Testbench（`verilog/tb_ising_fpga_annealing.v`）

```verilog
`timescale 1ns/1ps
module tb_ising_fpga_annealing;

    parameter N=4; parameter WIDTH=16;
    reg clk, rst_n;
    reg [7:0] adc0_data, adc1_data;
    wire [7:0] dac_data; wire pulse_out;
    reg [7:0] temp_reg;

    ising_fpga_system #(.N(N),.WIDTH(WIDTH)) dut (
        .clk(clk), .rst_n(rst_n),
        .adc0_data(adc0_data), .adc1_data(adc1_data),
        .dac_data(dac_data), .pulse_out(pulse_out)
    );

    initial begin clk=0; forever #5 clk=~clk; end

    integer csv_file;
    initial begin
        rst_n=0; adc0_data=0; adc1_data=0; #50; rst_n=1;
        csv_file=$fopen("ising_annealing_log.csv","w");
        $fwrite(csv_file,"time_ns,energy,dac_data,pulse_out\n");
        repeat(500) begin
            adc0_data=$random%256; adc1_data=$random%256; #10;
            $fwrite(csv_file,"%0t,%0d,%0d,%0b\n",$time,dut.energy,dac_data,pulse_out);
        end
        $fclose(csv_file); $stop;
    end
endmodule
```

---

## 🔹 Python 部分

### 矩阵生成器（`python/generate_ising_matrix.py`）

```python
import numpy as np, os

def generate_matrix(N=8, mode="full", sparsity=0.5, seed=None):
    if seed is not None:
        np.random.seed(seed)
    J = np.zeros((N, N), dtype=int)
    if mode == "full":
        J = np.random.choice([-1, 1], size=(N, N))
    elif mode == "sparse":
        mask = np.random.rand(N, N) < sparsity
        J = np.random.choice([-1, 1], size=(N, N)) * mask
    elif mode == "random":
        J = np.random.choice([-1, 1], size=(N, N))
    np.fill_diagonal(J, 0)
    J = (J + J.T) // 2
    return J

def export_to_verilog(J, filename="ising_matrix.vh"):
    N = J.shape[0]
    with open(filename, "w") as f:
        f.write("// 自动生成的伊辛矩阵初始化文件\n")
        f.write(f"parameter N = {N};\n")
        f.write("reg signed [15:0] J_matrix [0:N-1][0:N-1];\n\n")
        f.write("initial begin\n")
        for i in range(N):
            for j in range(N):
                f.write(f"    J_matrix[{i}][{j}] = {J[i,j]};\n")
        f.write("end\n")

if __name__ == "__main__":
    os.makedirs("matrices", exist_ok=True)
    J_full = generate_matrix(N=8, mode="full", seed=42)
    export_to_verilog(J_full, "matrices/J_full.vh")
    J_sparse = generate_matrix(N=8, mode="sparse", sparsity=0.3, seed=123)
    export_to_verilog(J_sparse, "matrices/J_sparse.vh")
    J_random = generate_matrix(N=8, mode="random", seed=99)
    export_to_verilog(J_random, "matrices/J_random.vh")
    print("✅ 矩阵文件已生成在 matrices/ 文件夹下")
```

---

### 单次分析（`python/analyze_ising_annealing.py`）

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("ising_annealing_log.csv")

cutoff = int(len(df) * 0.8)
final_energy = df["energy"].iloc[cutoff:]
avg_final_energy = final_energy.mean()

threshold = 0.05 * abs(avg_final_energy)
stable_idx = np.where(abs(df["energy"] - avg_final_energy) < threshold)[0]
convergence_time = df["time_ns"].iloc[stable_idx[0]] if len(stable_idx) > 0 else None

print("=== 分析结果 ===")
print(f"最终平均能量: {avg_final_energy:.2f}")
if convergence_time:
    print(f"收敛时间点: {convergence_time} ns")
else:
    print("未检测到明显收敛")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,8), sharex=True,
                               gridspec_kw={'height_ratios': [3, 1]})

ax1.plot(df["time_ns"], df["energy"], color="blue", label="Energy")
ax1.axhline(avg_final_energy, color="blue", linestyle="--", alpha=0.6, label="Avg Final Energy")
if convergence_time:
    ax1.axvline(convergence_time, color="orange", linestyle="--", label=f"Convergence @ {convergence_time} ns")
ax1.set_ylabel("Energy")
ax1.legend()

ax2.step(df["time_ns"], df["pulse_out"], where="post", color="purple", label="Pulse Out")
ax2.set_ylabel("Pulse")
ax2.set_xlabel("Simulation Time (ns)")
ax2.set_ylim(-0.2, 1.2)
ax2.legend()

plt.tight_layout()
plt.show()
```

---

### 批量实验（`python/batch_analyze_ising.py`）

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

files = glob.glob("results/ising_annealing_*.csv")
summary = []

plt.figure(figsize=(12,6))

for f in files:
    df = pd.read_csv(f)
    label = f.split("/")[-1].replace(".csv","")
    cutoff = int(len(df) * 0.8)
    final_energy = df["energy"].iloc[cutoff:]
    avg_final_energy = final_energy.mean()
    threshold = 0.05 * abs(avg_final_energy)
    stable_idx = np.where(abs(df["energy"] - avg_final_energy) < threshold)[0]
    convergence_time = df["time_ns"].iloc[stable_idx[0]] if len(stable_idx) > 0 else None
    summary.append({"Experiment": label, "Avg Final Energy": avg_final_energy, "Convergence Time (ns)": convergence_time})
    plt.plot(df["time_ns"], df["energy"], label=f"{label} (E={avg_final_energy:.1f})")

plt.title("Batch Comparison of Ising Machine Annealing Experiments")
plt.xlabel("Simulation Time (ns)")
plt.ylabel("Energy")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

summary_df = pd.DataFrame(summary)
print("\n=== 实验结果汇总 ===")
print(summary_df.to_string(index=False))
```

---

### 一键实验平台（`python/ising_experiment_platform.py`）

```python
import os, numpy as np, pandas as pd, matplotlib.pyplot as plt
from datetime import datetime

from generate_ising_matrix import generate_matrix, export_to_verilog

def run_experiments(temps, matrices, N=8):
    os.makedirs("results", exist_ok=True)
    os.makedirs("matrices", exist_ok=True)
    results = []
    for T in temps:
        for mode in matrices:
            exp_name = f"ising_annealing_temp{T}_{mode}"
            vh_file = f"matrices/{exp_name}.vh"
            J = generate_matrix(N=N, mode=mode, seed=T)
            export_to_verilog(J, vh_file)
            # 这里应调用仿真工具生成 CSV 文件
            csv_file = f"results/{exp_name}.csv"
            if os.path.exists(csv_file):
                df = pd.read_csv(csv_file)
                cutoff = int(len(df) * 0.8)
                avg_final_energy = df["energy"].iloc[cutoff:].mean()
                threshold = 0.05 * abs(avg_final_energy)
                stable_idx = np.where(abs(df["energy"] - avg_final_energy) < threshold)[0]
                convergence_time = df["time_ns"].iloc[stable_idx[0]] if len(stable_idx) > 0 else None
                results.append({"Experiment": exp_name, "Avg Final Energy": avg_final_energy, "Convergence Time (ns)": convergence_time})
    return pd.DataFrame(results)

def plot_energy_curves(summary_df):
    plt.figure(figsize=(12,6))
    for exp in summary_df["Experiment"]:
        csv_file = f"results/{exp}.csv"
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            plt.plot(df["time_ns"], df["energy"], label=f"{exp}")
    plt.title("Batch Comparison of Ising Machine Annealing Experiments")
    plt.xlabel("Simulation Time (ns)")
    plt.ylabel("Energy")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("reports/energy_curves.png")

def generate_report(summary_df, report_file="reports/ising_report.md"):
    os.makedirs("reports", exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# 伊辛机 FPGA 实验报告\n\n")
        f.write(f"生成时间: {datetime.now()}\n\n")
        f.write("## 实验结果汇总\n\n")
        f.write(summary_df.to_markdown(index=False))
        f.write("\n\n## 能量收敛曲线对比\n\n")
        f.write("![Energy Curves](energy_curves.png)\n")

if __name__ == "__main__":
    temps = [50, 100, 150]
    matrices = ["full", "sparse", "random"]
    summary_df = run_experiments(temps, matrices, N=8)
    if not summary_df.empty:
        print(summary_df)
        plot_energy_curves(summary_df)
        generate_report(summary_df)
        print("✅ 实验报告已生成 reports/ising_report.md")
```

---

---
*来源：Get笔记 | 类型：plain_text | 入库：2026-04-29 10:40*

## Related Notes

- [[2028全球智能危机：人工智能引发的经济与制度冲击全景分析]]
- [[AgentEvolver vs AlphaEvolve：AI自我进化的两条核心路线对比 🧠]]
- [[AI双引擎的未来之光]]
