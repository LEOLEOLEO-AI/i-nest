<Slide>
  <Box style={{ width: '1280px', height: '720px', background: 'linear-gradient(135deg, #0E3F8C 0%, #1E4FA8 60%, #3D7BD9 100%)', display: 'flex', flexDirection: 'column', padding: '56px 80px' }}>
    <Box style={{ textAlign: 'center' }}>
      <Text style={{ fontSize: '17px', color: '#9FB6E0', letterSpacing: '3px' }}>FROM SOFTWARE-DEFINED TO COMPLEXITY-DEFINED</Text>
      <Text style={{ fontSize: '52px', fontWeight: 'bold', color: '#FFFFFF', marginTop: '12px' }}>从软件定义系统，到复杂度定义智能</Text>
    </Box>

    {/* 七要素链 */}
    <Box style={{ display: 'flex', flexWrap: 'wrap', gap: '14px', justifyContent: 'center', marginTop: '44px' }}>
      {[
        'SDSoW 给资源', 'CST 给刻度', 'TCC 做匹配', 'SDDE 写演化', 'SDI 做调控', 'iNEST 推临界', 'iMESO 造智涌脑',
      ].map((s, i) => (
        <Box key={i} style={{ background: 'rgba(255,255,255,0.12)', border: '1px solid rgba(255,255,255,0.35)', borderRadius: '24px', padding: '16px 24px' }}>
          <Text style={{ fontSize: '22px', fontWeight: 'bold', color: '#FFFFFF' }}>{s}</Text>
        </Box>
      ))}
    </Box>

    {/* 院士收尾金句 */}
    <Box style={{ marginTop: 'auto', alignSelf: 'center', background: 'rgba(255,255,255,0.12)', borderLeft: '4px solid #FFC107', borderRadius: '8px', padding: '20px 30px', maxWidth: '1000px' }}>
      <Text style={{ fontSize: '26px', fontWeight: 'bold', color: '#FFE08A', lineHeight: '1.6', textAlign: 'center' }}>
        先让系统复杂度匹配环境，再让复杂度在临界演化中同步放大，最终让介观物理网络自己长出智能。
      </Text>
      <Text style={{ fontSize: '18px', color: '#DCE7F8', textAlign: 'center', marginTop: '12px' }}>—— 邬江兴 院士</Text>
    </Box>
  </Box>
</Slide>
