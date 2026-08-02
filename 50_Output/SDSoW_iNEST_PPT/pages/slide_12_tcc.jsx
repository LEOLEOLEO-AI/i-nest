<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>用液态拓扑实现复杂性匹配 · TCC</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>度量与匹配 · 12</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', gap: '30px', padding: '30px 40px' }}>
      <Box style={{ width: '340px', background: '#0E3F8C', borderRadius: '12px', padding: '30px 26px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <Box>
          <Text style={{ fontSize: '16px', color: '#9FB6E0', letterSpacing: '2px' }}>TOPOLOGY-CENTRIC</Text>
          <Text style={{ fontSize: '34px', fontWeight: 'bold', color: '#FFFFFF', marginTop: '12px', lineHeight: '1.3' }}>TCC</Text>
          <Text style={{ fontSize: '24px', color: '#C9D8F0', marginTop: '10px', lineHeight: '1.4' }}>拓扑中心<Text style={{ color: '#FFC107' }}>计算</Text></Text>
        </Box>
        <Box style={{ background: 'rgba(255,255,255,0.10)', borderRadius: '8px', padding: '14px' }}>
          <Text style={{ fontSize: '17px', color: '#EAF1FB', lineHeight: '1.5' }}>第一阶段目标：让系统复杂度<Text style={{ fontWeight: 'bold', color: '#FFE08A' }}>动态匹配</Text>环境复杂度。</Text>
        </Box>
      </Box>

      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '26px', fontWeight: 'bold', color: '#1E4FA8', lineHeight: '1.5' }}>系统复杂度匹配环境复杂度</Text>
        <Box style={{ height: '2px', background: '#D6DCE5', margin: '14px 0 16px' }} />
        <Text style={{ fontSize: '22px', color: '#1A2230', lineHeight: '1.65' }}>
          TCC 基于 SDI，从<Text style={{ fontWeight: 'bold', color: '#0E3F8C' }}>复杂度视角</Text>调节拓扑，使系统复杂度动态逼近环境复杂度。当结构被持续塑形，资源中的非线性被唤醒，产生系统级超线性增益。
        </Text>
        <Box style={{ background: '#F0F5FC', border: '1px solid #3D7BD9', borderRadius: '10px', padding: '18px 24px', marginTop: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Math latex="C_{\mathrm{ST}}^{\mathrm{sys}} \approx C_{\mathrm{ST}}^{\mathrm{env}} \quad \Rightarrow \quad 1+1>2" width={520} display={true} color="#0E3F8C" />
        </Box>
        <Text style={{ fontSize: '15px', color: '#8B97A8', marginTop: '14px' }}>页脚佐证：Dally & Towles, Interconnection Networks；Hennessy & Patterson, 2019。</Text>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>介观尺度计算新范式 · 从SDSoW到iNEST</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>12 / 20</Text>
    </Box>
  </Box>
</Slide>
