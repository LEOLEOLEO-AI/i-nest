<Slide>
  <Box style={{ width: '1280px', height: '720px', background: 'linear-gradient(135deg, #0E3F8C 0%, #1E4FA8 60%, #3D7BD9 100%)', display: 'flex', flexDirection: 'column', padding: '56px 80px', position: 'relative' }}>
    {/* 顶部机构与标签 */}
    <Box style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <Text style={{ fontSize: '18px', color: '#C9D8F0' }}>国家数字交换系统工程技术研究中心 · 复旦大学大数据研究院</Text>
      <Text style={{ fontSize: '15px', color: '#DCE7F8', border: '1px solid #5C86C9', padding: '6px 16px', borderRadius: '20px' }}>后冯·诺依曼时代 · 换道引领战略机遇</Text>
    </Box>

    {/* 主标题区 */}
    <Box style={{ marginTop: '54px' }}>
      <Text style={{ fontSize: '17px', color: '#9FB6E0', letterSpacing: '3px', fontStyle: 'italic' }}>MESOSCOPIC COMPUTING NEW PARADIGM</Text>
      <Text style={{ fontSize: '62px', fontWeight: 'bold', color: '#FFFFFF', marginTop: '14px', lineHeight: '1.18' }}>介观尺度计算新范式</Text>
      <Text style={{ fontSize: '38px', fontWeight: 'bold', color: '#EAF1FB', marginTop: '12px' }}>——从 SDSoW 到 iNEST 智能涌现之路</Text>
    </Box>

    {/* 概念演化链（主视觉） */}
    <Box style={{ marginTop: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '18px' }}>
      {[
        { t: '晶圆 / 晶矩平台', s: '介观物理资源' },
        { t: '液态拓扑', s: '复杂度匹配' },
        { t: '智涌脑', s: '智能涌现' },
        { t: '具身智能体', s: '自主行为' },
      ].map((n, i) => (
        <Box key={i} style={{ display: 'flex', alignItems: 'center', gap: '18px' }}>
          <Box style={{ width: '210px', background: 'rgba(255,255,255,0.10)', border: '1px solid rgba(255,255,255,0.35)', borderRadius: '14px', padding: '16px 18px', textAlign: 'center' }}>
            <Text style={{ fontSize: '24px', fontWeight: 'bold', color: '#FFFFFF', display: 'block' }}>{n.t}</Text>
            <Text style={{ fontSize: '15px', color: '#BBD0F0', marginTop: '6px', display: 'block' }}>{n.s}</Text>
          </Box>
          {i < 3 && <Text style={{ fontSize: '34px', color: '#FFC107', fontWeight: 'bold' }}>→</Text>}
        </Box>
      ))}
    </Box>

    {/* 底部：报告人 + 金句 */}
    <Box style={{ marginTop: 'auto', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
      <Box>
        <Text style={{ fontSize: '22px', color: '#FFFFFF' }}>报告人：<Text style={{ fontWeight: 'bold', fontSize: '24px' }}>邬江兴 院士</Text></Text>
        <Text style={{ fontSize: '16px', color: '#C9D8F0', marginTop: '8px' }}>国家数字交换系统工程技术研究中心 · 复旦大学大数据研究院</Text>
      </Box>
      <Box style={{ background: 'rgba(255,255,255,0.12)', borderLeft: '4px solid #FFC107', padding: '12px 20px', borderRadius: '6px', maxWidth: '420px' }}>
        <Text style={{ fontSize: '22px', fontWeight: 'bold', color: '#FFE08A' }}>“让物理网络自己长出智能”</Text>
      </Box>
    </Box>
  </Box>
</Slide>
