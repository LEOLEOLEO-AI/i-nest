---
type: direction
tags:
  - tcc
provenance: own
---

# 网络中心计算（TCC）

## 入口锚点
- [[10_Knowledge/主题知识/CST_核心理论/TCC_Core_Concepts|TCC_Core_Concepts]]
- [[30_Outputs/论文/B组_SDI-CC互连体系/SDI-CC论文框架_拓扑即计算新范式|SDI-CC论文框架_拓扑即计算新范式]]
- [[10_Knowledge/99_参考资料/04_会议战略/面向万亿参数大模型训练的SDI_软件定义互联___网内原生_AI_通信加速系统|网内原生 AI 通信加速系统]]

## 导入文献（自动汇总）
```datacorejsx
function Render() {
  const pages = dc.useQuery("@page");
  const rows = pages.filter(function(p) {
    var fm = p.$frontmatter || {};
    var tags = fm.tags || [];
    return tags.indexOf("tcc") >= 0 && (p.$path || "").indexOf("00_Inbox/") === 0;
  });
  return <dc.List rows={rows} renderer={function(p) { return <dc.Link link={p.$link} />; }} />;
}
```
