<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>系统级摩尔定律正在兴起</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>引子 · 04</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', gap: '32px', padding: '30px 40px' }}>
      {/* 左主视觉：主航道结构图 */}
      <Box style={{ width: '620px', background: '#F0F5FC', border: '1px solid #D6DCE5', borderRadius: '12px', padding: '26px 28px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '20px', fontWeight: 'bold', color: '#0E3F8C', textAlign: 'center' }}>竞争焦点迁移：从微缩到集成</Text>
        <Box style={{ display: 'flex', justifyContent: 'center', marginTop: '18px' }}>
          <Box style={{ background: '#E8EFF8', border: '1px dashed #3D7BD9', borderRadius: '10px', padding: '14px 26px', textAlign: 'center' }}>
            <Text style={{ fontSize: '20px', color: '#4A5568' }}>旧范式：先进节点微缩</Text>
            <Text style={{ fontSize: '15px', color: '#8B97A8', marginTop: '4px', display: 'block' }}>逼近物理极限，红利衰减</Text>
          </Box>
        </Box>
        <Text style={{ fontSize: '30px', color: '#1E4FA8', textAlign: 'center', margin: '10px 0' }}>↓</Text>
        <Box style={{ background: '#0E3F8C', borderRadius: '10px', padding: '14px 26px', textAlign: 'center' }}>
          <Text style={{ fontSize: '22px', fontWeight: 'bold', color: '#FFFFFF' }}>新范式：系统级摩尔定律</Text>
        </Box>
        <Box style={{ display: 'flex', gap: '14px', justifyContent: 'center', marginTop: '18px' }}>
          {['SoW\n晶圆级', '先进封装\n2.5D / 3D', '3DHI\n异质集成'].map((s, i) => (
            <Box key={i} style={{ flex: 1, background: '#FFFFFF', border: '1px solid #3D7BD9', borderRadius: '10px', padding: '16px 10px', textAlign: 'center' }}>
              <Text style={{ fontSize: '20px', fontWeight: 'bold', color: '#1E4FA8', whiteSpace: 'pre-line' }}>{s}</Text>
            </Box>
          ))}
        </Box>
      </Box>

      {/* 右正文 */}
      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '26px', fontWeight: 'bold', color: '#1E4FA8', lineHeight: '1.5' }}>SoW、先进封装、3DHI 成为主航道</Text>
        <Box style={{ height: '2px', background: '#D6DCE5', margin: '14px 0 16px' }} />
        <Text style={{ fontSize: '22px', color: '#1A2230', lineHeight: '1.65' }}>
          全球竞争的主战场，正从“把晶体管做得更小”，转向“把系统集得更巧”：晶圆级集成（SoW）、Chiplet 先进封装、三维异质集成（3DHI）共同构成<Text style={{ fontWeight: 'bold', color: '#0E3F8C' }}>系统级摩尔定律</Text>。
        </Text>
        <Text style={{ fontSize: '22px', color: '#4A5568', lineHeight: '1.65', marginTop: '14px' }}>
          这意味着价值重心上移到体系结构与互连创新——也为介观物理网络提供了难得的换道窗口。
        </Text>
        <Box style={{ marginTop: 'auto', background: '#F0F5FC', borderLeft: '4px solid #1E4FA8', borderRadius: '6px', padding: '12px 18px' }}>
          <Text style={{ fontSize: '15px', color: '#8B97A8' }}>页脚佐证：IRDS；Heterogeneous Integration Roadmap；DARPA NGMM；NSTC；TSMC SoW；Cerebras WSE。</Text>
        </Box>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>介观尺度计算新范式 · 从SDSoW到iNEST</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>04 / 20</Text>
    </Box>
  </Box>
</Slide>
