---
type: direction
tags:
  - inest
provenance: external
---

# 复杂网络智能涌现（iNEST/INEST）

## 入口锚点
- [[10_Knowledge/00_导航/00_iNEST_全景知识图谱|00_iNEST_全景知识图谱]]
- [[30_Outputs/论文/CST_Intelligence_Emergence_Paper_V22_Engineering_Format|CST 智能涌现理论（V22）]]
- [[00_KnowledgeBase_知识库/03_Inbox_文献与碎片/网络时空协同复杂度涌现智能|网络时空协同复杂度涌现智能]]

## 导入文献（自动汇总）
```datacorejsx
function Render() {
  const pages = dc.useQuery("@page");
  const rows = pages.filter(function(p) {
    var fm = p.$frontmatter || {};
    var tags = fm.tags || [];
    return tags.indexOf("inest") >= 0 && (p.$path || "").indexOf("00_Inbox/") === 0;
  });
  return <dc.List rows={rows} renderer={function(p) { return <dc.Link link={p.$link} />; }} />;
}
```
