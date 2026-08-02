<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>先有演化语言，再谈涌现机制 · SDDE</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>演化与调控 · 15</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', gap: '30px', padding: '30px 40px' }}>
      <Box style={{ width: '340px', background: '#0E3F8C', borderRadius: '12px', padding: '30px 26px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <Box>
          <Text style={{ fontSize: '16px', color: '#9FB6E0', letterSpacing: '2px' }}>STOCHASTIC DELAY DE</Text>
          <Text style={{ fontSize: '40px', fontWeight: 'bold', color: '#FFFFFF', marginTop: '12px', lineHeight: '1.2' }}>SDDE</Text>
          <Text style={{ fontSize: '22px', color: '#C9D8F0', marginTop: '10px', lineHeight: '1.4' }}>连续演化<Text style={{ color: '#FFC107' }}>语言</Text></Text>
        </Box>
        <Box style={{ background: 'rgba(255,255,255,0.10)', borderRadius: '8px', padding: '14px' }}>
          <Text style={{ fontSize: '17px', color: '#EAF1FB', lineHeight: '1.5' }}>先有演化语言，再有涌现调控机制——故置于 iNEST 之前更自洽。</Text>
        </Box>
      </Box>

      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '26px', fontWeight: 'bold', color: '#1E4FA8', lineHeight: '1.5' }}>带噪声、带时延、带记忆的连续演化</Text>
        <Box style={{ background: '#F0F5FC', border: '1px solid #3D7BD9', borderRadius: '12px', padding: '22px', marginTop: '18px', display: 'flex', justifyContent: 'center' }}>
          <Math latex="dx_i(t) = \left[ f_i + \sum_j A_{ij}(t) w_{ij}(t) g_{ij} + u_i \right] dt + \sigma_i dW_i(t)" width={640} display={true} color="#0E3F8C" />
        </Box>
        <Text style={{ fontSize: '22px', color: '#1A2230', lineHeight: '1.65', marginTop: '18px' }}>
          SDDE 刻画<Text style={{ fontWeight: 'bold', color: '#0E3F8C' }}>材料内部状态、非线性器件、拓扑耦合与环境反馈</Text>的共同演化；其中 A_{ij}(t) 正是 SDI 可直接调控的耦合结构。
        </Text>
        <Text style={{ fontSize: '15px', color: '#8B97A8', marginTop: '12px' }}>页脚佐证：Mohammed, 1984；Buckwar, 2000；Mao, 2007。</Text>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>介观尺度计算新范式 · 从SDSoW到iNEST</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>15 / 20</Text>
    </Box>
  </Box>
</Slide>
