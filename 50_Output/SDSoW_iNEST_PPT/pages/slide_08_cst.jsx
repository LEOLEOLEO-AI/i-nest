<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: 'linear-gradient(90deg,#0E3F8C,#1E4FA8)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>可用时空协同复杂度 · CST V4.0</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>资源与刻度 · 08</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '20px 50px' }}>
      <Text style={{ fontSize: '18px', color: '#8B97A8', letterSpacing: '2px' }}>COMPLEXITY OF SPACE–TIME SYNERGY (CAPABLE)</Text>
      {/* 公式主视觉带 */}
      <Box style={{ background: '#F0F5FC', border: '1px solid #3D7BD9', borderRadius: '14px', padding: '26px 40px', marginTop: '14px' }}>
        <Math latex="C_{\mathrm{ST}}^{\mathrm{cap}}(t) = S_c(t)\cdot T_c(t)\cdot \exp\left[ \alpha_{\mathrm{eff}}(t)\cdot \Gamma_{\mathrm{st}}^{u}(t) \right]" width={760} display={true} color="#0E3F8C" />
      </Box>

      {/* 参数四联 */}
      <Box style={{ display: 'flex', gap: '16px', marginTop: '22px', width: '100%', justifyContent: 'center' }}>
        {[
          { k: 'S_c', d: '空间拓扑组织能力' },
          { k: 'T_c', d: '时间演化与记忆能力' },
          { k: 'α_eff', d: '非平衡态有效状态容量' },
          { k: 'Γ_st^u', d: '结构·功能·环境匹配度' },
        ].map((p, i) => (
          <Box key={i} style={{ flex: '1', maxWidth: '250px', background: '#FFFFFF', border: '1px solid #D6DCE5', borderRadius: '10px', padding: '14px 16px', textAlign: 'center' }}>
            <Text style={{ fontSize: '24px', fontWeight: 'bold', color: '#1E4FA8', display: 'block' }}>{p.k}</Text>
            <Text style={{ fontSize: '17px', color: '#4A5568', marginTop: '6px', display: 'block' }}>{p.d}</Text>
          </Box>
        ))}
      </Box>

      <Box style={{ marginTop: '22px', background: '#FFF6E6', borderLeft: '4px solid #FFC107', borderRadius: '6px', padding: '14px 22px', maxWidth: '860px' }}>
        <Text style={{ fontSize: '22px', fontWeight: 'bold', color: '#8A6D2B' }}>金句：S_c·T_c 是复杂度底座，指数项是协同放大器。</Text>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>页脚佐证：Anderson, 1972；Watts & Strogatz, Nature, 1998；Bullmore & Sporns, NRN, 2009。</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>08 / 20</Text>
    </Box>
  </Box>
</Slide>
