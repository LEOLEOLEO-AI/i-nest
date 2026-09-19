# 文献与主张证据台账

检索日期：2026-09-17。任务：V-LIT01、V-LIT02、V-NOV01。

状态区分：`META`=题录/标识符已核；`ABSTRACT`=摘要用途已核；`TEXT`=相关正文已核；`LIMITED`=本轮不足以核所需细节。即使 `TEXT`，也不表示论文的全部结论已被本团队独立证明或复现。

Crossref返回原始题录记录见 `10_Reference_Metadata.md`。空的更正字段不能证明没有更正；R08 的更正通过出版社页面另行查到。网络抓取若失败，使用其他来源或记为未核，不将失败当作文献不存在。

## 一、核心文献

| ID | 文献与定位 | 核查层级及支持范围 | 不支持什么 |
|---|---|---|---|
| R01 | Dambre et al., 2012, [DOI](https://doi.org/10.1038/srep00514)；Results、Theorem 4、Fading Memory | META+TEXT。容量受独立观测函数数量约束；完备性和衰退记忆相关的饱和条件 | 不支持“所有容量只在混沌边缘达到最大” |
| R02 | Engelken, Wolf, Abbott, 2023, [DOI](https://doi.org/10.1103/PhysRevResearch.5.043044)，[arXiv摘要](https://arxiv.org/abs/2006.02427) | META+ABSTRACT。特定随机循环网络全谱、广延混沌、部分区间解析近似及诊断用途 | 不支持六级智能、任意硬件通用全谱理论；本轮未逐式核其全部附录 |
| R03 | Manjunath, Jaeger, 2013, [DOI](https://doi.org/10.1162/NECO_a_00411)，[PubMed](https://pubmed.ncbi.nlm.nih.gov/23272918/) | META。输入相关ESP的直接相关来源；本报告错误等价的否证使用自含反例 | 未以题录替代该文全部定理条件核验 |
| R04 | Seifert, 2012, [DOI](https://doi.org/10.1088/0034-4885/75/12/126001)，[arXiv](https://arxiv.org/abs/1205.4176) | META+相关内容核查。随机热力学、熵产生、路径概率与反向过程框架 | 不支持一般Lyapunov谱和就是总热熵产生 |
| R05 | Still et al., 2012, [DOI](https://doi.org/10.1103/PhysRevLett.109.120604)，[全文](https://arxiv.org/html/1203.3271v3)；Problem setup、式(14)、Lower bound | META+TEXT。无反馈随机驱动；驱动步与松弛步；非预测信息与指定耗散的关系 | 不支持任意闭环智能系统的长时预测信息直接等于耗散 |
| R06 | Landauer, 1961, [DOI](https://doi.org/10.1147/rd.53.0183) | META；本报告只使用逻辑不可逆复位下界的标准限定性背景 | 不把每次任务、每个因果比特或每次浮点运算等同于理想擦除 |
| R07 | Pecora, Carroll, 1998, [DOI](https://doi.org/10.1103/PhysRevLett.80.2109) | META；经典耦合系统MSF的来源定位；本报告明确列出使用条件 | 未据其题录认证多层异质高阶网络的任意标量解耦 |
| R08 | Hochstetter et al., 2021, [正文](https://www.nature.com/articles/s41467-021-24260-z)；Results、Fig.6–8、Lyapunov analysis、Discussion | META+TEXT。相关谱和任务比较是仿真；简单正弦变换任务没有边缘优势 | 不支持原稿“硬件实测谱、普适最优”。[2024更正](https://www.nature.com/articles/s41467-024-54027-1)修正Methods公式及Fig.1b电路；本轮未独立重跑更正后的模型 |
| R09 | Tanaka et al., 2019, [DOI](https://doi.org/10.1016/j.neunet.2019.03.005) | META。物理储备池已有研究的综述定位 | 不表示本候选框架已跨基质验证 |
| R10 | Wright et al., 2022, [DOI](https://doi.org/10.1038/s41586-021-04223-6)，[PubMed](https://pubmed.ncbi.nlm.nih.gov/35082422/) | META+检索摘要。物理网络训练已有代表性路线 | 本轮不引用其性能数字，也不据此承诺SEI收益 |
| R11 | Scellier, Bengio, 2017, [全文](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2017.00024/full)；§3.2–3.3、Theorem 1 | META+TEXT。总能量、扰动强度与两相固定点梯度结构 | 不支持原稿未归一化、未收缩的混合二阶导数式 |
| R12 | Friston, 2010, [DOI](https://doi.org/10.1038/nrn2787) | META。FEP背景来源；本报告没有把其普遍性当作前提 | 不证明自由能优化强制指数趋零 |
| R13 | Shalizi, Crutchfield, 2001, [DOI](https://doi.org/10.1023/A:1010388907793) | META。计算力学与预测状态的既有工作定位 | 不能把预测态自动提升为干预因果态；更不能预设光滑有限维流形 |
| R14 | Hoel, Albantakis, Tononi, 2013, [DOI](https://doi.org/10.1073/pnas.1314922110) | META。因果涌现既有研究定位；本报告的数据处理限制另行给出 | 不将不同干预分布下的EI比较当作同一分布互信息凭空增加 |
| R15 | Hennequin, Vogels, Gerstner, 2012, [DOI](https://doi.org/10.1103/PhysRevE.86.011909) | META。非正规放大的既有工作定位；本报告矩阵例子自含 | 不代表非正规性越大能力越强 |
| R16 | Das, Green, 2025, [DOI](https://doi.org/10.1088/1751-8121/ad8f06)，[全文](https://arxiv.org/html/2501.04485v2) | META+TEXT。局部稳定矩阵的谱界、特定确定性恒温器条件 | 不支持原稿任意正指数和的幂律热熵上界 |
| R17 | Xie, Mihalas, Kuśmierz, 2025, [全文](https://arxiv.org/html/2505.09816v2)，[OpenReview](https://openreview.net/forum?id=J0SbYYY0po)；摘要、Results维数部分 | TEXT+会议记录。有限重尾网络增益转变与动力学维数权衡 | 未找到原稿训练过程中维数单调下降或指定幂律的对应证明 |
| R18 | Ding, Qiu, 2026, [摘要](https://arxiv.org/abs/2607.02157)，[所核全文](https://arxiv.org/html/2607.02157v1) | TEXT。确有该文，讨论量子储备池信息与热力学；按预印本处理 | 所核版本未找到独立词Lyapunov或OTOC对应的原稿全谱恒等式；不是说量子体系不存在相关动力学概念 |
| R19 | Ceni, Gallicchio, [全文版本](https://arxiv.org/html/2308.02902v2)；§3.1、式(7)–(11)、Theorem 3.5 | TEXT。特定ES2N构造、Jacobian及范数参数；设计与实验范围有限 | 不将特定网络稳定界提升为所有任务近临界最优 |
| R20 | Hoffmann et al., 2022, [全文](https://ar5iv.labs.arxiv.org/html/2203.15556)；§3.3式(2)与计算预算约束 | TEXT。加性损失分解、参数与数据共同预算 | 不支持原稿独立三变量乘积律与极端无限外推 |
| R21 | Senn et al., [eLife版本记录](https://elifesciences.org/articles/89674) | META/检索摘要。文献存在且研究特定神经最小作用量 | LIMITED：本轮未核全文构造；原稿所给作用量的错误由直接变分判断 |
| R22 | O'Byrne, Jerbi, 2022, [PubMed](https://pubmed.ncbi.nlm.nih.gov/36096888/) | META/检索摘要。临界性争论的综述定位 | LIMITED：本轮未逐段核综述，不使用其题录作为临界普适最优证据 |
| R23 | [Oseledets theorem，Scholarpedia](http://www.scholarpedia.org/article/Oseledets_theorem)；Theorem 4、连续时间部分 | TEXT。专家条目明确给出可逆cocycle的正反可积性、分解及连续时间条件 | 不宣称指数是动力系统完整不变量；不跳过随机/延迟系统适用性 |
| R24 | Hasselblatt, Pesin, 2008, [Pesin entropy formula](http://www.scholarpedia.org/article/Pesin_entropy_formula)；Margulis–Ruelle、Pesin公式、SRB测度 | TEXT。光滑性、测度、重数积分与等号条件 | 不支持任意驱动系统把内部正指数和直接当全部信息吞吐 |

## 二、可追溯的主张状态

| 主张 | 类型与来源 | 验证/验收 | 状态与限制 |
|---|---|---|---|
| 内部谱不足以判定一般任务能力 | [推导] 主报告§6.1同谱异读出 | V-TH01；保持内部过程不变且任务通道可不同 | 在允许不同端口的系统类中成立；不排除受限族相关性 |
| 最优时间尺度依赖任务 | [推导] 主报告§6.2标量模型 | V-TH02；解析极值与数值一致 | 在线性、指定输入和读出条件下成立 |
| 任务几何给最优线性风险 | [推导] 主报告§6.4；相关背景R01 | V-TH07；核空间、Schur补与风险展开正确 | 总体量；不是有限样本算法成功保证 |
| 约化路径误差限制策略价值误差 | [推导] 主报告§6.7 | V-TH08；同路径空间、共同可行策略类 | 假设很强，尚未证明真实器件满足 |
| 同谱同密度可以不同耗散 | [推导] 主报告§7.1；物理框架R04 | V-TH05；偶变量OU、概率流和熵产生一致 | 不否定特定模型的有条件谱界 |
| 任务响应指导SEI有优势 | [假设] 主报告§6.6、§8.3 | V-EXP01/03；未见操作预测与全成本增益 | 尚未运行主实验 |
| 时空协同可跨物理基质复现 | [假设] 主报告§10 | V-EXP04；独立基质、端口和预算一致 | 尚无本轮实验证据 |
| 候选框架具有新颖性 | [待测] 邻近工作定位 | V-NOV01；逐式差异、现有理论不可直接涵盖的新结果 | 命名和组合不算证明新颖性 |
| 世纪级成果或最大产业 | 愿景；无可支持的本轮证据 | 无法由本轮理论审查验收 | 不作为科学结论或产品承诺 |

## 三、检索与访问限制

检索词围绕 physical reservoir computing、Lyapunov spectra、input-dependent ESP、non-normal amplification、information processing capacity、thermodynamics of prediction、heavy-tailed recurrent networks。未将TCC误解为安全计算方向。

部分Firecrawl调用曾出现传输错误；某个不正确的arXiv版本路径返回404，随后改用论文实际列出的版本或摘要。Crossref题录均以实际响应登记；日期来自注册记录或页面，预印本与出版版本不混作同一审查深度。

这是聚焦核心争议的证据审计，不是系统综述。未完成全数据库查全、完整专利检索、所有原稿编号的反向匹配和全面撤稿排查。正式投稿前须补齐这些工作；其限制不影响本报告自含反例的数学效力。
