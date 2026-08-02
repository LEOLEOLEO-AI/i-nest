<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>不同智能裕度，对应不同智能等级</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>度量与匹配 · 11</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', gap: '30px', padding: '26px 40px' }}>
      {/* 左标题 + 公式 */}
      <Box style={{ width: '340px', background: '#0E3F8C', borderRadius: '12px', padding: '28px 26px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <Box>
          <Text style={{ fontSize: '16px', color: '#9FB6E0', letterSpacing: '2px' }}>SIX-LEVEL FRAMEWORK</Text>
          <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF', marginTop: '12px', lineHeight: '1.3' }}>裕度决定</Text>
          <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF', lineHeight: '1.3' }}>智能等级</Text>
        </Box>
        <Box style={{ background: 'rgba(255,255,255,0.10)', borderRadius: '8px', padding: '16px' }}>
          <Text style={{ fontSize: '16px', color: '#DCE7F8', display: 'block', marginBottom: '8px' }}>等级由最大可胜任复杂度决定：</Text>
          <Math latex="L = \max_k\left\{ R_I^{(k)} \geq 1 \right\}" width={270} color="#FFFFFF" />
        </Box>
      </Box>

      {/* 右六级阶梯 */}
      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '9px', justifyContent: 'center' }}>
        {[
          { lv: 'L1', n: '感知', d: '提取稳定环境信息', c: '#E8EFF8' },
          { lv: 'L2', n: '反应', d: '形成低延迟闭环', c: '#D6E4F7' },
          { lv: 'L3', n: '适应', d: '在线调整状态或结构', c: '#BBD2F2' },
          { lv: 'L4', n: '创造', d: '形成新策略或新吸引子', c: '#8FB6EC' },
          { lv: 'L5', n: '通用', d: '跨环境迁移与整合', c: '#5C86C9' },
          { lv: 'L6', n: '超级', d: '受控自演化与能力提升', c: '#0E3F8C' },
        ].map((x, i) => (
          <Box key={i} style={{ display: 'flex', alignItems: 'center', gap: '16px', background: x.c, borderRadius: '10px', padding: '12px 18px' }}>
            <Text style={{ fontSize: '26px', fontWeight: 'bold', color: x.c === '#0E3F8C' ? '#FFFFFF' : '#0E3F8C', width: '60px' }}>{x.lv}</Text>
            <Text style={{ fontSize: '24px', fontWeight: 'bold', color: x.c === '#0E3F8C' ? '#FFFFFF' : '#0E3F8C', width: '90px' }}>{x.n}</Text>
            <Text style={{ fontSize: '20px', color: x.c === '#0E3F8C' ? '#EAF1FB' : '#1A2230' }}>{x.d}</Text>
          </Box>
        ))}
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>边界：六级为操作化等级框架，阈值需持续校准。佐证：Bassett & Sporns, 2017；Friston, 2010。</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>11 / 20</Text>
    </Box>
  </Box>
</Slide>
