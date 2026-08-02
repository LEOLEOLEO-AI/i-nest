<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>SDSoW 让介观网络资源可定义</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>资源与刻度 · 05</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', gap: '32px', padding: '30px 40px' }}>
      {/* 左：尺度轴 */}
      <Box style={{ width: '500px', background: '#F0F5FC', border: '1px solid #D6DCE5', borderRadius: '12px', padding: '26px 28px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '18px', fontWeight: 'bold', color: '#0E3F8C', textAlign: 'center', marginBottom: '14px' }}>资源尺度轴（自下而上扩展）</Text>
        {[
          { t: '芯片 / Chiplet', w: '62%', c: '#E8EFF8' },
          { t: '晶圆 / 晶矩', w: '76%', c: '#D6E4F7' },
          { t: '面板级', w: '88%', c: '#BBD2F2' },
          { t: '机架 / 集群', w: '100%', c: '#0E3F8C' },
        ].map((b, i) => (
          <Box key={i} style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '14px' }}>
            <Box style={{ width: b.w, background: b.c, borderRadius: '8px', padding: '14px 16px' }}>
              <Text style={{ fontSize: '19px', fontWeight: 'bold', color: b.c === '#0E3F8C' ? '#FFFFFF' : '#0E3F8C' }}>{b.t}</Text>
            </Box>
            <Text style={{ fontSize: '22px', color: '#3D7BD9' }}>↑</Text>
          </Box>
        ))}
      </Box>

      {/* 右正文 */}
      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '26px', fontWeight: 'bold', color: '#1E4FA8', lineHeight: '1.5' }}>高密度 · 高维度 · 大规模 · 动态可塑</Text>
        <Box style={{ height: '2px', background: '#D6DCE5', margin: '14px 0 16px' }} />
        <Text style={{ fontSize: '22px', color: '#1A2230', lineHeight: '1.65' }}>
          SDSoW（Software-Defined System on Wafer）在<Text style={{ fontWeight: 'bold', color: '#0E3F8C' }}>晶圆 / 晶矩 / 面板级</Text>尺度上，把物理资源组织成可重构网络，兼具芯片的密度与系统的规模。
        </Text>
        <Text style={{ fontSize: '22px', color: '#4A5568', lineHeight: '1.65', marginTop: '14px' }}>
          它首次让“介观物理网络资源”成为可被定义、调度与编程的对象——这是后续所有复杂度调控的物质前提。
        </Text>
        <Box style={{ marginTop: 'auto', background: '#F0F5FC', borderLeft: '4px solid #1E4FA8', borderRadius: '6px', padding: '12px 18px' }}>
          <Text style={{ fontSize: '15px', color: '#8B97A8' }}>页脚佐证：IRDS；Heterogeneous Integration Roadmap；Cerebras WSE 公开资料。</Text>
        </Box>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>介观尺度计算新范式 · 从SDSoW到iNEST</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>05 / 20</Text>
    </Box>
  </Box>
</Slide>
