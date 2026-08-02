<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: 'linear-gradient(90deg,#0E3F8C,#1E4FA8)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>智能是系统复杂度对环境复杂度的相对裕度</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>度量与匹配 · 10</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '16px 50px' }}>
      <Text style={{ fontSize: '18px', color: '#8B97A8', letterSpacing: '2px' }}>RELATIVE INTELLIGENCE INDEX</Text>
      <Box style={{ background: '#F0F5FC', border: '1px solid #3D7BD9', borderRadius: '14px', padding: '22px 40px', marginTop: '12px' }}>
        <Math latex="R_I(t) = \frac{C_{\mathrm{ST}}^{\mathrm{sys}}(t)}{C_{\mathrm{ST}}^{\mathrm{env}}(t)}" width={560} display={true} color="#0E3F8C" />
      </Box>
      <Text style={{ fontSize: '19px', color: '#4A5568', marginTop: '12px', textAlign: 'center' }}>
        <Text style={{ fontWeight: 'bold', color: '#0E3F8C' }}>C_ST^sys</Text>：系统可用时空协同复杂度　·　<Text style={{ fontWeight: 'bold', color: '#0E3F8C' }}>C_ST^env</Text>：广义环境复杂度（环境状态·任务目标·扰动强度·实时约束·行动边界）
      </Text>

      {/* 三档判据 */}
      <Box style={{ display: 'flex', gap: '16px', marginTop: '18px', width: '100%', justifyContent: 'center' }}>
        <Box style={{ flex: '1', maxWidth: '360px', background: '#EEF1F5', border: '1px solid #D6DCE5', borderRadius: '10px', padding: '16px' }}>
          <Text style={{ fontSize: '24px', fontWeight: 'bold', color: '#D9534F' }}>R_I &lt; 1</Text>
          <Text style={{ fontSize: '19px', color: '#4A5568', marginTop: '8px', display: 'block' }}>难以胜任任务</Text>
        </Box>
        <Box style={{ flex: '1', maxWidth: '360px', background: '#E8EFF8', border: '1px solid #3D7BD9', borderRadius: '10px', padding: '16px' }}>
          <Text style={{ fontSize: '24px', fontWeight: 'bold', color: '#1E4FA8' }}>R_I ≈ 1</Text>
          <Text style={{ fontSize: '19px', color: '#4A5568', marginTop: '8px', display: 'block' }}>能力与任务难度相匹配</Text>
        </Box>
        <Box style={{ flex: '1', maxWidth: '360px', background: '#D6E4F7', border: '1px solid #1E4FA8', borderRadius: '10px', padding: '16px' }}>
          <Text style={{ fontSize: '24px', fontWeight: 'bold', color: '#0E3F8C' }}>R_I &gt; 1</Text>
          <Text style={{ fontSize: '19px', color: '#1A2230', marginTop: '8px', display: 'block' }}>游刃有余，具备更高等级能力余裕</Text>
        </Box>
      </Box>

      <Box style={{ marginTop: '16px', background: '#FFF6E6', borderLeft: '4px solid #FFC107', borderRadius: '6px', padding: '12px 20px', maxWidth: '900px' }}>
        <Text style={{ fontSize: '18px', color: '#8A6D2B' }}>判据修订：不再写“远大于1进入候选区”；统一为 小于1 / 约等于1 / 大于1 三档，不同区间对应不同智能等级（见 P11）。</Text>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>页脚佐证：Ashby, 1956；Friston, Nature Reviews Neuroscience, 2010。</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>10 / 20</Text>
    </Box>
  </Box>
</Slide>
