<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>不是算力不够，而是范式太旧</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>引子 · 03</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', gap: '30px', padding: '30px 40px' }}>
      {/* 左锚点栏 */}
      <Box style={{ width: '380px', background: 'linear-gradient(160deg,#0E3F8C,#1E4FA8)', borderRadius: '12px', padding: '34px 30px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '120px', fontWeight: 'bold', color: '#FFC107', lineHeight: '1' }}>3</Text>
        <Text style={{ fontSize: '26px', fontWeight: 'bold', color: '#FFFFFF', marginTop: '6px' }}>堵墙同时逼近</Text>
        <Text style={{ fontSize: '20px', color: '#C9D8F0', marginTop: '18px', lineHeight: '1.6' }}>功耗墙 · 存储墙 · 互连墙，正把“堆算力”路线的红利吃干。</Text>
        <Box style={{ marginTop: '22px', background: 'rgba(255,255,255,0.10)', borderRadius: '8px', padding: '14px' }}>
          <Text style={{ fontSize: '18px', color: '#EAF1FB', lineHeight: '1.55' }}>主矛盾已从<Text style={{ fontWeight:'bold', color:'#FFE08A' }}>单点算力</Text>，转向<Text style={{ fontWeight:'bold', color:'#FFE08A' }}>系统架构</Text>。</Text>
        </Box>
      </Box>

      {/* 右三墙清单 */}
      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '18px', justifyContent: 'center' }}>
        {[
          { k: '功耗墙', e: 'Power Wall', d: 'AI 算力堆叠带来能耗陡增，单位算力的能效正逼近半导体物理下限，单纯扩大规模难以为继。' },
          { k: '存储墙', e: 'Memory Wall', d: '数据搬运成为时延与能耗的主要来源，大量算力“饿死”在访存等待中，算力利用率被严重拖累。' },
          { k: '互连墙', e: 'Interconnect Wall', d: '系统规模扩张受限于互连带宽、拓扑扩展与同步开销，横向堆核遭遇通信瓶颈。' },
        ].map((w, i) => (
          <Box key={i} style={{ background: '#F0F5FC', border: '1px solid #D6DCE5', borderLeft: '5px solid #1E4FA8', borderRadius: '10px', padding: '18px 22px' }}>
            <Text style={{ fontSize: '24px', fontWeight: 'bold', color: '#0E3F8C' }}>{w.k}<Text style={{ fontSize: '16px', color: '#8B97A8', marginLeft: '10px' }}>{w.e}</Text></Text>
            <Text style={{ fontSize: '21px', color: '#4A5568', lineHeight: '1.55', marginTop: '8px', display: 'block' }}>{w.d}</Text>
          </Box>
        ))}
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>页脚佐证：Horowitz, ISSCC, 2014；Hennessy & Patterson, CACM, 2019。</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>03 / 20</Text>
    </Box>
  </Box>
</Slide>
