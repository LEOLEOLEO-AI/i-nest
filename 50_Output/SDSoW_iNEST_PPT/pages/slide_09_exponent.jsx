<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>指数放大从材料与非线性动力学中来</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>资源与刻度 · 09</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', gap: '32px', padding: '30px 40px' }}>
      {/* 左正文 + 公式 */}
      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '26px', fontWeight: 'bold', color: '#1E4FA8', lineHeight: '1.5' }}>材料状态容量 × 时空协同匹配</Text>
        <Box style={{ height: '2px', background: '#D6DCE5', margin: '14px 0 16px' }} />
        <Text style={{ fontSize: '22px', color: '#1A2230', lineHeight: '1.65' }}>
          Mott 相变、忆阻、相变、铁电、离子迁移等<Text style={{ fontWeight: 'bold', color: '#0E3F8C' }}>非平衡过程</Text>为系统提供内部状态变量。当材料状态容量与网络拓扑、时间动力学和环境需求匹配时，系统响应进入协同放大区。
        </Text>
        <Box style={{ background: '#F0F5FC', border: '1px solid #3D7BD9', borderRadius: '10px', padding: '16px 22px', marginTop: '20px', display: 'flex', alignItems: 'center', gap: '18px' }}>
          <Text style={{ fontSize: '21px', color: '#1A2230' }}>有效状态容量：</Text>
          <Math latex="\alpha_{\mathrm{eff}} \approx \ln M_{\mathrm{eff}} \quad \text{或} \quad I(z_i; y_i)" width={420} color="#0E3F8C" />
        </Box>
        <Text style={{ fontSize: '15px', color: '#8B97A8', marginTop: '14px' }}>页脚佐证：Chua, 1971；Strukov et al., Nature, 2008；Pickett et al., Nature Materials, 2013；Marković et al., Nat Rev Phys, 2020。</Text>
      </Box>

      {/* 右：材料家族 */}
      <Box style={{ width: '480px', background: '#F0F5FC', border: '1px solid #D6DCE5', borderRadius: '12px', padding: '24px 26px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '19px', fontWeight: 'bold', color: '#0E3F8C', textAlign: 'center', marginBottom: '16px' }}>内部状态变量来源（非线性器件）</Text>
        <Box style={{ display: 'flex', flexWrap: 'wrap', gap: '14px', justifyContent: 'center' }}>
          {['Mott 相变', '忆阻', '相变', '铁电', '离子迁移', '非线性动力学'].map((m, i) => (
            <Box key={i} style={{ background: '#FFFFFF', border: '1px solid #3D7BD9', borderRadius: '20px', padding: '14px 20px' }}>
              <Text style={{ fontSize: '20px', fontWeight: 'bold', color: '#1E4FA8' }}>{m}</Text>
            </Box>
          ))}
        </Box>
        <Box style={{ marginTop: '20px', background: '#0E3F8C', borderRadius: '8px', padding: '14px' }}>
          <Text style={{ fontSize: '19px', color: '#FFFFFF', textAlign: 'center' }}>容量 × 拓扑 × 动力学 × 环境 → 协同放大区</Text>
        </Box>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>介观尺度计算新范式 · 从SDSoW到iNEST</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>09 / 20</Text>
    </Box>
  </Box>
</Slide>
