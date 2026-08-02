<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>局部规则推动系统接近临界 · iNEST</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>演化与调控 · 17</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', gap: '30px', padding: '30px 40px' }}>
      <Box style={{ width: '340px', background: '#0E3F8C', borderRadius: '12px', padding: '30px 26px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <Box>
          <Text style={{ fontSize: '16px', color: '#9FB6E0', letterSpacing: '2px' }}>CRITICAL INTELLIGENCE</Text>
          <Text style={{ fontSize: '40px', fontWeight: 'bold', color: '#FFFFFF', marginTop: '12px', lineHeight: '1.2' }}>iNEST</Text>
          <Text style={{ fontSize: '22px', color: '#C9D8F0', marginTop: '10px', lineHeight: '1.4' }}>临界智能区</Text>
        </Box>
        <Box style={{ background: 'rgba(255,255,255,0.10)', borderRadius: '8px', padding: '14px' }}>
          <Text style={{ fontSize: '17px', color: '#EAF1FB', lineHeight: '1.5' }}>塑边 · 选向 · 稳态 · 临界——逼近混沌边缘。</Text>
        </Box>
      </Box>

      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '23px', color: '#1A2230', lineHeight: '1.6', marginBottom: '14px' }}>
          iNEST 通过<Text style={{ fontWeight: 'bold', color: '#0E3F8C' }}>局部规则与 SDI 调控</Text>，使复杂度在介观物理网络中持续演化，接近混沌边缘并形成稳定吸引子。
        </Text>
        <Table
          style={{ width: '100%', height: '320px' }}
          defaultTextStyle={{ fontSize: '20px', textAlign: 'left', color: '#1A2230' }}
          defaultCellStyle={{ border: { left: { width: 1, color: '#D6DCE5' }, right: { width: 1, color: '#D6DCE5' }, top: { width: 1, color: '#D6DCE5' }, bottom: { width: 1, color: '#D6DCE5' } } }}
          cells={[
            [
              { text: '机制', textStyle: { bold: true, color: '#FFFFFF', fontSize: '21px' }, cellStyle: { background: { color: '#0E3F8C' } } },
              { text: '作用', textStyle: { bold: true, color: '#FFFFFF', fontSize: '21px' }, cellStyle: { background: { color: '#0E3F8C' } } },
            ],
            ['STDP', '按时序塑造连接'],
            [{ text: '局部预测误差', cellStyle: { background: { color: '#F0F5FC' } } }, { text: '引导状态向低误差吸引子收敛', cellStyle: { background: { color: '#F0F5FC' } } }],
            ['稳态可塑性', '防止全静默或全饱和'],
            [{ text: 'SOC / EOC', cellStyle: { background: { color: '#F0F5FC' } } }, { text: '维持临界窗口', cellStyle: { background: { color: '#F0F5FC' } } }],
          ]}
        />
        <Text style={{ fontSize: '15px', color: '#8B97A8', marginTop: '14px' }}>页脚佐证：Bi & Poo, J Neurosci, 1998；Bak et al., PRL, 1987；Kinouchi & Copelli, Nature Physics, 2006。</Text>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>介观尺度计算新范式 · 从SDSoW到iNEST</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>17 / 20</Text>
    </Box>
  </Box>
</Slide>
