<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>iMESO 介观物理智能平台</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>平台与路线 · 18</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', gap: '32px', padding: '30px 40px' }}>
      {/* 左：五层闭环 */}
      <Box style={{ width: '600px', background: '#F0F5FC', border: '1px solid #D6DCE5', borderRadius: '12px', padding: '24px 28px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '19px', fontWeight: 'bold', color: '#0E3F8C', textAlign: 'center', marginBottom: '12px' }}>材料·器件·拓扑·动力学·环境 闭环一体化</Text>
        {[
          { t: '材料', d: '状态记忆', c: '#E8EFF8' },
          { t: '器件', d: '非线性载荷', c: '#D6E4F7' },
          { t: '拓扑', d: '协同关系', c: '#BBD2F2' },
          { t: '动力学', d: '临界演化', c: '#8FB6EC' },
          { t: '环境', d: '选择智能行为', c: '#0E3F8C' },
        ].map((x, i) => (
          <Box key={i}>
            <Box style={{ display: 'flex', alignItems: 'center', gap: '14px', background: x.c, borderRadius: '10px', padding: '13px 18px' }}>
              <Text style={{ fontSize: '22px', fontWeight: 'bold', color: x.c === '#0E3F8C' ? '#FFFFFF' : '#0E3F8C', width: '90px' }}>{x.t}</Text>
              <Text style={{ fontSize: '20px', color: x.c === '#0E3F8C' ? '#EAF1FB' : '#1A2230' }}>{x.d}</Text>
            </Box>
            {i < 4 && <Text style={{ fontSize: '22px', color: '#1E4FA8', textAlign: 'center', display: 'block' }}>↑ 反馈闭环 ↓</Text>}
          </Box>
        ))}
      </Box>

      {/* 右正文 */}
      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '26px', fontWeight: 'bold', color: '#1E4FA8', lineHeight: '1.5' }}>让智能涌现走向工程验证</Text>
        <Box style={{ height: '2px', background: '#D6DCE5', margin: '14px 0 16px' }} />
        <Text style={{ fontSize: '22px', color: '#1A2230', lineHeight: '1.65' }}>
          iMESO 作为<Text style={{ fontWeight: 'bold', color: '#0E3F8C' }}>晶圆 / 晶矩 / 面板级</Text>介观物理载体，把材料、器件、拓扑、动力学、环境闭环集成于同一平台，使前述理论可被工程验证。
        </Text>
        <Box style={{ marginTop: '18px', background: '#E8EFF8', borderLeft: '4px solid #1E4FA8', borderRadius: '6px', padding: '16px 20px' }}>
          <Text style={{ fontSize: '20px', color: '#0E3F8C', lineHeight: '1.6' }}>材料提供状态记忆，拓扑组织协同关系，临界放大有效响应，环境选择智能行为。</Text>
        </Box>
        <Text style={{ fontSize: '15px', color: '#8B97A8', marginTop: '14px' }}>页脚佐证：Strukov et al., 2008；Marković et al., 2020；Sebastian et al., Nat Nano, 2020；Schuman et al., Nat Comput Sci, 2022。</Text>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>介观尺度计算新范式 · 从SDSoW到iNEST</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>18 / 20</Text>
    </Box>
  </Box>
</Slide>
