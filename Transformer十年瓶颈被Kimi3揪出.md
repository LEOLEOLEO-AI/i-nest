2015年，何恺明画了一条线。  
一条简单到令人发指的线，**把输入原封不动地加回输出**  
这条线叫残差连接，它救活了深度神经网络，也从此被写进每一个Transformer的骨骼里，**十年没人敢动**

直到月之暗面的Kimi团队说：这条线，**本身就是一个设计缺陷**

![Kimi官方发布Attention Residuals（分段1）](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreiavMTRd1IwgDxYBB8VAGfxjOWMsZUeGIcucyibXznRK5uU7nicmjVhIHY27ZkEx2g4sgAQjGxeqC4hickReu5nib90zrDhz6EuuBHJ8/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)![Kimi官方发布Attention Residuals（分段2）](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreias3MJZ0UCL2icuUPAEXegoKaaK0PqUypZVlj5Rq5JiaPRqWoj5uve5tDCEmrPzffWlOAFRVSIehY4jMfMlUw7KStC7o45XUibfDJU/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

▲ 2026年3月16日，Kimi团队在arXiv发布技术报告《Attention Residuals》，正式向残差连接"开刀"

## 十年"高速公路"，跑出了一个致命Bug

先用30秒搞懂残差连接在干什么。

想象一栋**80层的大楼**，每一层的工人加工一批货物，然后把成品和原材料**一起打包**往上送  
这就是标准Transformer的工作方式，每一层的输出，_以固定权重1_，加回到输入上，再交给下一层

好处显而易见：梯度有了一条"高速公路"，信号不会在层层传递中消失  
从ResNet到GPT，这条路跑了十年，**所有人都觉得它没问题**

但Kimi团队指出了一个被集体忽视的后果：**PreNorm稀释**

把80层的递推公式展开来看，第80层拿到的隐状态，其实是_前面所有层输出的等权求和_，每一层的贡献系数都是1  
结果是，**每一层不管多重要、多不重要，都被无差别地搅进同一锅汤里**

随着层数加深，这锅汤越来越稠。  
新加入的一勺高汤，味道瞬间被稀释到几乎尝不出来  
于是深层的网络为了"被听见"，不得不**拼命放大自己的输出幅度**，训练因此变得越来越不稳定

这个bug，_藏在每一个大模型的每一层里_，从2015年到2026年

## "把注意力旋转90度"：一个极其优雅的类比

Kimi团队的破题思路，可以这样概括：

> **RNN在时间维上压缩信息，Transformer用注意力解决了它。残差在深度维上压缩信息，为什么不用同样的方法？**

![Avi Chawla的详细解读（分段1）](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreiav2PDTU8FOdVSibZm6oF69iczFNxjHRjfRgwwMy7HlkgtzOWH22YiaaX7cJ2MIeibOP6zJqkG9708F9c2Dq27pbgesL1UspOpRLoaU/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)![Avi Chawla的详细解读（分段2）](https://mmbiz.qpic.cn/sz_mmbiz_jpg/wkbW3msreiasibnSEMJMx4SvmKnxoyIj82G1wuXdMDaPWNI9NhdlgyxrNZ6rsTQtUz3fbibW0HjX2ULPIhvqrxdkXGr9rp9q7WKSicPqk3TDTicg/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)![Avi Chawla的详细解读（分段3）](https://mmbiz.qpic.cn/sz_mmbiz_jpg/wkbW3msreiasRQGA48ZSy5kdQ5LbKhXKibOuWqpwMicHc4vE93jqTvmIfzOYvEF2RZlPxCXUlqXH5Wicjibb9LHTrgwlorZLcrBfFRNvHT5N6InE/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)![Avi Chawla的详细解读（分段4）](https://mmbiz.qpic.cn/sz_mmbiz_jpg/wkbW3msreiavGZpTwvQuCqYoJvJdSABGqic0z5YWhOqIf4mUkeibOJpazM1ic84NiaaNDPCtJQGQ6FcpnU7CB5EJOhPMeNnrs6jQV66nn8zFmLAY/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)

▲ 数据科学博主Avi Chawla在三月撰写的长文解读，系统拆解了从PreNorm稀释到Block AttnRes的完整逻辑

这就是**Attention Residuals（AttnRes）**的核心思想  
不再把每一层的输出以权重1机械相加，而是让每一层_用softmax注意力_，**回头看所有前序层的输出，自己决定该从哪里拿多少**

杨植麟在GTC上给出了一个更直觉的描述：这就像**把LSTM"旋转90度"**，LSTM在序列时间步上决定记住什么、忘掉什么；  
AttnRes在网络深度上做完全相同的事

每一层拥有一个**学习到的伪查询向量**，它对此前所有层的输出（键和值）做注意力计算  
权重是_内容相关的_，不同的token、不同的上下文，可以从不同的层拿回不同的表示  
**该记的记，该忘的忘，不再被迫吃下所有历史的等权平均**

## 从论文到工程：Block AttnRes才是工程上的杀手锏

理论很美，**但直接用，系统会爆**。

Full AttnRes要求每一层都保存并访问此前_所有层_的输出，在流水线并行和激活重计算的大规模训练中，内存和通信开销是 $O(Ld)$ 量级，对于动辄近百层的模型，这根本不实际

Kimi的工程答案是**Block AttnRes**：把所有层分成约8个块，**块内仍用标准残差**快速累加，**块间用注意力**选择性聚合  
内存直降到 $O(Nd)$，推理延迟开销**不到2%**

![缩放律实验（分段1）](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreiau67X2ianZjlI5eIibUWYdm8V8qjia5vg5S4NdYyHQEIBibmdYnVTQuu9HrpkkpA27Tsq0Z2q4HG0yGfo1wxp7oMqzkQib0gMSkZ3fU/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=6)![缩放律实验（分段2）](https://mmbiz.qpic.cn/sz_mmbiz_jpg/wkbW3msreiatfTeFD5EyiatWwW46yswaWbkxjwQSjmEfWAnfWeEyfxcQfU7ZwD4MQKuG7BxBT94ICQ3JF03NF0jfZuHrbAD3HdMajpwpk9mB4/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=7)

▲ 官方缩放律曲线：Block AttnRes在不同模型规模上稳定呈现约1.25倍算力优势

在48B参数的Kimi Linear模型（激活3B）上训练1.4万亿token后，数字说话：

- **GPQA-Diamond：36.9% → 44.4%**
    
    （+7.5个点）
    
- **Math：53.5% → 57.1%**
    
    （+3.6个点）
    
- **HumanEval：59.1% → 62.2%**
    
    （+3.1个点）
    
- 全部15个评测基准**一致提升**，无一例外
    

而代价？  
几乎可以忽略的参数开销和不到2%的推理延迟  
**同样的模型、同样的数据，换一种残差架构，相当于白捡25%的训练效率**

连马斯克都忍不住回了一句：_"Impressive work from Kimi."_

![马斯克评价](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreiaux8wF1gb9Fo8VlK9e6JDGgicLm106mXicTsHzE7RJTutuj5HAogQDKvryPibcf8wxpyT6ibt0j1qwNlkF1r9bYgYZPTianwOyNia3l8/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=8)

▲ Elon Musk对Kimi Attention Residuals的公开评价

## 四个月后，它被装进了2.8万亿参数的怪兽

2026年7月16日，**Kimi K3发布**

![K3发布主帖（分段1）](https://mmbiz.qpic.cn/sz_mmbiz_jpg/wkbW3msreiatmdARvFxF7ZIkkcfgrP6x4CyDKTru4S6wiaJK6aFOxXlobb0kw8WE0YQftxp70OJDCiaDc6XkKA4pbTkXibicdJtevQ2iawKG4X75U/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=9)![K3发布主帖（分段2）](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreiatTj1aw4licf3rjLO37F56YTAgWt7fRMH3ow2hyq1vHMRlydP41W6g0VcFD5U6xodSibxNV8vHwUicAY5hUxwd8byFAYkrzg8dj0w/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=10)

▲ Kimi K3官宣：2.8万亿参数、百万token上下文、原生多模态，AttnRes正式进入产品级部署

这是一个**约2.8万亿参数、百万token上下文、原生多模态**的旗舰模型  
而它的架构骨干，被官方明确写成两根柱子：**Kimi Delta Attention（KDA）** 负责序列长度方向的效率（百万token解码最高6.3倍加速），**Attention Residuals** 负责模型深度方向的信息路由

再叠上Stable LatentMoE（896个专家中仅激活16个）以及精调的训练数据配方，官方宣称相对上一代K2，整体缩放效率提升约**2.5倍**

![K3架构说明（分段1）](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreiat4ZUlQ3r2dMNBZX9sEMxEn8570sF4syZt0x1JEqWBAJnDOgcfeb6bY1p80d6twJLO9p5yrANTR3wAw7AhIjC2CS5nkCbBIxicQ/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=11)![K3架构说明（分段2）](https://mmbiz.qpic.cn/sz_mmbiz_jpg/wkbW3msreiatIOk37SXKibnvveEr4T2ZSBPUmyUJVp5cpKpPJz4N8jnQwIw3Bl5FvGAHzTQP0ia317zCWqh8ZXtyGYnS2ZNqJFzFc7iab1PxZUE/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=12)

▲ K3线程中的架构描述：KDA + AttnRes + 极端稀疏MoE，三位一体

**一个三月份还只存在于论文和48B实验中的残差改写，四个月后就被部署进了接近3万亿参数的产品模型**  
从研究原型到生产系统的速度，已经快到让社区反应不过来

K3甚至展示了一个"自进化"案例：在96层、8192维的生产配置上，系统自动迭代优化AttnRes的Triton Kernel，把前向+反向时间从283.6毫秒压到114.4毫秒  
**AttnRes已经从论文公式走进生产基础设施，专用算子优化也随之成为工程环节**

## 争议来了："十年未动"这话，严格吗？

流量起来了，纠正也跟着来了。

![反对意见](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreiasBkv8jMj8nNicXBm7fo3dBoiaLPVQSiaMY4icibiaibzLzBtib8LuSpqnYl3za24W06zqm4Lwl1pQibLE2fIQwMaqJsR5nU0Hbh5TKOlVo/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=13)

▲ 有开发者直接回复"wrong"，残差连接并非自2015年从未被改动

学术史上，Highway Networks引入了门控，DenseNet做了跨层拼接，DeepSeek的**mHC（流形约束超连接）** 用多流并行加学习混合矩阵攻击同一个问题

![mHC优先权讨论](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreiavlNUSgj55iakDljQA55GCPwrt3cZIpKW9c6VrJvsIpyViah6661JX4WVjn3eGpo9GCdRRhRf1q83tz5yOTWWRLfpic1H8ACuKYrw/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=14)

▲ 有评论认为DeepSeek的mHC才是更早"破除残差禁忌"的工作

但技术向的讨论也给出了更精细的对比：论文消融显示Full AttnRes_一致优于_mHC；  
而Block AttnRes在性能接近的前提下，**每层内存I/O仅约5.5d，mHC四流配置下约34d**，差了6倍

![AttnRes vs mHC对比](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreiavJkibDibAtcnia1tkhHkXOiao87uPtBaoVYdZqAmsK03vX4MkLYmpjxIGACOojq8rYhbGac2wFr8gYUAfWSjNSJX1gLfiayX1eShhM/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=15)

▲ 社区技术讨论：AttnRes在内存I/O效率上显著优于mHC

更公允的表述或许是：**"跨层访问"从来不新；  
在工业级训练栈里把开销压到"可当残差替换件"的程度，门槛就在这里**

## 残差革命，才刚刚开始

AttnRes发布后不到四个月，学术圈已经炸开：**Delta Attention Residuals**对增量而非累积态做路由；  
**Low-Rank Attention Residuals**压缩参数预算；  
**Multi-Resolution Residual Routing**引入多分辨率块结构；  
甚至有研究者在小模型上追问，AttnRes的softmax会不会像序列注意力一样_制造attention sink_？

![Attention Sink实验（分段1）](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreiaun3aqIxYOpNksYofWynkBFgOHIqKBUp6iaC2fknqS1uXuYX1ic9Lnwq0XTl9RMZfAvImvf8wJ3wqsX0pdVoYIahxefCxFBMqbmc/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=16)![Attention Sink实验（分段2）](https://mmbiz.qpic.cn/mmbiz_jpg/wkbW3msreiasDcGWBGVTiaYpy69mqHu8ic8YLNtQ8jsV31pcAaYfBXFJIjBt9w4pOBpVTrQiawsZ2NXRKib81ibgqicVWruVjQSxqaCw4X3apmyqWU/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=17)

▲ 研究者在nanochat小模型上检验AttnRes是否存在"深度方向的attention sink"，初步结论是没有

**2025到2026年，残差连接突然从"默认不改项"变成了最活跃的研究前线**  
 稳定性、宽度、深度选择、访存效率，四条轴同时被扳动  
AttnRes给出一个模块家族的起点，远未成为终点公式

十年前，何恺明用一条恒等映射拯救了深度学习  
十年后，Kimi说：**光"加回去"还不够，你得学会"回头看"**

标准残差说：什么都加，继续往前。

Attention Residuals说：**回头看，决定什么重要，再带走**

K3的权重将于7月27日开源。  
届时，2.8万亿参数模型里的每一个Block AttnRes节点，都将变成可检查、可拆解、可追问的对象  
这场残差革命的第一页刚刚翻开，而下一页，**属于所有敢动那条线的人**