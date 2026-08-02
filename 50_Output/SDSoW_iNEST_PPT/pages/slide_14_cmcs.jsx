<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>从复杂性匹配到复杂性同步</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>度量与匹配 · 14</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '26px 40px' }}>
      <Text style={{ fontSize: '26px', fontWeight: 'bold', color: '#1E4FA8', textAlign: 'center' }}>CM 是匹配，CS 是同步，EI 是涌现</Text>

      {/* 上：三段推进带 */}
      <Box style={{ display: 'flex', alignItems: 'stretch', justifyContent: 'center', gap: '16px', marginTop: '20px' }}>
        {[
          { t: 'CM', s: '复杂性匹配', c: '#E8EFF8', tc: '#0E3F8C' },
          { t: 'CS', s: '复杂性同步', c: '#BBD2F2', tc: '#0E3F8C' },
          { t: 'EI', s: '复杂性涌现', c: '#0E3F8C', tc: '#FFFFFF' },
        ].map((x, i) => (
          <Box key={i} style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <Box style={{ width: '300px', background: x.c, borderRadius: '12px', padding: '22px', textAlign: 'center' }}>
              <Text style={{ fontSize: '40px', fontWeight: 'bold', color: x.tc, display: 'block' }}>{x.t}</Text>
              <Text style={{ fontSize: '22px', color: x.tc, marginTop: '6px', display: 'block' }}>{x.s}</Text>
            </Box>
            {i < 2 && <Text style={{ fontSize: '40px', color: '#1E4FA8', fontWeight: 'bold' }}>→</Text>}
          </Box>
        ))}
      </Box>

      {/* 下：三卡 */}
      <Box style={{ display: 'flex', gap: '20px', marginTop: '24px', flex: 1 }}>
        <Box style={{ flex: 1, background: '#F0F5FC', border: '1px solid #D6DCE5', borderTop: '5px solid #3D7BD9', borderRadius: '10px', padding: '18px 20px' }}>
          <Text style={{ fontSize: '23px', fontWeight: 'bold', color: '#0E3F8C' }}>CM：匹配</Text>
          <Text style={{ fontSize: '20px', color: '#4A5568', lineHeight: '1.55', marginTop: '10px', display: 'block' }}>TCC 使系统复杂度匹配环境，形成 1+1&gt;2 的超线性增益。</Text>
        </Box>
        <Box style={{ flex: 1, background: '#F0F5FC', border: '1px solid #D6DCE5', borderTop: '5px solid #1E4FA8', borderRadius: '10px', padding: '18px 20px' }}>
          <Text style={{ fontSize: '23px', fontWeight: 'bold', color: '#0E3F8C' }}>CS：同步</Text>
          <Text style={{ fontSize: '20px', color: '#4A5568', lineHeight: '1.55', marginTop: '10px', display: 'block' }}>多子系统高阶复杂特征发生同步，迈向 1+1&gt;N。</Text>
        </Box>
        <Box style={{ flex: 1, background: '#0E3F8C', borderRadius: '10px', padding: '18px 20px' }}>
          <Text style={{ fontSize: '23px', fontWeight: 'bold', color: '#FFFFFF' }}>EI：涌现</Text>
          <Text style={{ fontSize: '20px', color: '#DCE7F8', lineHeight: '1.55', marginTop: '10px', display: 'block' }}>智能作为系统演化的涌现属性显现。</Text>
        </Box>
      </Box>
      <Text style={{ fontSize: '15px', color: '#8B97A8', marginTop: '14px', textAlign: 'center' }}>术语统一：CS = Complexity Synchronization。页脚佐证：Mahmoodi, Kerick & West, Scientific Reports, 2024。</Text>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>介观尺度计算新范式 · 从SDSoW到iNEST</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>14 / 20</Text>
    </Box>
  </Box>
</Slide>
