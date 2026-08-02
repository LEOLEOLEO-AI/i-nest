<Slide>
  <Box style={{ width: '1280px', height: '720px', background: '#FFFFFF', display: 'flex', flexDirection: 'column' }}>
    <Box style={{ height: '80px', background: '#0E3F8C', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px' }}>
      <Text style={{ fontSize: '32px', fontWeight: 'bold', color: '#FFFFFF' }}>路径成算：Route ≈ Transform</Text>
      <Text style={{ fontSize: '15px', color: '#C9D8F0' }}>度量与匹配 · 13</Text>
    </Box>

    <Box style={{ flex: 1, display: 'flex', gap: '32px', padding: '30px 40px' }}>
      <Box style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '26px', fontWeight: 'bold', color: '#1E4FA8', lineHeight: '1.5' }}>数据走过什么拓扑，就经历什么变换</Text>
        <Box style={{ height: '2px', background: '#D6DCE5', margin: '14px 0 16px' }} />
        <Text style={{ fontSize: '22px', color: '#1A2230', lineHeight: '1.65' }}>
          在可重构拓扑中，路径上的<Text style={{ fontWeight: 'bold', color: '#0E3F8C' }}>边权、时延、节点状态、非线性器件与记忆效应</Text>共同构成一个复合算子：数据所经历的变换，等价于它所走过的拓扑。
        </Text>
        <Box style={{ background: '#FFF6E6', borderLeft: '4px solid #FFC107', borderRadius: '6px', padding: '14px 18px', marginTop: '20px' }}>
          <Text style={{ fontSize: '18px', color: '#8A6D2B' }}>严谨口径：Route ≈ Transform 不是无条件等号，而是拓扑可编译条件下的近似等价。</Text>
        </Box>
        <Text style={{ fontSize: '15px', color: '#8B97A8', marginTop: '14px' }}>页脚佐证：Maass et al., Neural Computation, 2002；Jaeger & Haas, Science, 2004。</Text>
      </Box>

      {/* 右：复合算子图 */}
      <Box style={{ width: '500px', background: '#F0F5FC', border: '1px solid #D6DCE5', borderRadius: '12px', padding: '26px 28px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Text style={{ fontSize: '18px', fontWeight: 'bold', color: '#0E3F8C', textAlign: 'center', marginBottom: '18px' }}>路径即复合变换算子</Text>
        <Box style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', flexWrap: 'wrap' }}>
          {['φ_{e_1}', 'φ_{e_2}', '\\cdots', 'φ_{e_k}'].map((s, i) => (
            <Box key={i} style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Box style={{ background: '#FFFFFF', border: '1px solid #3D7BD9', borderRadius: '8px', padding: '14px 16px' }}>
                <Math latex={s} width={70} color="#0E3F8C" />
              </Box>
              {i < 3 && <Text style={{ fontSize: '26px', color: '#1E4FA8', fontWeight: 'bold' }}>∘</Text>}
            </Box>
          ))}
        </Box>
        <Box style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginTop: '20px' }}>
          <Text style={{ fontSize: '24px', color: '#1E4FA8', fontWeight: 'bold' }}>=</Text>
          <Box style={{ background: '#0E3F8C', borderRadius: '8px', padding: '14px 22px' }}>
            <Math latex="\mathcal{T}_{\rho}" width={90} color="#FFFFFF" />
          </Box>
        </Box>
      </Box>
    </Box>

    <Box style={{ height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '40px', paddingRight: '40px', borderTop: '1px solid #E5E7EB' }}>
      <Text style={{ fontSize: '14px', color: '#8B97A8' }}>介观尺度计算新范式 · 从SDSoW到iNEST</Text>
      <Text style={{ fontSize: '14px', color: '#1E4FA8', fontWeight: 'bold' }}>13 / 20</Text>
    </Box>
  </Box>
</Slide>
