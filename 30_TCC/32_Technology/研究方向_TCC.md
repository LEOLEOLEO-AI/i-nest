---
type: direction
tags:
  - tcc
provenance: own
---

# 网络中心计算（TCC）

## 入口锚点
- TCC_Core_Concepts
- SDI-CC论文框架_拓扑即计算新范式
- 网内原生 AI 通信加速系统

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

---
## 相关笔记 (AI 自动关联)
- [[海河实验室_项目汇报_Marp]]
- [[SDI-软件定义互连]]
