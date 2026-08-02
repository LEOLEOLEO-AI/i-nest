<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: 'linear-gradient(90deg,#0E3F8C,#1E4FA8)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>连续演化，需要离散拓扑执行器 · SDI</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>演化与调控 · 16</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '14px 50px' }}>
      <Text style={{ fontSize: '18px', color: '#8B97A8', letterSpacing: '2px' }}>SDI TOPOLOGY CONTROL OPERATOR（工程控制律）</Text>
      <Box style={{ background: '#F0F5FC', border: '2px solid #1E4FA8', borderRadius: '14px', padding: '22px 34px', marginTop: '12px' }}>
        <Math latex="A(t^+) = \Pi_{\mathrm{SDI}}\left[ A(t), \lambda_{\max}^{FT}, \hat{m}, TE, AIS, E_{\mathrm{diss}}, \Gamma_{\mathrm{st}}^{u} \right]" width={860} display={true} color="#0E3F8C" />
      </Box>

      {/* 输入参数七联 */}
      <Box style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', justifyContent: 'center', marginTop: '18px', width: '100%' }}>
        {[
          { k: 'A(t)', d: '当前拓扑' }, { k: 'λ_max^FT', d: '有限时间李雅普诺夫指数' }, { k: 'm̂', d: '分支比' },
          { k: 'TE', d: '传递熵' }, { k: 'AIS', d: '动态信息存储' }, { k: 'E_diss', d: '耗散能量' }, { k: 'Γ_st^u', d: '可用时空协同因子' },
        ].map((p, i) => (
          <Box key={i} style={{ background: '#FFFFFF', border: '1px solid #D6DCE5', borderRadius: '8px', padding: '8px 12px', textAlign: 'center' }}>
            <Text style={{ fontSize: '18px', fontWeight: 'bold', color: '#1E4FA8', display: 'block' }}>{p.k}</Text>
            <Text style={{ fontSize: '13px', color: '#8B97A8', marginTop: '2px', display: 'block' }}>{p.d}</Text>
          </Box>
        ))}
      </Box>

      <Box style={{ marginTop: '18px', background: '#E8EFF8', borderLeft: '4px solid #1E4FA8', borderRadius: '6px', padding: '14px 22px', maxWidth: '980px' }}>
        <Text style={{ fontSize: '20px', color: '#0E3F8C', lineHeight: '1.55' }}>SDI 拓扑调控算子：从“受控 SDDE 混合动力系统”中抽象出的<Text style={{ fontWeight: 'bold' }}>工程控制律</Text>，而非自然定律公式。</Text>
      </Box>
      <Box style={{ marginTop: '12px', background: '#FFF6E6', borderLeft: '4px solid #FFC107', borderRadius: '6px', padding: '12px 22px', maxWidth: '980px' }}>
        <Text style={{ fontSize: '17px', color: '#8A6D2B' }}>口播边界：这是工程控制抽象，不宣称为已证明的普适定律。</Text>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>页脚佐证：Liu, Slotine & Barabási, Nature, 2011；Schreiber, PRL, 2000；Lizier, 2012。</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>16 / 20</Text>
    </Box>
  </Box>
</Slide>
