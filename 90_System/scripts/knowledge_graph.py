# -*- coding: utf-8 -*-
\"\"\"
知识图谱模块 - KnowledgeGraph
使用 Neo4j 存储知识图谱，构建双向标签系统
\"\"\"

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Tuple
from collections import defaultdict

logger = logging.getLogger('knowledge_graph')


class KnowledgeGraph:
    def __init__(self, config):
        self.config = config
        self.base_dir = Path(__file__).parent.parent
        self.graph_dir = self.base_dir / 'knowledge_graph' / 'neo4j_data'
        self.graph_dir.mkdir(parents=True, exist_ok=True)
        self.nodes = defaultdict(list)
        self.edges = []
        self.tag_index = defaultdict(list)

    def update(self):
        logger.info('更新知识图谱...')
        self._load_existing_graph()
        self._scan_new_papers()
        self._build_bidirectional_tags()
        self._save_graph()
        logger.info(f'知识图谱更新完成: {len(self.nodes)} 个节点, {len(self.edges)} 条边')

    def _load_existing_graph(self):
        graph_file = self.graph_dir / 'graph.json'
        if graph_file.exists():
            with open(graph_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.nodes = defaultdict(list, data.get('nodes', {}))
                self.edges = data.get('edges', [])

    def _scan_new_papers(self):
        papers_dir = self.base_dir / 'papers'
        if not papers_dir.exists():
            return

        for direction in ['TCC', 'iNEST']:
            dir_path = papers_dir / direction
            if not dir_path.exists():
                continue
            for md_file in dir_path.glob('*.md'):
                if 'index.json' in str(md_file):
                    continue
                self._process_paper_file(md_file, direction)

    def _process_paper_file(self, md_file: Path, direction: str):
        content = md_file.read_text(encoding='utf-8')
        frontmatter = {}
        in_frontmatter = False

        for line in content.split('\n'):
            if line.startswith('---'):
                in_frontmatter = not in_frontmatter
                continue
            if in_frontmatter and ':' in line:
                key, val = line.split(':', 1)
                frontmatter[key.strip()] = val.strip()

        title = frontmatter.get('title', md_file.stem)
        node_id = f'paper_{title[:30].replace(" ", "_")}'

        if node_id not in self.nodes:
            self.nodes[node_id].append({
                'type': 'paper',
                'title': title,
                'direction': direction,
                'source_file': str(md_file),
                'date': datetime.now().isoformat(),
            })

    def _build_bidirectional_tags(self):
        tag_system = self.config['knowledge_graph']['tag_system']
        for node_id, node_list in self.nodes.items():
            for node in node_list:
                direction = node.get('direction', '')
                if direction:
                    self.tag_index[f'direction:{direction}'].append(node_id)
                self.tag_index[f'category:paper'].append(node_id)
                self.tag_index[f'status:new'].append(node_id)

    def _save_graph(self):
        graph_data = {
            'nodes': {k: v for k, v in self.nodes.items()},
            'edges': self.edges,
            'tag_index': {k: v for k, v in self.tag_index.items()},
            'last_updated': datetime.now().isoformat(),
        }
        graph_file = self.graph_dir / 'graph.json'
        with open(graph_file, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)

        # 导出为 Cypher 脚本（Neo4j 导入用）
        self._export_cypher(graph_data)

    def _export_cypher(self, graph_data):
        lines = ['// Neo4j Cypher import script', f'// Generated: {datetime.now().isoformat()}', '']

        # Create nodes
        for node_id, node_list in graph_data['nodes'].items():
            for node in node_list:
                node_type = node.get('type', 'unknown')
                props = ', '.join(f'{k}: \'{v}\'' for k, v in node.items() if k != 'type')
                lines.append(f'CREATE (n:{node_type} {{id: \'{node_id}\', {props}}});')

        # Create edges
        for edge in graph_data['edges']:
            lines.append(f\"\"\"MATCH (a {{id: '{edge['source']}'}}), (b {{id: '{edge['target']}'}})
CREATE (a)-[:{edge['type']}]->(b);
\"\"\")

        cypher_file = self.graph_dir / 'import.cypher'
        cypher_file.write_text('\n'.join(lines), encoding='utf-8')

    def get_related_nodes(self, node_id: str, depth: int = 2) -> Dict[str, List]:
        result = {'nodes': [], 'edges': [], 'depth': 0}
        visited = set()
        self._traverse(node_id, depth, visited, result)
        return result

    def _traverse(self, node_id: str, depth: int, visited: set, result: dict):
        if depth <= 0 or node_id in visited:
            return
        visited.add(node_id)
        result['nodes'].append(node_id)

        for edge in self.edges:
            if edge['source'] == node_id and edge['target'] not in visited:
                result['edges'].append(edge)
                self._traverse(edge['target'], depth - 1, visited, result)
            elif edge['target'] == node_id and edge['source'] not in visited:
                result['edges'].append(edge)
                self._traverse(edge['source'], depth - 1, visited, result)

    def export_tag_cloud(self, output_dir: Optional[Path] = None) -> Dict[str, int]:
        tag_counts = defaultdict(int)
        for tag, nodes in self.tag_index.items():
            tag_counts[tag] = len(set(nodes))

        if output_dir:
            (output_dir / 'tag_cloud.json').write_text(
                json.dumps(dict(tag_counts), ensure_ascii=False, indent=2), encoding='utf-8'
            )

        return dict(tag_counts)
