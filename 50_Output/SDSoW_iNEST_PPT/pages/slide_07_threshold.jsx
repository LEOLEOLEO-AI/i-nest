<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>复杂度要从不可说走向可度量</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>资源与刻度 · 07</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', gap: '30px', padding: '30px 40px' }}>
      {/* 左标题 + 引用 */}
      <Box style={{ width: '360px', background: '#0E3F8C', borderRadius: '12px', padding: '30px 26px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <Box>
          <Text style={{ fontSize: '16px', color: '#9FB6E0', letterSpacing: '2px' }}>THRESHOLD → CST</Text>
          <Text style={{ fontSize: '34px', fontWeight: 'bold', color: '#FFFFFF', marginTop: '12px', lineHeight: '1.3' }}>先立刻度</Text>
          <Text style={{ fontSize: '34px', fontWeight: 'bold', color: '#FFFFFF', lineHeight: '1.3' }}>再谈涌现</Text>
        </Box>
        <Box style={{ background: 'rgba(255,255,255,0.10)', borderRadius: '8px', padding: '16px', borderLeft: '4px solid #FFC107' }}>
          <Text style={{ fontSize: '18px', color: '#EAF1FB', lineHeight: '1.55', fontStyle: 'italic' }}>“复杂自动机的组织，存在使功能跃迁的阈值。”</Text>
          <Text style={{ fontSize: '15px', color: '#9FB6E0', marginTop: '8px', display: 'block' }}>—— 借鉴冯·诺依曼阈值思想的问题起点</Text>
        </Box>
      </Box>

      {/* 右正文 */}
      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Text style={{ fontSize: '26px', fontWeight: 'bold', color: '#1E4FA8', lineHeight: '1.5' }}>先立复杂度刻度，再谈智能涌现</Text>
        <Box style={{ height: '2px', background: '#D6DCE5', margin: '16px 0 18px' }} />
        <Text style={{ fontSize: '22px', color: '#1A2230', lineHeight: '1.65' }}>
          借鉴冯·诺依曼关于复杂自动机组织的<Text style={{ fontWeight: 'bold', color: '#0E3F8C' }}>阈值思想</Text>，我们并不宣称他提出了 CST 公式，而是以其思想为问题起点：首先定义一套复杂度刻度 CST，使系统的复杂度变得<Text style={{ fontWeight: 'bold', color: '#1E4FA8' }}>可观测、可度量、可预测、可调控</Text>。
        </Text>
        <Text style={{ fontSize: '22px', color: '#4A5568', lineHeight: '1.65', marginTop: '14px' }}>
          没有刻度，智能涌现就停留在比喻层面；有了刻度，匹配、同步与涌现才能成为可被工程化追求的目标。
        </Text>
        <Box style={{ marginTop: 'auto', background: '#FFF6E6', borderLeft: '4px solid #FFC107', borderRadius: '6px', padding: '14px 18px' }}>
          <Text style={{ fontSize: '17px', color: '#8A6D2B' }}>口播边界：不说“冯·诺依曼提出了 CST 公式”，仅说其阈值思想启发了问题起点。</Text>
        </Box>
        <Text style={{ fontSize: '15px', color: '#8B97A8', marginTop: '12px' }}>页脚佐证：von Neumann, 1956；von Neumann, 1966；Ashby, 1956。</Text>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>介观尺度计算新范式 · 从SDSoW到iNEST</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>07 / 20</Text>
    </Box>
  </Box>
</Slide>
