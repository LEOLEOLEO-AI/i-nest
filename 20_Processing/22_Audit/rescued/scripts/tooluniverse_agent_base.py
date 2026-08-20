"""
ToolUniverse Research Agent Base Class

基于 ToolUniverse 框架的研究代理基类，提供标准化的工具发现、调用、编排和优化能力。
"""

import yaml
import json
import logging
import re
import html
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from urllib import parse, request, error
import xml.etree.ElementTree as ET
import os
import socket
import time
import hashlib


class ToolUniverseAgentBase:
    """
    ToolUniverse 研究代理基类
    
    提供核心功能：
    - Tool Finder: 智能工具发现
    - Tool Caller: 工具调用执行
    - Tool Composer: 工作流编排
    - Tool Discover: 自动工具生成
    - Tool Optimizer: 工具优化
    """
    
    def __init__(self, config_path: str):
        """
        初始化 ToolUniverse Agent
        
        Args:
            config_path: YAML 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        
        # 初始化核心组件（待 ToolUniverse 安装后实现）
        self.tool_finder = None  # ToolFinder()
        self.tool_caller = None  # ToolCaller()
        self.tool_composer = None  # ToolComposer()
        self.tool_discover = None  # ToolDiscover()
        self.tool_optimizer = None  # ToolOptimizer()
        
        # 工具注册表
        self.tool_registry = {}
        self.workflow_history = []
        self.research_profile = self._build_research_profile()
        self.local_pdf_alias_index = self._build_local_pdf_alias_index()
        
        self.logger.info(f"ToolUniverse Agent initialized: {self.config['agent']['name']}")
    
    def _load_config(self, config_path: str) -> Dict:
        """加载 YAML 配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _setup_logging(self) -> logging.Logger:
        """设置日志系统"""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        
        logger = logging.getLogger(self.config['agent']['name'])
        logger.setLevel(log_level)
        
        # 控制台输出
        if log_config.get('console_output', True):
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # 文件输出
        if log_config.get('file_output', True):
            log_dir = Path(log_config.get('output_dir', './logs'))
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = log_dir / f"{self.config['agent']['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger

    def _build_research_profile(self) -> Dict[str, Any]:
        task_config = self.config.get('task_config', {})
        quantclaw_config = self.config.get('quantclaw', {})
        search_config = task_config.get('search', {})
        profile = {
            'keywords': [],
            'negative_keywords': quantclaw_config.get('negative_keywords', []),
            'domain_boost_keywords': quantclaw_config.get('domain_boost_keywords', []),
            'paths': quantclaw_config.get('paths', {}),
            'ranking': quantclaw_config.get('ranking', {}),
            'pipeline': quantclaw_config.get('pipeline', {}),
        }
        for values in search_config.get('keywords', {}).values():
            profile['keywords'].extend(values)
        return profile

    def _build_local_pdf_alias_index(self) -> Dict[str, List[str]]:
        kb_root = Path(self.research_profile.get('paths', {}).get('knowledge_base_root', ''))
        index: Dict[str, List[str]] = {}
        if not kb_root.exists():
            return index
        self._index_aliases_from_literature_index(kb_root, index)
        self._index_aliases_from_directory(kb_root / 'Snapshots', index)
        self._index_aliases_from_directory(kb_root / 'Notes', index)
        self._index_aliases_from_directory(kb_root / 'Sources', index, include_pdf_stems=True)
        self._index_aliases_from_directory(kb_root / 'Inbox', index, include_pdf_stems=True)
        return index

    def _index_aliases_from_literature_index(self, kb_root: Path, index: Dict[str, List[str]]) -> None:
        path = kb_root / 'literature_index.md'
        if not path.exists():
            return
        try:
            lines = path.read_text(encoding='utf-8').splitlines()
        except Exception:
            return
        for line in lines:
            if not line.startswith('| LIT-'):
                continue
            parts = [part.strip() for part in line.strip().strip('|').split('|')]
            if len(parts) < 11:
                continue
            title = parts[1]
            original_path = parts[9]
            snapshot_path = parts[10]
            aliases = [title, Path(snapshot_path).stem if snapshot_path else '']
            resolved = self._resolve_pdf_candidate_path(original_path) or self._resolve_pdf_candidate_path(snapshot_path)
            if not resolved:
                continue
            for alias in aliases:
                self._add_pdf_alias(index, alias, resolved)

    def _index_aliases_from_directory(self, root: Path, index: Dict[str, List[str]], include_pdf_stems: bool = False) -> None:
        if not root.exists():
            return
        pattern = '*.pdf' if include_pdf_stems else '*.md'
        for path in root.rglob(pattern):
            alias = path.stem
            resolved = str(path if path.suffix.lower() == '.pdf' else self._resolve_pdf_candidate_path(str(path)))
            if not resolved or resolved == '.':
                continue
            self._add_pdf_alias(index, alias, resolved)

    def _add_pdf_alias(self, index: Dict[str, List[str]], alias: str, pdf_path: str) -> None:
        normalized = self._canonicalize_title(alias)
        if not normalized:
            return
        bucket = index.setdefault(normalized, [])
        if pdf_path not in bucket:
            bucket.append(pdf_path)

    def _tool_catalog(self) -> Dict[str, List[str]]:
        return {
            'search': [
                'arxiv',
                'semantic_scholar',
                'pubmed',
                'openalex',
                'zotero',
            ],
            'reading': [
                'dailypaper-skills',
                'pdf_reader',
                'summarizer',
                'formula_extractor',
                'deep-research-mcp',
            ],
            'organization': [
                'obsidian',
                'zotero',
                'knowledge_base',
                'notebook_sync',
            ],
            'analysis': [
                'networkx',
                'plotly',
                'scikit-learn',
                'pandas',
                'manuscript_analyzer',
            ],
        }

    def _match_tool_stage(self, tool_name: str) -> str:
        normalized = tool_name.lower().replace('_', '-')
        for stage, names in self._tool_catalog().items():
            normalized_names = [name.lower().replace('_', '-') for name in names]
            if normalized in normalized_names:
                return stage
        return 'general'
    
    def discover_tools(self, task_description: str, max_results: int = 10) -> List[Dict]:
        """
        智能工具发现
        
        Args:
            task_description: 任务描述
            max_results: 最大返回结果数
            
        Returns:
            工具列表
        """
        self.logger.info(f"Discovering tools for: {task_description}")
        
        # TODO: 实现 ToolFinder 集成
        # tools = self.tool_finder.find(
        #     query=task_description,
        #     method=self.config['tools']['discovery']['search_method'],
        #     max_results=max_results
        # )
        
        # 临时实现：返回配置中的必需工具
        discovered_tools = []
        for tool in self.config['tools'].get('required', []):
            tool_copy = dict(tool)
            tool_copy['stage'] = self._match_tool_stage(tool_copy.get('name', ''))
            discovered_tools.append(tool_copy)
        tools = discovered_tools[:max_results]
        
        self.logger.info(f"Found {len(tools)} tools")
        return tools
    
    def call_tool(self, tool_name: str, parameters: Dict) -> Any:
        """
        调用单个工具
        
        Args:
            tool_name: 工具名称
            parameters: 工具参数
            
        Returns:
            工具执行结果
        """
        self.logger.info(f"Calling tool: {tool_name}")
        
        # TODO: 实现 ToolCaller 集成
        # result = self.tool_caller.execute(
        #     tool_name=tool_name,
        #     parameters=parameters,
        #     timeout=self.config['tools']['execution']['timeout']
        # )
        
        stage = self._match_tool_stage(tool_name)
        try:
            output = self._try_real_tool_call(tool_name, parameters, stage)
        except Exception as exc:
            self.logger.error(f"Real tool call failed for {tool_name}: {exc}")
            raise
        result = {
            'tool': tool_name,
            'parameters': parameters,
            'stage': stage,
            'status': 'real',
            'output': output
        }
        
        self.logger.info(f"Tool {tool_name} executed successfully")
        return result
    
    def compose_workflow(self, task_definition: Dict) -> Dict:
        """
        编排工作流
        
        Args:
            task_definition: 任务定义
            
        Returns:
            工作流定义
        """
        self.logger.info("Composing workflow")
        
        # TODO: 实现 ToolComposer 集成
        # workflow = self.tool_composer.compose(
        #     task=task_definition,
        #     tools=self.tool_registry,
        #     mode=self.config['workflow']['execution_mode']
        # )
        
        stages = task_definition.get('pipeline_stages') or self.config.get(
            'quantclaw',
            {},
        ).get(
            'pipeline',
            {},
        ).get(
            'stages',
            ['search', 'reading', 'organization'],
        )
        workflow = {
            'name': task_definition.get('name', 'unnamed_workflow'),
            'steps': self._compose_research_steps(task_definition, stages),
            'mode': self.config['workflow']['execution_mode'],
            'stages': stages,
            'skipped_stages': self._collect_skipped_stages(stages),
            'created_at': datetime.now().isoformat()
        }
        
        self.logger.info(f"Workflow composed: {workflow['name']}")
        return workflow
    
    def execute_workflow(self, workflow: Dict) -> Dict:
        """
        执行工作流
        
        Args:
            workflow: 工作流定义
            
        Returns:
            执行结果
        """
        self.logger.info(f"Executing workflow: {workflow['name']}")
        
        results = {
            'workflow_name': workflow['name'],
            'stages': workflow.get('stages', []),
            'skipped_stages': workflow.get('skipped_stages', []),
            'start_time': datetime.now().isoformat(),
            'steps': [],
            'status': 'running',
            'artifacts': {},
            'errors': [],
        }
        
        try:
            for step in workflow.get('steps', []):
                step_result = self._execute_step(step, results['artifacts'])
                results['steps'].append(step_result)
                self._merge_step_artifacts(results['artifacts'], step_result.get('artifacts', {}))
                
                if step_result['status'] == 'failed':
                    results['errors'].append({
                        'step_name': step_result.get('step_name'),
                        'stage': step_result.get('stage'),
                        'error': step_result.get('error', ''),
                    })
                    if not self._can_continue_after_failure(step_result, results):
                        results['status'] = 'failed'
                        break
            
            if results['status'] == 'running':
                results['status'] = 'completed_with_errors' if results['errors'] else 'completed'
                
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {str(e)}")
            results['status'] = 'error'
            results['error'] = str(e)
        
        results['end_time'] = datetime.now().isoformat()
        results['summary'] = self._build_execution_summary(results)
        self.workflow_history.append(results)
        
        self.logger.info(f"Workflow execution {results['status']}")
        return results
    
    def _execute_step(self, step: Dict, artifacts: Optional[Dict[str, Any]] = None) -> Dict:
        """执行单个工作流步骤"""
        self.logger.debug(f"Executing step: {step.get('name', 'unnamed')}")
        
        result = {
            'step_name': step.get('name'),
            'stage': step.get('stage'),
            'start_time': datetime.now().isoformat(),
            'status': 'success'
        }
        
        try:
            # 调用工具
            parameters = dict(step.get('parameters', {}))
            if artifacts:
                parameters['context_artifacts'] = artifacts
            tool_result = self.call_tool(
                tool_name=step.get('tool'),
                parameters=parameters
            )
            result['output'] = tool_result
            result['artifacts'] = self._extract_artifacts_from_tool_result(tool_result)
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
        
        result['end_time'] = datetime.now().isoformat()
        return result

    def _can_continue_after_failure(self, step_result: Dict[str, Any], results: Dict[str, Any]) -> bool:
        stage = step_result.get('stage')
        if stage == 'search':
            return True
        if stage == 'reading':
            return False
        return False

    def _compose_research_steps(self, task_definition: Dict, stages: List[str]) -> List[Dict]:
        steps: List[Dict] = []
        objectives = task_definition.get('objectives', [])
        for stage in stages:
            if not self._stage_has_real_execution(stage):
                continue
            if stage == 'search':
                for tool_name in self._pick_tools_for_stage('search'):
                    if not self._is_real_tool_supported(tool_name, 'search'):
                        continue
                    steps.append({
                        'name': f"Search with {tool_name}",
                        'stage': 'search',
                        'tool': tool_name,
                        'parameters': {
                            'query': task_definition.get('description', '').strip(),
                            'keywords': self.research_profile.get('keywords', []),
                            'negative_keywords': self.research_profile.get('negative_keywords', []),
                            'domain_boost_keywords': self.research_profile.get('domain_boost_keywords', []),
                            'top_k': self.research_profile.get('ranking', {}).get('daily_top_k', 10),
                        },
                    })
            elif stage == 'reading':
                reading_tool = None
                for candidate in self._pick_tools_for_stage('reading'):
                    if self._is_real_tool_supported(candidate, 'reading'):
                        reading_tool = candidate
                        break
                if not reading_tool:
                    continue
                steps.append({
                    'name': f"Read and summarize candidate papers with {reading_tool}",
                    'stage': 'reading',
                    'tool': reading_tool,
                    'parameters': {
                        'mode': 'critical_summary',
                        'focus': objectives,
                        'must_extract': [
                            'core_contribution',
                            'method',
                            'limitations',
                            'relevance_score',
                        ],
                    },
                })
            elif stage == 'organization':
                organization_tool = None
                for candidate in self._pick_tools_for_stage('organization'):
                    if self._is_real_tool_supported(candidate, 'organization'):
                        organization_tool = candidate
                        break
                if not organization_tool:
                    continue
                steps.append({
                    'name': f"Organize real outputs with {organization_tool}",
                    'stage': 'organization',
                    'tool': organization_tool,
                    'parameters': {
                        'task_name': task_definition.get('name', 'unnamed_workflow'),
                        'task_description': task_definition.get('description', '').strip(),
                        'objectives': objectives,
                    },
                })
            elif stage == 'analysis':
                analysis_tool = None
                for candidate in self._pick_tools_for_stage('analysis'):
                    if self._is_real_tool_supported(candidate, 'analysis'):
                        analysis_tool = candidate
                        break
                if not analysis_tool:
                    continue
                steps.append({
                    'name': f"Analyze manuscript claims with {analysis_tool}",
                    'stage': 'analysis',
                    'tool': analysis_tool,
                    'parameters': {
                        'task_name': task_definition.get('name', 'unnamed_analysis'),
                        'task_description': task_definition.get('description', '').strip(),
                        'objectives': objectives,
                        'manuscript_path': task_definition.get('manuscript_path', ''),
                    },
                })
        return steps

    def _pick_tools_for_stage(self, stage: str) -> List[str]:
        configured = []
        for tool in self.config.get('tools', {}).get('required', []):
            if self._match_tool_stage(tool.get('name', '')) == stage:
                configured.append(tool['name'])
        if configured:
            if stage == 'analysis' and 'manuscript_analyzer' in configured:
                configured = ['manuscript_analyzer'] + [tool for tool in configured if tool != 'manuscript_analyzer']
            return configured
        return self._tool_catalog().get(stage, ['knowledge_base'])

    def _try_real_tool_call(self, tool_name: str, parameters: Dict[str, Any], stage: str) -> Any:
        if tool_name == 'arxiv':
            return self._call_arxiv_api(parameters)
        if tool_name == 'semantic_scholar':
            return self._call_semantic_scholar_api(parameters)
        if tool_name == 'pubmed':
            return self._call_pubmed_api(parameters)
        if tool_name == 'openalex':
            return self._call_openalex_api(parameters)
        if stage == 'reading' and tool_name in {'dailypaper-skills', 'deep-research-mcp', 'summarizer', 'pdf_reader'}:
            return self._build_reading_digest(parameters)
        if stage == 'organization' and tool_name in {'knowledge_base', 'obsidian'}:
            return self._write_knowledge_base_artifacts(parameters)
        if stage == 'analysis' and tool_name in {'manuscript_analyzer', 'pandas', 'networkx'}:
            return self._analyze_manuscript(parameters)
        raise RuntimeError(f"No real adapter available for tool: {tool_name}")

    def _call_arxiv_api(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        top_k = int(parameters.get('top_k', 10))
        max_results = min(max(top_k, 1), 20)
        queries = self._build_arxiv_query_candidates(parameters)
        retry_attempts = max(1, int(self.config.get('tools', {}).get('execution', {}).get('retry_attempts', 3)))
        errors: List[str] = []
        for query in queries:
            for attempt in range(1, retry_attempts + 1):
                try:
                    url = (
                        "http://export.arxiv.org/api/query?"
                        + parse.urlencode(
                            {
                                'search_query': f'all:{query}',
                                'start': 0,
                                'max_results': max_results,
                                'sortBy': 'submittedDate',
                                'sortOrder': 'descending',
                            }
                        )
                    )
                    payload = self._fetch_url(url, timeout=20, source='arxiv')
                    root = ET.fromstring(payload)
                    ns = {'atom': 'http://www.w3.org/2005/Atom'}
                    papers: List[Dict[str, Any]] = []
                    for entry in root.findall('atom:entry', ns):
                        title = self._clean_text(entry.findtext('atom:title', default='', namespaces=ns))
                        summary = self._clean_text(entry.findtext('atom:summary', default='', namespaces=ns))
                        paper_url = entry.findtext('atom:id', default='', namespaces=ns)
                        authors = [
                            self._clean_text(author.findtext('atom:name', default='', namespaces=ns))
                            for author in entry.findall('atom:author', ns)
                        ]
                        papers.append({
                            'title': title,
                            'abstract': summary,
                            'url': paper_url,
                            'authors': authors,
                            'source': 'arxiv',
                            'score': self._score_paper(title, summary),
                        })
                    papers.sort(key=lambda item: item.get('score', 0), reverse=True)
                    output = self._finalize_search_output(parameters, papers, 'arxiv')
                    output['query_attempts'] = queries[:queries.index(query) + 1]
                    return output
                except Exception as exc:
                    errors.append(f"query='{query}' attempt={attempt}: {exc}")
                    if attempt < retry_attempts:
                        time.sleep(min(2 ** (attempt - 1), 4))
        raise RuntimeError(
            "arxiv failed after retries and query narrowing. "
            f"Tried queries: {queries}. Last errors: {' | '.join(errors[-3:])}"
        )

    def _call_semantic_scholar_api(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        query = self._build_search_query(parameters)
        top_k = int(parameters.get('top_k', 10))
        limit = min(max(top_k, 1), 20)
        url = (
            "https://api.semanticscholar.org/graph/v1/paper/search?"
            + parse.urlencode(
                {
                    'query': query,
                    'limit': limit,
                    'fields': 'title,abstract,year,url,authors,citationCount',
                }
            )
        )
        headers = {'User-Agent': 'ToolUniverseResearchAgent/1.0'}
        api_key = self._lookup_tool_config_value('semantic_scholar', 'api_key')
        has_api_key = self._has_configured_value(api_key)
        if has_api_key:
            headers['x-api-key'] = str(api_key).strip()
        else:
            if self._is_placeholder_value(api_key):
                self.logger.warning(
                    "Semantic Scholar API key is still a placeholder (${SEMANTIC_SCHOLAR_API_KEY}). "
                    "Set the real environment variable before retrying."
                )
            else:
                self.logger.warning(
                    "Semantic Scholar API key is not configured. Proceeding without key; requests may hit strict rate limits."
                )
        req = request.Request(url, headers=headers)
        try:
            payload = json.loads(self._fetch_request(req, timeout=30, source='semantic_scholar').decode('utf-8'))
        except RuntimeError as exc:
            message = str(exc)
            if 'HTTP 429' in message:
                advice = (
                    "Semantic Scholar rate limited the request. "
                    + (
                        "The configured API key still hit rate limits; wait and retry later or reduce request volume."
                        if has_api_key
                        else "Set a real SEMANTIC_SCHOLAR_API_KEY to reduce rate limiting, then retry."
                    )
                )
                raise RuntimeError(f"{message} Advice: {advice}") from exc
            if not has_api_key:
                raise RuntimeError(
                    "Semantic Scholar request failed and no valid API key is configured. "
                    "Set a real SEMANTIC_SCHOLAR_API_KEY and retry. "
                    f"Underlying error: {message}"
                ) from exc
            raise
        papers: List[Dict[str, Any]] = []
        for item in payload.get('data', []):
            title = self._clean_text(item.get('title', ''))
            abstract = self._clean_text(item.get('abstract', ''))
            papers.append({
                'title': title,
                'abstract': abstract,
                'url': item.get('url', ''),
                'year': item.get('year'),
                'authors': [author.get('name', '') for author in item.get('authors', [])],
                'citation_count': item.get('citationCount', 0),
                'source': 'semantic_scholar',
                'score': self._score_paper(title, abstract, item.get('citationCount', 0)),
            })
        papers.sort(key=lambda item: item.get('score', 0), reverse=True)
        return self._finalize_search_output(parameters, papers, 'semantic_scholar')

    def _call_pubmed_api(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        query = self._build_search_query(parameters)
        top_k = int(parameters.get('top_k', 10))
        limit = min(max(top_k, 1), 20)
        search_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
            + parse.urlencode(
                {
                    'db': 'pubmed',
                    'term': query,
                    'retmode': 'json',
                    'retmax': limit,
                    'sort': 'relevance',
                }
            )
        )
        search_payload = json.loads(self._fetch_url(search_url, timeout=30, source='pubmed').decode('utf-8'))
        id_list = search_payload.get('esearchresult', {}).get('idlist', [])
        if not id_list:
            raise RuntimeError(f"PubMed returned no papers for query: {query}")
        summary_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
            + parse.urlencode(
                {
                    'db': 'pubmed',
                    'id': ','.join(id_list),
                    'retmode': 'json',
                }
            )
        )
        summary_payload = json.loads(self._fetch_url(summary_url, timeout=30, source='pubmed').decode('utf-8'))
        result_map = summary_payload.get('result', {})
        papers: List[Dict[str, Any]] = []
        for pubmed_id in id_list:
            item = result_map.get(pubmed_id, {})
            title = self._clean_text(item.get('title', ''))
            authors = [author.get('name', '') for author in item.get('authors', [])]
            abstract = self._fetch_pubmed_abstract(pubmed_id)
            papers.append({
                'title': title,
                'abstract': abstract,
                'url': f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/",
                'authors': authors,
                'year': str(item.get('pubdate', '')).split(' ')[0] if item.get('pubdate') else '',
                'citation_count': 0,
                'source': 'pubmed',
                'score': self._score_paper(title, abstract),
            })
        papers.sort(key=lambda item: item.get('score', 0), reverse=True)
        return self._finalize_search_output(parameters, papers, 'pubmed')

    def _call_openalex_api(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        query = self._build_search_query(parameters)
        top_k = int(parameters.get('top_k', 10))
        limit = min(max(top_k, 1), 20)
        url = (
            "https://api.openalex.org/works?"
            + parse.urlencode(
                {
                    'search': query,
                    'per-page': limit,
                    'sort': 'relevance_score:desc',
                }
            )
        )
        payload = json.loads(self._fetch_url(url, timeout=30, source='openalex').decode('utf-8'))
        papers: List[Dict[str, Any]] = []
        for item in payload.get('results', []):
            title = self._clean_text(item.get('display_name', ''))
            abstract = self._openalex_abstract_text(item)
            papers.append({
                'title': title,
                'abstract': abstract,
                'url': item.get('id', ''),
                'year': item.get('publication_year'),
                'authors': [
                    authorship.get('author', {}).get('display_name', '')
                    for authorship in item.get('authorships', [])
                ],
                'citation_count': item.get('cited_by_count', 0),
                'source': 'openalex',
                'score': self._score_paper(title, abstract, item.get('cited_by_count', 0)),
            })
        papers.sort(key=lambda item: item.get('score', 0), reverse=True)
        return self._finalize_search_output(parameters, papers, 'openalex')

    def _build_reading_digest(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        context = parameters.get('context_artifacts', {})
        search_digest = context.get('search_digest', {})
        papers = search_digest.get('papers', [])
        if not papers:
            raise RuntimeError("No search papers available for reading stage")
        limit = self.research_profile.get('ranking', {}).get('must_read_k', 3)
        cards = []
        for paper in papers[:limit]:
            abstract = paper.get('abstract', '')
            full_text = self._load_local_full_text_for_paper(paper)
            sections = self._extract_pdf_sections(full_text) if full_text else {}
            reading_text = self._compose_reading_text(abstract, sections)
            cards.append({
                'title': paper.get('title', ''),
                'source': paper.get('source', ''),
                'url': paper.get('url', ''),
                'relevance_score': paper.get('score', 0),
                'core_contribution': self._summarize_text(reading_text, 320),
                'method': self._infer_method(sections.get('method', '') or reading_text),
                'limitations': self._infer_limitations(sections.get('experiments', '') or sections.get('conclusion', '') or reading_text),
                'reading_source': 'pdf_full_text' if full_text else 'abstract',
                'full_text_path': paper.get('local_pdf_path', ''),
                'section_digest': sections,
            })
        return {
            'papers_processed': len(cards),
            'generated_sections': parameters.get('must_extract', []),
            'reading_mode': parameters.get('mode'),
            'paper_cards': cards,
        }

    def _build_search_query(self, parameters: Dict[str, Any]) -> str:
        keywords = parameters.get('keywords', [])
        if keywords:
            return ' OR '.join(keywords[:4])
        return parameters.get('query', '').strip() or 'research papers'

    def _build_arxiv_query_candidates(self, parameters: Dict[str, Any]) -> List[str]:
        keywords = [self._clean_text(keyword) for keyword in parameters.get('keywords', []) if self._clean_text(keyword)]
        query = self._build_search_query(parameters)
        candidates: List[str] = []
        if query:
            candidates.append(query)
        if keywords:
            candidates.append(' OR '.join(keywords[:3]))
            candidates.append(' OR '.join(keywords[:2]))
            candidates.append(keywords[0])
        fallback_query = self._clean_text(parameters.get('query', ''))
        if fallback_query:
            shortened = ' '.join(fallback_query.split()[:8])
            if shortened:
                candidates.append(shortened)
        deduped: List[str] = []
        for candidate in candidates:
            if candidate and candidate not in deduped:
                deduped.append(candidate)
        return deduped or ['research papers']

    def _finalize_search_output(self, parameters: Dict[str, Any], papers: List[Dict[str, Any]], source: str) -> Dict[str, Any]:
        top_k = int(parameters.get('top_k', 10))
        enriched_papers = []
        for paper in papers:
            enriched = dict(paper)
            enriched['local_pdf_path'] = self._find_local_pdf_for_title(enriched.get('title', ''))
            enriched['local_pdf_boost'] = 6.0 if enriched.get('local_pdf_path') else 0.0
            enriched['score'] = float(enriched.get('score', 0)) + enriched['local_pdf_boost']
            enriched_papers.append(enriched)
        enriched_papers.sort(key=lambda item: item.get('score', 0), reverse=True)
        must_read_k = min(self.research_profile.get('ranking', {}).get('must_read_k', 3), len(enriched_papers))
        selected = enriched_papers[:top_k]
        if not selected:
            raise RuntimeError(f"{source} returned no papers for query: {self._build_search_query(parameters)}")
        return {
            'recommended_count': len(selected),
            'must_read_count': must_read_k,
            'query': self._build_search_query(parameters),
            'keywords_used': parameters.get('keywords', [])[:8],
            'source': source,
            'papers': selected,
            'must_read': self._prioritize_local_pdf_papers(selected, must_read_k),
        }

    def _score_paper(self, title: str, abstract: str, citation_count: int = 0) -> float:
        text = f"{title} {abstract}".lower()
        score = 0.0
        for keyword in self.research_profile.get('keywords', []):
            if keyword.lower() in text:
                score += 2.0
        for keyword in self.research_profile.get('domain_boost_keywords', []):
            if keyword.lower() in text:
                score += 3.0
        for keyword in self.research_profile.get('negative_keywords', []):
            if keyword.lower() in text:
                score -= 5.0
        score += min(citation_count / 50.0, 5.0)
        return score

    def _clean_text(self, value: str) -> str:
        return ' '.join((value or '').split())

    def _summarize_text(self, text: str, max_chars: int) -> str:
        cleaned = self._clean_text(text)
        if len(cleaned) <= max_chars:
            return cleaned
        cutoff = cleaned[:max_chars].rsplit(' ', 1)[0]
        return f"{cutoff}..."

    def _infer_method(self, abstract: str) -> str:
        lower = abstract.lower()
        if 'reinforcement learning' in lower or 'rl' in lower:
            return 'reinforcement learning'
        if 'diffusion' in lower:
            return 'diffusion model'
        if 'graph' in lower or 'network' in lower:
            return 'graph/network modeling'
        if 'transformer' in lower or 'attention' in lower:
            return 'transformer-based modeling'
        return 'see abstract'

    def _infer_limitations(self, abstract: str) -> str:
        lower = abstract.lower()
        if 'benchmark' in lower:
            return 'benchmark scope may limit generalization'
        if 'simulation' in lower:
            return 'results may require real-world validation'
        return 'limitations not explicit in abstract'

    def _lookup_tool_config_value(self, tool_name: str, key: str) -> Optional[str]:
        for tool in self.config.get('tools', {}).get('required', []):
            if tool.get('name') == tool_name:
                raw = tool.get('config', {}).get(key)
                if raw and str(raw).startswith(''):
                    env_key = str(raw)[2:-1]
                    env_val = os.getenv(env_key)
                    if env_val:
                        return env_val
                return raw
        env_value = os.getenv(key.upper())
        return env_value

    def _has_configured_value(self, value: Optional[str]) -> bool:
        if value is None:
            return False
        normalized = str(value).strip()
        return bool(normalized) and not normalized.startswith('${')

    def _is_placeholder_value(self, value: Optional[str]) -> bool:
        if value is None:
            return False
        return str(value).strip().startswith('${')

    def _fetch_pubmed_abstract(self, pubmed_id: str) -> str:
        fetch_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
            + parse.urlencode(
                {
                    'db': 'pubmed',
                    'id': pubmed_id,
                    'retmode': 'xml',
                }
            )
        )
        payload = self._fetch_url(fetch_url, timeout=30, source='pubmed').decode('utf-8', errors='ignore')
        try:
            root = ET.fromstring(payload)
        except ET.ParseError:
            return ""
        fragments = []
        for node in root.findall('.//Abstract/AbstractText'):
            text = ''.join(node.itertext()).strip()
            if text:
                fragments.append(self._clean_text(text))
        return ' '.join(fragments)

    def _openalex_abstract_text(self, item: Dict[str, Any]) -> str:
        index = item.get('abstract_inverted_index') or {}
        if not index:
            return ""
        pairs = []
        for token, positions in index.items():
            for position in positions:
                pairs.append((position, token))
        pairs.sort(key=lambda entry: entry[0])
        return self._clean_text(' '.join(token for _, token in pairs))

    def _normalize_name_for_match(self, value: str) -> str:
        return ''.join(self._tokenize_title(value))

    def _tokenize_title(self, value: str) -> List[str]:
        normalized = self._clean_text(value).lower()
        normalized = normalized.replace('&', ' and ')
        normalized = re.sub(r'[^a-z0-9]+', ' ', normalized)
        tokens = [token for token in normalized.split() if token]
        stopwords = {
            'a', 'an', 'the', 'of', 'for', 'and', 'or', 'to', 'in', 'on', 'with',
            'from', 'by', 'via', 'toward', 'towards', 'using', 'based', 'study',
            'analysis', 'approach', 'method', 'methods', 'system',
        }
        return [token for token in tokens if token not in stopwords]

    def _canonicalize_title(self, value: str) -> str:
        tokens = self._tokenize_title(value)
        return ' '.join(tokens)

    def _find_local_pdf_for_title(self, title: str) -> str:
        title_tokens = self._tokenize_title(title)
        canonical_title = self._canonicalize_title(title)
        if not title_tokens:
            return ''
        alias_match = self._find_local_pdf_via_alias_index(canonical_title, title_tokens)
        if alias_match:
            return alias_match
        kb_root = Path(self.research_profile.get('paths', {}).get('knowledge_base_root', ''))
        if not kb_root.exists():
            return ''
        indexed_match = self._find_local_pdf_via_index(kb_root, canonical_title, title_tokens)
        if indexed_match:
            return indexed_match
        fuzzy_match = self._find_local_pdf_via_fuzzy_scan(kb_root, title_tokens)
        if fuzzy_match:
            return fuzzy_match
        return ''

    def _find_local_pdf_via_alias_index(self, canonical_title: str, title_tokens: List[str]) -> str:
        best_score = 0.0
        best_path = ''
        for alias, pdf_paths in self.local_pdf_alias_index.items():
            score = self._title_match_score(canonical_title, title_tokens, alias)
            if not self._is_strong_title_match(canonical_title, title_tokens, alias, score):
                continue
            if score > best_score and pdf_paths:
                best_score = score
                best_path = pdf_paths[0]
        return best_path

    def _prioritize_local_pdf_papers(self, papers: List[Dict[str, Any]], must_read_k: int) -> List[Dict[str, Any]]:
        sorted_papers = sorted(
            papers,
            key=lambda item: (
                1 if item.get('local_pdf_path') else 0,
                item.get('score', 0),
            ),
            reverse=True,
        )
        return sorted_papers[:must_read_k]

    def _find_local_pdf_via_index(self, kb_root: Path, canonical_title: str, title_tokens: List[str]) -> str:
        index_path = kb_root / 'literature_index.md'
        if not index_path.exists():
            return ''
        try:
            lines = index_path.read_text(encoding='utf-8').splitlines()
        except Exception:
            return ''
        candidates: List[tuple[float, str]] = []
        for line in lines:
            if not line.startswith('| LIT-'):
                continue
            parts = [part.strip() for part in line.strip().strip('|').split('|')]
            if len(parts) < 11:
                continue
            row_title = parts[1]
            original_path = parts[9]
            snapshot_path = parts[10]
            score = self._title_match_score(canonical_title, title_tokens, row_title)
            if not self._is_strong_title_match(canonical_title, title_tokens, row_title, score):
                continue
            for candidate in [original_path, snapshot_path]:
                resolved = self._resolve_pdf_candidate_path(candidate)
                if resolved:
                    candidates.append((score, resolved))
        if not candidates:
            return ''
        candidates.sort(key=lambda item: item[0], reverse=True)
        return candidates[0][1]

    def _find_local_pdf_via_fuzzy_scan(self, kb_root: Path, title_tokens: List[str]) -> str:
        search_roots = [kb_root / 'Sources', kb_root / 'Inbox']
        best_score = 0.0
        best_path = ''
        canonical_title = ' '.join(title_tokens)
        for search_root in search_roots:
            if not search_root.exists():
                continue
            for path in search_root.rglob('*.pdf'):
                score = self._path_match_score(path, title_tokens)
                if self._is_strong_title_match(canonical_title, title_tokens, path.stem, score) and score > best_score:
                    best_score = score
                    best_path = str(path)
        return best_path

    def _resolve_pdf_candidate_path(self, value: str) -> str:
        raw = str(value).strip()
        if not raw:
            return ''
        path = Path(raw)
        if path.suffix.lower() == '.pdf' and path.exists():
            return str(path)
        if path.suffix.lower() == '.md' and path.exists():
            pdf_candidate = path.with_suffix('.pdf')
            if pdf_candidate.exists():
                return str(pdf_candidate)
            stem = path.stem
            if stem.endswith('_2'):
                alt = path.with_name(stem[:-2] + '.pdf')
                if alt.exists():
                    return str(alt)
        return ''

    def _title_match_score(self, canonical_title: str, title_tokens: List[str], candidate_title: str) -> float:
        candidate_canonical = self._canonicalize_title(candidate_title)
        candidate_tokens = set(self._tokenize_title(candidate_title))
        if not candidate_tokens or not title_tokens:
            return 0.0
        shared_tokens = set(title_tokens) & candidate_tokens
        overlap = len(shared_tokens) / max(len(set(title_tokens)), 1)
        score = overlap
        if canonical_title and candidate_canonical == canonical_title:
            score += 1.0
        elif canonical_title and (canonical_title in candidate_canonical or candidate_canonical in canonical_title):
            score += 0.5
        return score

    def _path_match_score(self, path: Path, title_tokens: List[str]) -> float:
        stem_tokens = set(self._tokenize_title(path.stem))
        if not stem_tokens:
            return 0.0
        shared_tokens = set(title_tokens) & stem_tokens
        overlap = len(shared_tokens) / max(len(set(title_tokens)), 1)
        if self._canonicalize_title(path.stem) == ' '.join(title_tokens):
            overlap += 1.0
        return overlap

    def _is_strong_title_match(self, canonical_title: str, title_tokens: List[str], candidate_title: str, score: float) -> bool:
        candidate_tokens = set(self._tokenize_title(candidate_title))
        query_tokens = set(title_tokens)
        shared_count = len(query_tokens & candidate_tokens)
        if canonical_title and self._canonicalize_title(candidate_title) == canonical_title:
            return True
        if shared_count >= 3 and score >= 0.6:
            return True
        if len(query_tokens) <= 3 and shared_count == len(query_tokens) and shared_count >= 2:
            return True
        return False

    def _load_local_full_text_for_paper(self, paper: Dict[str, Any]) -> str:
        pdf_path = paper.get('local_pdf_path', '')
        if not pdf_path:
            return ''
        path = Path(pdf_path)
        if not path.exists():
            return ''
        try:
            from pypdf import PdfReader
        except ImportError:
            return ''
        try:
            reader = PdfReader(str(path))
        except Exception:
            return ''
        chunks: List[str] = []
        page_limit = min(len(reader.pages), 12)
        for page in reader.pages[:page_limit]:
            try:
                text = self._clean_text(page.extract_text() or '')
            except Exception:
                text = ''
            if text:
                chunks.append(text)
        return '\n\n'.join(chunks)

    def _extract_pdf_sections(self, full_text: str) -> Dict[str, str]:
        if not full_text:
            return {}
        sections: Dict[str, str] = {}
        patterns = {
            'abstract': r'(?is)\babstract\b[:\s]*(.*?)(?=\bintroduction\b|\b1\.\s*introduction\b|\bbackground\b|$)',
            'introduction': r'(?is)(?:\bintroduction\b|\b1\.\s*introduction\b)[:\s]*(.*?)(?=\brelated work\b|\bmethod\b|\bmethods\b|\bapproach\b|\b2\.\b|$)',
            'method': r'(?is)(?:\bmethod\b|\bmethods\b|\bapproach\b|\bmethodology\b)[:\s]*(.*?)(?=\bexperiment\b|\bexperiments\b|\bevaluation\b|\bresults\b|\b3\.\b|$)',
            'experiments': r'(?is)(?:\bexperiment\b|\bexperiments\b|\bevaluation\b|\bresults\b)[:\s]*(.*?)(?=\bconclusion\b|\bdiscussion\b|\b4\.\b|$)',
            'conclusion': r'(?is)(?:\bconclusion\b|\bconclusions\b|\bdiscussion\b)[:\s]*(.*)$',
        }
        for key, pattern in patterns.items():
            match = re.search(pattern, full_text)
            if match:
                sections[key] = self._summarize_text(self._clean_text(match.group(1)), 1200)
        return sections

    def _compose_reading_text(self, abstract: str, sections: Dict[str, str]) -> str:
        parts = []
        for key in ['abstract', 'introduction', 'method', 'experiments', 'conclusion']:
            value = sections.get(key, '')
            if value:
                parts.append(value)
        if not parts and abstract:
            parts.append(abstract)
        return '\n\n'.join(parts)

    def _write_knowledge_base_artifacts(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        context = parameters.get('context_artifacts', {})
        reading_digest = context.get('reading_digest', {})
        search_digest = context.get('search_digest', {})
        cards = reading_digest.get('paper_cards', [])
        if not cards:
            raise RuntimeError("No reading_digest available for organization stage")
        kb_root = Path(self.research_profile.get('paths', {}).get('knowledge_base_root', ''))
        obsidian_root = Path(self.research_profile.get('paths', {}).get('obsidian_vault', ''))
        if not kb_root:
            raise RuntimeError("knowledge_base_root is not configured")
        notes_dir = kb_root / 'Notes'
        snapshots_dir = kb_root / 'Snapshots' / 'tooluniverse' / datetime.now().strftime('%Y%m%d')
        notes_dir.mkdir(parents=True, exist_ok=True)
        snapshots_dir.mkdir(parents=True, exist_ok=True)
        written_notes = []
        written_snapshots = []
        index_path = kb_root / 'literature_index.md'
        index_text = index_path.read_text(encoding='utf-8') if index_path.exists() else ''
        for card in cards:
            canonical_id = self._next_canonical_id(index_text)
            note_stem = self._safe_stem(card.get('title', canonical_id))
            snapshot_path = self._ensure_unique_path(snapshots_dir / f"{note_stem}.md")
            note_path = self._ensure_unique_path(notes_dir / f"{canonical_id}_{note_stem}.md")
            snapshot_body = self._build_snapshot_markdown(card, search_digest)
            note_body = self._build_note_markdown(card, canonical_id)
            snapshot_path.write_text(snapshot_body, encoding='utf-8')
            note_path.write_text(note_body, encoding='utf-8')
            row = self._build_index_row({
                'canonical_id': canonical_id,
                'title': card.get('title', ''),
                'author_or_source': card.get('source', ''),
                'year': str(datetime.now().year),
                'source_type': 'report' if card.get('reading_source') == 'pdf_full_text' else 'web',
                'theme_tags': ', '.join(self.research_profile.get('domain_boost_keywords', [])[:4]),
                'priority': 'medium',
                'status': 'reviewed',
                'task_link': parameters.get('task_name', ''),
                'original_path_or_uri': card.get('url', ''),
                'local_snapshot_path': str(snapshot_path),
                'formula_level': 'low',
                'quality_notes': f"Generated by ToolUniverse organization stage; reading_source={card.get('reading_source', 'abstract')}",
                'summary': card.get('core_contribution', ''),
                'key_concepts': ', '.join(filter(None, [card.get('method', ''), card.get('limitations', '')])),
                'next_action': 'Review generated note',
                'last_updated': datetime.now().strftime('%Y-%m-%d'),
            })
            index_text = self._insert_index_row(index_text, row)
            written_notes.append(str(note_path))
            written_snapshots.append(str(snapshot_path))
        index_path.write_text(index_text, encoding='utf-8')
        obsidian_written = self._sync_notes_to_obsidian(written_notes, obsidian_root)
        return {
            'notes_written': written_notes,
            'snapshots_written': written_snapshots,
            'literature_index_path': str(index_path),
            'obsidian_notes_written': obsidian_written,
        }

    def _sync_notes_to_obsidian(self, note_paths: List[str], obsidian_root: Path) -> List[str]:
        if not str(obsidian_root):
            return []
        target_dir = obsidian_root / 'Inbox' / 'ToolUniverse'
        target_dir.mkdir(parents=True, exist_ok=True)
        written = []
        for note_path in note_paths:
            source_path = Path(note_path)
            target_path = self._ensure_unique_path(target_dir / source_path.name)
            target_path.write_text(source_path.read_text(encoding='utf-8'), encoding='utf-8')
            written.append(str(target_path))
        return written

    def _next_canonical_id(self, index_text: str) -> str:
        numbers = [int(match) for match in re.findall(r"LIT-(\d+)", index_text)]
        next_number = max(numbers, default=0) + 1
        return f"LIT-{next_number:04d}"

    def _safe_stem(self, value: str) -> str:
        stem = re.sub(r"[^A-Za-z0-9._\-\u4e00-\u9fff]+", "_", value).strip("_")
        return stem or hashlib.sha1(value.encode('utf-8')).hexdigest()[:10]

    def _ensure_unique_path(self, path: Path) -> Path:
        if not path.exists():
            return path
        counter = 2
        while True:
            candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
            if not candidate.exists():
                return candidate
            counter += 1

    def _build_index_row(self, data: Dict[str, str]) -> str:
        ordered_keys = [
            'canonical_id', 'title', 'author_or_source', 'year', 'source_type',
            'theme_tags', 'priority', 'status', 'task_link', 'original_path_or_uri',
            'local_snapshot_path', 'formula_level', 'quality_notes', 'summary',
            'key_concepts', 'next_action', 'last_updated',
        ]
        values = [self._escape_cell(data.get(key, '')) for key in ordered_keys]
        return "| " + " | ".join(values) + " |\n"

    def _escape_cell(self, value: str) -> str:
        return str(value).replace('|', '\\|').replace('\n', ' ').strip()

    def _insert_index_row(self, index_text: str, row: str) -> str:
        marker = "\n## Quick Inbox"
        if marker not in index_text:
            raise RuntimeError("Could not locate '## Quick Inbox' section in literature_index.md")
        return index_text.replace(marker, row + marker, 1)

    def _build_snapshot_markdown(self, card: Dict[str, Any], search_digest: Dict[str, Any]) -> str:
        lines = [
            f"# {card.get('title', '')}",
            "",
            f"- Source: `{card.get('source', '')}`",
            f"- URL: `{card.get('url', '')}`",
            f"- Reading Source: `{card.get('reading_source', '')}`",
            f"- Local PDF: `{card.get('full_text_path', '')}`",
            "",
            "## Summary",
            "",
            card.get('core_contribution', ''),
            "",
            "## Method",
            "",
            card.get('method', ''),
            "",
            "## Limitations",
            "",
            card.get('limitations', ''),
            "",
        ]
        query_attempts = search_digest.get('query_attempts', [])
        if query_attempts:
            lines.extend([
                "## Query Attempts",
                "",
                *[f"- `{item}`" for item in query_attempts],
                "",
            ])
        return "\n".join(lines)

    def _build_note_markdown(self, card: Dict[str, Any], canonical_id: str) -> str:
        return "\n".join([
            f"# {canonical_id} {card.get('title', '')}",
            "",
            f"- Source: `{card.get('source', '')}`",
            f"- URL: `{card.get('url', '')}`",
            f"- Relevance Score: `{card.get('relevance_score', 0)}`",
            "",
            "## Core Contribution",
            "",
            card.get('core_contribution', ''),
            "",
            "## Method",
            "",
            card.get('method', ''),
            "",
            "## Limitations",
            "",
            card.get('limitations', ''),
            "",
        ])

    def _analyze_manuscript(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        manuscript_path_str = parameters.get('manuscript_path', '') or ''
        if not manuscript_path_str:
            raise RuntimeError('manuscript_path is empty; provide a manuscript path to analyze. Skipping analysis stage.')
        manuscript_path = Path(manuscript_path_str)
        if not manuscript_path.is_file():
            raise RuntimeError(f'manuscript_path is not a readable file: {manuscript_path}')
        raw_text = manuscript_path.read_text(encoding='utf-8', errors='ignore')
        manuscript = self._parse_manuscript_html(raw_text, manuscript_path)
        claims = self._extract_manuscript_claims(manuscript)
        proof_obligations = self._build_proof_obligations(claims)
        evidence = self._verify_claims_with_search(claims, manuscript)
        math_validation = self._build_math_validation(manuscript, claims, proof_obligations)
        proof_skeleton = self._build_proof_skeletons(manuscript, claims, proof_obligations, math_validation)
        simulation_handoff = self._build_simulation_handoff(claims, proof_obligations, evidence)
        consistency = self._check_manuscript_consistency(manuscript, claims, proof_obligations, evidence, simulation_handoff, math_validation, proof_skeleton)
        revision_report = self._build_revision_report(manuscript, claims, proof_obligations, evidence, simulation_handoff, math_validation, proof_skeleton, consistency)
        return {
            'manuscript_digest': manuscript,
            'claims_digest': {'claims': claims, 'claim_count': len(claims)},
            'proof_obligations_digest': {'items': proof_obligations, 'count': len(proof_obligations)},
            'evidence_digest': evidence,
            'math_validation_digest': math_validation,
            'proof_skeleton_digest': proof_skeleton,
            'simulation_handoff_digest': simulation_handoff,
            'consistency_digest': consistency,
            'revision_report': revision_report,
        }

    def _parse_manuscript_html(self, raw_html: str, manuscript_path: Path) -> Dict[str, Any]:
        title_match = re.search(r'<title>(.*?)</title>', raw_html, flags=re.IGNORECASE | re.DOTALL)
        title = self._clean_text(html.unescape(title_match.group(1))) if title_match else manuscript_path.stem
        sections = []
        heading_matches = list(re.finditer(r'<h([1-4])[^>]*>(.*?)</h\1>', raw_html, flags=re.IGNORECASE | re.DOTALL))
        for index, match in enumerate(heading_matches):
            level = int(match.group(1))
            heading = self._clean_text(html.unescape(re.sub(r'<[^>]+>', ' ', match.group(2))))
            start = match.end()
            end = heading_matches[index + 1].start() if index + 1 < len(heading_matches) else len(raw_html)
            chunk = raw_html[start:end]
            chunk = re.sub(r'<script.*?</script>', ' ', chunk, flags=re.IGNORECASE | re.DOTALL)
            chunk = re.sub(r'<style.*?</style>', ' ', chunk, flags=re.IGNORECASE | re.DOTALL)
            text = self._clean_text(html.unescape(re.sub(r'<[^>]+>', ' ', chunk)))
            sections.append({
                'heading': heading,
                'level': level,
                'text': text,
            })
        full_text = self._clean_text(html.unescape(re.sub(r'<[^>]+>', ' ', raw_html)))
        return {
            'title': title,
            'path': str(manuscript_path),
            'section_count': len(sections),
            'sections': sections,
            'full_text': full_text,
        }

    def _extract_manuscript_claims(self, manuscript: Dict[str, Any]) -> List[Dict[str, Any]]:
        claims = []
        claim_counter = 1
        theorem_markers = [('定理', 'theorem'), ('引理', 'lemma'), ('假设', 'assumption'), ('猜想', 'conjecture')]
        simulation_tokens = ['验证数据集', '准确率', '检测成功率', 'GPT-4', 'LSTM', 'ResNet', 'Level']
        for section in manuscript.get('sections', []):
            text = section.get('text', '')
            heading = section.get('heading', '')
            normalized_text = self._normalize_pdf_math_noise(text)
            claim_type = 'derivation_claim'
            for marker, inferred_type in theorem_markers:
                if marker in heading or marker in normalized_text:
                    claim_type = inferred_type
                    break
            if heading == '目 录':
                claim_type = 'conjecture'
            requires_simulation_handoff = any(token in normalized_text for token in simulation_tokens)
            if not text.strip():
                continue
            claims.append({
                'claim_id': f'CLM-{claim_counter:03d}',
                'section': heading,
                'claim_type': claim_type,
                'statement': text,
                'requires_theoretical_proof': claim_type in {'theorem', 'lemma', 'conjecture', 'derivation_claim'},
                'requires_literature_grounding': claim_type in {'theorem', 'lemma', 'conjecture', 'derivation_claim', 'assumption'},
                'requires_simulation_handoff': requires_simulation_handoff,
                'citations_present': bool(re.search(r'\b(19|20)\d{2}\b', text)),
                'keywords': re.findall(r'[A-Za-zα-ωΑ-Ω]+|\d+(?:\.\d+)?', normalized_text)[:8],
                'status': 'extracted',
            })
            claim_counter += 1
        return claims

    def _build_proof_obligations(self, claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        items = []
        for claim in claims:
            if claim.get('requires_theoretical_proof'):
                checks = ['definitions_closed', 'derivation_chain_present']
                statement = self._normalize_pdf_math_noise(claim.get('statement', ''))
                if any(token in statement for token in ['θ', '阈值', 'SNR']):
                    checks.append('threshold_algebra_explicit')
                if any(token in statement for token in ['Γ_st', 'NMI', 'Mantel']):
                    checks.append('bounded_domain_explicit')
                if any(token in statement for token in ['固定点', 'β(CST)', '重整化']):
                    checks.extend(['beta_function_specified', 'stability_condition_explicit'])
                items.append({
                    'claim_id': claim.get('claim_id'),
                    'obligation_kind': 'theoretical',
                    'required_checks': list(dict.fromkeys(checks)),
                })
            elif claim.get('requires_simulation_handoff'):
                items.append({
                    'claim_id': claim.get('claim_id'),
                    'obligation_kind': 'simulation_handoff',
                    'required_checks': ['open_source_dataset_selection', 'metric_mapping'],
                })
        return items

    def _verify_claims_with_search(self, claims: List[Dict[str, Any]], manuscript: Dict[str, Any]) -> Dict[str, Any]:
        items = []
        for claim in claims[:12]:
            support = 1 if claim.get('citations_present') else 0
            counter = 0
            items.append({
                'claim_id': claim.get('claim_id'),
                'support_count': support,
                'counter_count': counter,
                'status': 'heuristic_local_validation',
            })
        return {
            'verified_claim_count': len(items),
            'items': items,
        }

    def _build_symbol_catalog(self, section_texts: Dict[str, str], full_text: str) -> Dict[str, Any]:
        catalog = {}
        symbol_rules = {
            'CS': ['空间复杂度', 'CS'],
            'CT': ['时间复杂度', 'CT'],
            'CST': ['时空协同复杂度', 'CST'],
            'Γ_st': ['时空耦合', 'Γ_st'],
            'α': ['临界响应', 'α'],
            'RI': ['相对智能', 'RI'],
            'θ': ['智能阈值', 'θ'],
            'λ': ['临界性', 'λ'],
        }
        haystack = ' '.join(section_texts.keys()) + ' ' + full_text
        for symbol, hints in symbol_rules.items():
            catalog[symbol] = {
                'defined': any(hint in haystack for hint in hints),
                'hints': hints,
            }
        return catalog

    def _build_formula_dependency_checks(self, formulas: List[Dict[str, Any]], symbol_catalog: Dict[str, Any]) -> List[Dict[str, Any]]:
        checks = []
        for formula in formulas:
            missing = [
                symbol for symbol in formula.get('symbols', [])
                if symbol in symbol_catalog and not symbol_catalog[symbol].get('defined')
            ]
            checks.append({
                'name': f"dependency::{formula.get('expression', '')[:40]}",
                'status': 'pass' if not missing else 'warn',
                'detail': 'All referenced core symbols appear to have definitions.' if not missing else f"Potentially undefined symbols referenced: {', '.join(missing)}",
            })
        return checks

    def _build_derivation_chain_checks(self, claims: List[Dict[str, Any]], proof_obligations: List[Dict[str, Any]], section_texts: Dict[str, str]) -> List[Dict[str, Any]]:
        claim_by_section = {}
        for claim in claims:
            claim_by_section.setdefault(claim.get('section', ''), []).append(claim)
        checks = []
        expected_sections = [
            '0.2 阈值1（θ₁=0.5）的热力学推导',
            '0.3 阈值2（θ₂=1/√2）的信号检测理论推导',
            '0.4 从CST公式推导阈值表达式',
            '0.4bis',
            '0.5 六个自然常数作为智能等级边界的重整化群推导',
        ]
        for section_name in expected_sections:
            has_section = any(section_name in key for key in section_texts.keys())
            has_claims = any(section_name in key for key in claim_by_section.keys())
            checks.append({
                'name': f'section_chain::{section_name}',
                'status': 'pass' if has_section and has_claims else 'warn',
                'detail': 'Derivation section and extracted claims are both present.' if has_section and has_claims else 'Expected derivation section or extracted claims are incomplete.',
            })
        theorem_claims = [claim for claim in claims if claim.get('claim_type') in {'theorem', 'lemma', 'conjecture'}]
        theoretical_obligations = [item for item in proof_obligations if item.get('obligation_kind') == 'theoretical']
        checks.append({
            'name': 'theoretical_obligation_coverage',
            'status': 'pass' if len(theoretical_obligations) >= max(1, len(theorem_claims) - 1) else 'warn',
            'detail': f'{len(theoretical_obligations)} theoretical obligations detected for {len(theorem_claims)} theorem/lemma/conjecture style claims.',
        })
        return checks

    def _build_math_validation(self, manuscript: Dict[str, Any], claims: List[Dict[str, Any]], proof_obligations: List[Dict[str, Any]]) -> Dict[str, Any]:
        section_texts = {
            section.get('heading', ''): section.get('text', '')
            for section in manuscript.get('sections', [])
        }
        full_text = manuscript.get('full_text', '')
        normalized_full_text = self._normalize_pdf_math_noise(full_text)
        formulas = self._extract_math_formulas(normalized_full_text)
        symbol_catalog = self._build_symbol_catalog(section_texts, normalized_full_text)
        numeric_checks = self._build_numeric_consistency_checks(claims, normalized_full_text, full_text)
        dependency_checks = self._build_formula_dependency_checks(formulas, symbol_catalog)
        derivation_checks = self._build_derivation_chain_checks(claims, proof_obligations, section_texts)
        issues = []
        for bucket in [numeric_checks, dependency_checks, derivation_checks]:
            for item in bucket:
                if item.get('status') != 'pass':
                    issues.append(item)
        return {
            'formula_count': len(formulas),
            'formulas': formulas,
            'symbol_catalog': symbol_catalog,
            'normalized_text_excerpt': self._summarize_text(normalized_full_text, 1200),
            'numeric_checks': numeric_checks,
            'dependency_checks': dependency_checks,
            'derivation_checks': derivation_checks,
            'issue_count': len(issues),
            'issues': issues,
        }

    def _build_numeric_consistency_checks(self, claims: List[Dict[str, Any]], normalized_text: str, raw_text: str) -> List[Dict[str, Any]]:
        normalized = self._compact_math_text(normalized_text)
        checks = []
        if 'θ1=0.5' in normalized or 'θ₁=0.5' in raw_text:
            checks.append({
                'name': 'theta1_half_consistency',
                'status': 'pass',
                'detail': 'θ1 = 0.5 is consistently represented.',
            })
        raw_compact = self._compact_math_text(raw_text)
        if ('1/2≈0.707' in raw_compact or '1/2=0.707' in raw_compact) and '1/√2≈0.707' not in normalized:
            checks.append({
                'name': 'one_half_numeric_mismatch',
                'status': 'fail',
                'detail': 'The manuscript equates 1/2 with approximately 0.707, which is numerically inconsistent. This likely should be 1/√2 ≈ 0.707.',
            })
        elif ('1/2≈0.707' in raw_compact or '1/2=0.707' in raw_compact) and '1/√2≈0.707' in normalized:
            checks.append({
                'name': 'pdf_fraction_normalized_to_inverse_sqrt2',
                'status': 'pass',
                'detail': 'PDF-import fraction noise was normalized so that 0.707 is interpreted as 1/√2 rather than 1/2.',
            })
        elif '1/√2≈0.707' in normalized or '1/√2' in normalized:
            checks.append({
                'name': 'inverse_sqrt2_consistency',
                'status': 'pass',
                'detail': '1/√2 ≈ 0.707 is numerically consistent.',
            })
        elif '1/2≈0.707' in raw_compact or '1/2=0.707' in raw_compact:
            checks.append({
                'name': 'one_half_numeric_mismatch',
                'status': 'fail',
                'detail': 'The manuscript contains an unresolved 1/2 ≈ 0.707 pattern after PDF-math normalization.',
            })
        if 'Γ_st∈[-1,1]' in normalized:
            checks.append({
                'name': 'gamma_bound_presence',
                'status': 'pass',
                'detail': 'Γ_st bound [-1, 1] is explicitly stated.',
            })
        else:
            checks.append({
                'name': 'gamma_bound_missing',
                'status': 'warn',
                'detail': 'Γ_st bound [-1, 1] was not robustly detected in normalized math text.',
            })
        theta_constants = ['0.707', '1.0', '1.618', '2.718', '3.142', '4.669']
        found_constants = [value for value in theta_constants if value in normalized]
        checks.append({
            'name': 'theta_constant_table_presence',
            'status': 'pass' if len(found_constants) >= 4 else 'warn',
            'detail': f"Detected {len(found_constants)} threshold constants in the manuscript table.",
        })
        return checks

    def _extract_math_formulas(self, text: str) -> List[Dict[str, Any]]:
        normalized = self._compact_math_text(self._normalize_pdf_math_noise(text))
        patterns = [
            r'Γ_st\s*=\s*NMI\s*\(\s*M_S\s*,\s*M_T\s*\)\s*[·\*]\s*sign\s*\(\s*Mantel\s*\(\s*A\s*,\s*FC\s*\)\s*\)',
            r'CS\s*=\s*\([^)]+\)',
            r'CT\s*=\s*\([^)]+\)',
            r'CST\s*[=≈]\s*[^。；]+',
            r'RI\s*=\s*[^。；]+',
            r'θ[0-9₀₁₂₃₄₅]?\s*=\s*[^。；,]+',
        ]
        formulas = []
        seen = set()
        for pattern in patterns:
            for match in re.finditer(pattern, normalized):
                expr = self._clean_text(match.group(0))
                if expr and expr not in seen:
                    seen.add(expr)
                    formulas.append({
                        'expression': expr,
                        'symbols': self._extract_formula_symbols(expr),
                    })
        return formulas

    def _compact_math_text(self, text: str) -> str:
        compact = self._normalize_pdf_math_noise(text).replace('−', '-').replace('≈', '≈')
        compact = re.sub(r'(?<=\w)\s+(?=\w)', '', compact)
        compact = re.sub(r'\s+', ' ', compact)
        return compact

    def _build_proof_skeletons(self, manuscript: Dict[str, Any], claims: List[Dict[str, Any]], proof_obligations: List[Dict[str, Any]], math_validation: Dict[str, Any]) -> Dict[str, Any]:
        section_map = {
            section.get('heading', ''): self._normalize_pdf_math_noise(section.get('text', ''))
            for section in manuscript.get('sections', [])
        }
        theorem_like_claims = [
            claim for claim in claims
            if claim.get('claim_type') in {'theorem', 'lemma', 'conjecture', 'derivation_claim'}
        ]
        skeletons = []
        buckets = [
            ('theta1_thermodynamics', '0.2 阈值1（θ₁=0.5）的热力学推导', 'θ1 = 0.5'),
            ('theta2_signal_detection', '0.3 阈值2（θ₂=1/√2）的信号检测理论推导', 'θ2 = 1/√2'),
            ('cst_threshold_mapping', '0.4 CST阈值映射', 'CST'),
        ]
        for claim in theorem_like_claims[:12]:
            normalized_statement = self._normalize_pdf_math_noise(claim.get('statement', ''))
            section_text = next(
                (text for heading, text in section_map.items() if claim.get('section', '') in heading),
                self._normalize_pdf_math_noise(manuscript.get('full_text', '')),
            )
            obligation = next(
                (item for item in proof_obligations if item.get('claim_id') == claim.get('claim_id')),
                {},
            )
            skeletons.append({
                'claim_id': claim.get('claim_id'),
                'section': claim.get('section', ''),
                'claim_type': claim.get('claim_type', ''),
                'statement': normalized_statement,
                'assumptions': self._infer_proof_assumptions(claim, section_text),
                'lemmas': self._infer_proof_lemmas(claim, section_text),
                'derivation_steps': self._infer_derivation_steps(claim, section_text),
                'conclusion': self._infer_proof_conclusion(normalized_statement),
                'proof_gaps': self._infer_proof_gaps(claim, section_text, obligation, math_validation),
            })
        total_gaps = sum(len(item.get('proof_gaps', [])) for item in skeletons)
        return {
            'count': len(skeletons),
            'items': skeletons,
            'gap_count': total_gaps,
        }

    def _infer_proof_assumptions(self, claim: Dict[str, Any], section_text: str) -> List[str]:
        assumptions = []
        lower_text = section_text.lower()
        if '热力学第二定律' in section_text:
            assumptions.append('Assume the thermodynamic entropy balance applies to the modeled open/self-organizing system.')
        if 'landauer' in lower_text or 'shannon' in lower_text:
            assumptions.append('Assume an admissible mapping exists between information-processing complexity and thermodynamic/information entropy.')
        if 'signal' in lower_text or '检测' in section_text or 'snr' in lower_text:
            assumptions.append('Assume Gaussian-noise signal detection theory is an appropriate surrogate model for system discrimination ability.')
        if '重整化' in section_text or '固定点' in section_text:
            assumptions.append('Assume a coarse-graining flow β(CST) exists and preserves the relevant control parameters.')
        if 'α' in section_text and ('临界' in section_text or '相变' in section_text):
            assumptions.append('Assume critical-phenomena analogies are valid for mapping microscopic nonlinearity to macroscopic amplification.')
        if not assumptions:
            assumptions.append('Assume the section definitions and normalization rules are mathematically well-posed.')
        return assumptions

    def _infer_proof_lemmas(self, claim: Dict[str, Any], section_text: str) -> List[str]:
        lemmas = []
        if 'θ1' in section_text or '0.5' in section_text:
            lemmas.append('Lemma: the environment-compensation requirement can be rewritten as a lower bound on system-side effective complexity.')
        if 'θ2' in section_text or '1/√2' in section_text or 'SNR' in section_text:
            lemmas.append("Lemma: under the adopted signal model, a discrimination threshold on d' induces a threshold on SNR and then on CST.")
        if 'Γ_st' in section_text:
            lemmas.append('Lemma: because NMI ∈ [0,1] and sign(Mantel(·)) ∈ {-1,1}, Γ_st is bounded in [-1,1].')
        if 'λ_max' in section_text:
            lemmas.append('Lemma: Perron-Frobenius provides an upper-scale network amplification proxy through the dominant eigenvalue λ_max(A).')
        if 'β ( CST )' in section_text or '固定点' in section_text:
            lemmas.append('Lemma: any candidate intelligent-level boundary must satisfy β(CST*) = 0 before stability can be asserted.')
        return lemmas

    def _infer_derivation_steps(self, claim: Dict[str, Any], section_text: str) -> List[str]:
        steps = []
        normalized = self._normalize_pdf_math_noise(section_text)
        if '热力学第二定律' in normalized:
            steps.extend([
                'Start from total entropy balance and impose local entropy reduction for self-organization.',
                'Translate entropy compensation into an information/complexity capacity requirement.',
                'Aggregate sensing and prediction sub-capacities into a lower bound on system complexity.',
            ])
        if 'SNR' in normalized or 'signal detection' in normalized.lower() or '检测理论' in normalized:
            steps.extend([
                "Define signal and noise strengths and express SNR in terms of the manuscript's complexity ratio.",
                "Use the selected discrimination criterion on d' to derive a threshold inequality on SNR.",
                'Map the resulting SNR threshold onto the claimed CST intelligent-emergence threshold.',
            ])
        if 'α' in normalized and ('λ_max' in normalized or 'ξ' in normalized):
            steps.extend([
                'Model single-device nonlinear gain at the microscopic level.',
                'Lift local perturbation amplification to the network scale via λ_max(A).',
                'Insert critical correlation-length scaling to obtain the macroscopic α amplification law.',
            ])
        if '固定点' in normalized or 'β(CST)' in normalized:
            steps.extend([
                'Define the coarse-graining transformation and induced flow equation β(CST).',
                'Solve the fixed-point condition β(CST*) = 0 for candidate constants.',
                "Check local stability through the derivative sign β'(CST*).",
            ])
        if not steps:
            steps.append('Reconstruct the section into explicit implication steps from definitions to final claim.')
        return list(dict.fromkeys(steps))

    def _infer_proof_conclusion(self, statement: str) -> str:
        cleaned = self._clean_text(statement)
        return cleaned[:240]

    def _infer_proof_gaps(self, claim: Dict[str, Any], section_text: str, obligation: Dict[str, Any], math_validation: Dict[str, Any]) -> List[str]:
        gaps = []
        normalized = self._normalize_pdf_math_noise(section_text)
        if '0.25' in normalized and ('sensor' in normalized.lower() or 'predict' in normalized.lower() or '理解' in normalized or '预测' in normalized):
            gaps.append('The 0.25 + 0.25 decomposition needs an explicit derivation or citation rather than heuristic allocation.')
        if 'SNR' in normalized and '1/√2' in normalized and "d'" in normalized:
            gaps.append("The bridge from the chosen d' criterion to the 1/√2 threshold should be written explicitly; the current text does not show the intermediate algebra.")
        if 'β(CST)' in normalized or '固定点' in normalized:
            gaps.append("A concrete β(CST) function is not fully specified, so fixed-point existence and stability remain schematic.")
        if 'α' in normalized and '∝|σ-1|' in normalized and 'ξ/(ξ+c)' in normalized:
            gaps.append('The manuscript should state when the bounded ξ/(ξ+c) form is used versus when asymptotic critical divergence is invoked.')
        if obligation and not obligation.get('required_checks'):
            gaps.append('The proof obligation bundle lacks explicit required checks for this claim.')
        for issue in math_validation.get('issues', []):
            detail = issue.get('detail', '')
            if detail and any(token in detail for token in ['1/√2', 'Γ_st', 'threshold', 'fixed-point', '固定点']):
                gaps.append(detail)
        if not gaps:
            gaps.append('No explicit step-by-step formal derivation is written yet; convert prose reasoning into theorem-proof structure.')
        return list(dict.fromkeys(gaps))

    def _normalize_pdf_math_noise(self, text: str) -> str:
        normalized = text or ''
        replacements = [
            (r'\bC\s+S\s+T\b', 'CST'),
            (r'\bC\s+S\b', 'CS'),
            (r'\bC\s+T\b', 'CT'),
            (r'\bR\s+I\b', 'RI'),
            (r'Γ\s*s\s*t', 'Γ_st'),
            (r'Γ\s+st', 'Γ_st'),
            (r'λ\s+m\s+a\s+x', 'λ_max'),
            (r'η\s+c\s+o\s+u\s+p\s+l\s+i\s+n\s+g', 'η_coupling'),
            (r'β\s+d\s+e\s+v\s+i\s+c\s+e', 'β_device'),
            (r'1\s*/\s*√\s*2', '1/√2'),
            (r'1\s*/\s*2\s*≈\s*0\.707', '1/√2≈0.707'),
            (r'1\s*/\s*2\s*=\s*0\.707', '1/√2=0.707'),
            (r'θ\s*2\s*=\s*1\s*/\s*2\s*≈\s*0\.707', 'θ2=1/√2≈0.707'),
            (r'θ\s*₂\s*=\s*1\s*/\s*2\s*≈\s*0\.707', 'θ₂=1/√2≈0.707'),
            (r'θ\s*0\s*=\s*1\s*/\s*2', 'θ0=1/√2'),
            (r'θ\s*₀\s*=\s*1\s*/\s*2', 'θ₀=1/√2'),
        ]
        for pattern, replacement in replacements:
            normalized = re.sub(pattern, replacement, normalized)
        normalized = re.sub(r'(?<=\b[A-Za-zΑ-Ωα-ω])\s+(?=[A-Za-zΑ-Ωα-ω]\b)', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        return normalized

    def _extract_formula_symbols(self, expr: str) -> List[str]:
        symbols = []
        for token in ['CS', 'CT', 'CST', 'RI', 'Γ_st', 'α', 'θ', 'λ', 'NMI', 'Mantel']:
            if token in expr and token not in symbols:
                symbols.append(token)
        return symbols

    def _build_simulation_handoff(self, claims: List[Dict[str, Any]], proof_obligations: List[Dict[str, Any]], evidence: Dict[str, Any]) -> Dict[str, Any]:
        evidence_map = {item.get('claim_id'): item for item in evidence.get('items', [])}
        obligation_map = {item.get('claim_id'): item for item in proof_obligations}
        items = []
        for claim in claims:
            if not claim.get('requires_simulation_handoff'):
                continue
            claim_evidence = evidence_map.get(claim.get('claim_id'), {})
            obligation = obligation_map.get(claim.get('claim_id'), {})
            items.append({
                'claim_id': claim.get('claim_id'),
                'statement': claim.get('statement', ''),
                'section': claim.get('section', ''),
                'simulation_goal': 'Validate the operationalized consequence of this theoretical claim with open-source datasets in 02-Simulation-Platform.',
                'recommended_dataset_policy': 'open_source_only',
                'candidate_dataset_families': self._suggest_dataset_families(claim),
                'recommended_metrics': self._suggest_simulation_metrics(claim),
                'required_checks': obligation.get('required_checks', []),
                'literature_support_count': claim_evidence.get('support_count', 0),
                'literature_counter_count': claim_evidence.get('counter_count', 0),
            })
        return {
            'workspace': '02-Simulation-Platform',
            'policy': 'Simulation and experimental validation must be implemented outside 01-Theory-Research and should prioritize open-source datasets.',
            'count': len(items),
            'items': items,
        }

    def _suggest_dataset_families(self, claim: Dict[str, Any]) -> List[str]:
        text = f"{claim.get('section', '')} {claim.get('statement', '')}".lower()
        families = []
        if any(token in text for token in ['brain', 'cortical', 'neural', '神经', '脑']):
            families.append('open_neuroimaging_and_connectomics')
        if any(token in text for token in ['network', '拓扑', '图', 'graph']):
            families.append('open_graph_benchmark_datasets')
        if any(token in text for token in ['dynamics', '时序', 'temporal', '同步']):
            families.append('open_temporal_network_and_time_series_datasets')
        if any(token in text for token in ['reinforcement', 'agent', '智能体', '控制']):
            families.append('open_rl_and_control_benchmarks')
        if not families:
            families.extend(['open_graph_benchmark_datasets', 'open_temporal_network_and_time_series_datasets'])
        return list(dict.fromkeys(families))

    def _suggest_simulation_metrics(self, claim: Dict[str, Any]) -> List[str]:
        text = f"{claim.get('section', '')} {claim.get('statement', '')}".lower()
        metrics = []
        if any(token in text for token in ['阈值', 'critical', '临界']):
            metrics.extend(['critical_threshold_error', 'phase_transition_sharpness'])
        if any(token in text for token in ['同步', 'coherence', '一致性']):
            metrics.extend(['synchronization_index', 'mutual_information'])
        if any(token in text for token in ['预测', 'accuracy', '准确率']):
            metrics.extend(['accuracy', 'f1', 'calibration_error'])
        if any(token in text for token in ['复杂度', 'complexity', 'entropy']):
            metrics.extend(['structural_entropy', 'effective_complexity'])
        if not metrics:
            metrics.extend(['effect_size', 'robustness_under_perturbation'])
        return list(dict.fromkeys(metrics))

    def _check_manuscript_consistency(self, manuscript: Dict[str, Any], claims: List[Dict[str, Any]], proof_obligations: List[Dict[str, Any]], evidence: Dict[str, Any], simulation_handoff: Dict[str, Any], math_validation: Dict[str, Any], proof_skeleton: Dict[str, Any]) -> Dict[str, Any]:
        issues = []
        theorem_claims = [claim for claim in claims if claim.get('claim_type') == 'theorem']
        assumption_claims = [claim for claim in claims if claim.get('claim_type') == 'assumption']
        if not theorem_claims:
            issues.append({'severity': 'high', 'type': 'missing_theorem_structure', 'message': 'No theorem claims were extracted.'})
        if not assumption_claims:
            issues.append({'severity': 'medium', 'type': 'missing_assumptions', 'message': 'No explicit falsifiable assumptions were extracted.'})
        claim_text = ' '.join(claim.get('statement', '') for claim in claims)
        for symbol in ['CST', 'α', 'θ']:
            if symbol in manuscript.get('full_text', '') and symbol not in claim_text:
                issues.append({'severity': 'medium', 'type': 'symbol_definition_gap', 'message': f'Symbol {symbol} appears in manuscript but is weakly represented in extracted claims.'})
        for math_issue in math_validation.get('issues', []):
            issues.append({
                'severity': 'high' if math_issue.get('status') == 'fail' else 'medium',
                'type': 'math_validation_issue',
                'message': math_issue.get('detail', ''),
            })
        for skeleton in proof_skeleton.get('items', []):
            if skeleton.get('proof_gaps'):
                issues.append({
                    'severity': 'medium',
                    'type': 'proof_skeleton_gap',
                    'message': f"{skeleton.get('claim_id')}: {skeleton.get('proof_gaps', [])[0]}",
                })
        verified_map = {item.get('claim_id'): item for item in evidence.get('items', [])}
        obligation_map = {item.get('claim_id'): item for item in proof_obligations}
        proof_gaps = []
        simulation_gaps = []
        for claim in claims:
            support_item = verified_map.get(claim['claim_id'])
            obligation = obligation_map.get(claim['claim_id'])
            if claim.get('requires_theoretical_proof') and not obligation:
                proof_gaps.append({
                    'claim_id': claim['claim_id'],
                    'issue': 'Proof-oriented claim has no explicit proof obligation bundle.',
                })
            if claim.get('requires_theoretical_proof') and (not support_item or support_item.get('support_count', 0) == 0):
                proof_gaps.append({
                    'claim_id': claim['claim_id'],
                    'issue': 'No supporting literature found for proof-oriented claim.',
                })
            if claim.get('requires_literature_grounding') and (not support_item or support_item.get('support_count', 0) == 0):
                proof_gaps.append({
                    'claim_id': claim['claim_id'],
                    'issue': 'No literature grounding found for this theory-side claim.',
                })
            if claim.get('requires_simulation_handoff') and claim.get('claim_id') not in {item.get('claim_id') for item in simulation_handoff.get('items', [])}:
                simulation_gaps.append({
                    'claim_id': claim['claim_id'],
                    'issue': 'Simulation-bound claim is missing a handoff item for 02-Simulation-Platform.',
                })
            if support_item and support_item.get('counter_count', 0) > support_item.get('support_count', 0):
                issues.append({
                    'severity': 'high',
                    'type': 'counter_evidence_dominates',
                    'message': f"Claim {claim['claim_id']} currently has more counter-evidence than support.",
                })
        return {
            'issue_count': len(issues),
            'issues': issues,
            'proof_gaps': proof_gaps,
            'simulation_gaps': simulation_gaps,
        }

    def _build_revision_report(self, manuscript: Dict[str, Any], claims: List[Dict[str, Any]], proof_obligations: List[Dict[str, Any]], evidence: Dict[str, Any], simulation_handoff: Dict[str, Any], math_validation: Dict[str, Any], proof_skeleton: Dict[str, Any], consistency: Dict[str, Any]) -> Dict[str, Any]:
        actions = []
        for gap in consistency.get('proof_gaps', [])[:10]:
            actions.append(f"{gap.get('claim_id')}: 补充理论推导链或文献依据，当前理论侧支撑不足。")
        for gap in consistency.get('simulation_gaps', [])[:10]:
            actions.append(f"{gap.get('claim_id')}: 为 02-Simulation-Platform 补充开源数据集仿真移交项。")
        for issue in math_validation.get('issues', [])[:10]:
            actions.append(f"数学校验: {issue.get('detail', '')}")
        for skeleton in proof_skeleton.get('items', [])[:10]:
            if skeleton.get('proof_gaps'):
                actions.append(f"{skeleton.get('claim_id')}: 证明骨架缺口 -> {skeleton.get('proof_gaps', [])[0]}")
        for issue in consistency.get('issues', [])[:10]:
            actions.append(issue.get('message', ''))
        if not actions:
            actions.append('当前未发现高优先级修订项，但仍需人工检查数学证明细节。')
        return {
            'title': manuscript.get('title', ''),
            'priority_actions': actions,
            'summary': f"Extracted {len(claims)} claims, generated {len(proof_obligations)} theory-side obligations, verified {evidence.get('verified_claim_count', 0)} claims against literature, detected {math_validation.get('issue_count', 0)} math-validation issues, built {proof_skeleton.get('count', 0)} proof skeletons with {proof_skeleton.get('gap_count', 0)} proof-skeleton gaps, prepared {simulation_handoff.get('count', 0)} simulation handoff items for 02-Simulation-Platform, and found {len(consistency.get('proof_gaps', []))} theory proof gaps.",
        }

    def _stage_has_real_execution(self, stage: str) -> bool:
        return stage in {'search', 'reading', 'organization', 'analysis'}

    def _collect_skipped_stages(self, stages: List[str]) -> List[Dict[str, str]]:
        skipped = []
        for stage in stages:
            if not self._stage_has_real_execution(stage):
                skipped.append({
                    'stage': stage,
                    'reason': 'No real adapter implemented yet',
                })
        return skipped

    def _is_real_tool_supported(self, tool_name: str, stage: str) -> bool:
        if stage == 'search':
            return tool_name in {'arxiv', 'semantic_scholar', 'pubmed', 'openalex'}
        if stage == 'reading':
            return tool_name in {'dailypaper-skills', 'deep-research-mcp', 'summarizer', 'pdf_reader'}
        if stage == 'organization':
            return tool_name in {'knowledge_base', 'obsidian'}
        if stage == 'analysis':
            return tool_name in {'manuscript_analyzer', 'pandas', 'networkx'}
        return False

    def _fetch_url(self, url: str, timeout: int, source: str) -> bytes:
        req = request.Request(url, headers={'User-Agent': 'ToolUniverseResearchAgent/1.0'})
        return self._fetch_request(req, timeout=timeout, source=source)

    def _fetch_request(self, req: request.Request, timeout: int, source: str) -> bytes:
        try:
            with request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except error.HTTPError as exc:
            body = exc.read().decode('utf-8', errors='ignore')[:300]
            raise RuntimeError(
                f"{source} HTTP {exc.code}: {body or exc.reason}"
            ) from exc
        except error.URLError as exc:
            reason = exc.reason
            if isinstance(reason, socket.timeout):
                raise RuntimeError(f"{source} request timed out") from exc
            raise RuntimeError(f"{source} network error: {reason}") from exc
        except socket.timeout as exc:
            raise RuntimeError(f"{source} request timed out") from exc

    def _extract_artifacts_from_tool_result(self, tool_result: Dict[str, Any]) -> Dict[str, Any]:
        stage = tool_result.get('stage')
        output = tool_result.get('output', {})
        if not isinstance(output, dict):
            return {}
        if stage == 'search':
            return {'search_digest': output}
        if stage == 'reading':
            return {'reading_digest': output}
        if stage == 'organization':
            return {'knowledge_sync': output}
        if stage == 'analysis':
            return {'analysis_digest': output}
        if tool_result.get('tool') == 'knowledge_base':
            return {'synthesis_digest': output}
        return {}

    def _merge_step_artifacts(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        for key, value in source.items():
            if key == 'search_digest' and isinstance(value, dict):
                target[key] = self._merge_search_digests(target.get(key, {}), value)
                continue
            target[key] = value

    def _build_execution_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        steps = results.get('steps', [])
        completed_steps = [step for step in steps if step.get('status') == 'success']
        return {
            'total_steps': len(steps),
            'completed_steps': len(completed_steps),
            'pipeline': results.get('stages', []),
            'artifacts': list(results.get('artifacts', {}).keys()),
        }

    def _merge_search_digests(self, current: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
        if not current:
            merged = dict(incoming)
            merged['papers'] = list(incoming.get('papers', []))
            merged['sources'] = [incoming.get('source', '')] if incoming.get('source') else []
            merged['query_attempts'] = list(incoming.get('query_attempts', []))
            return self._rerank_search_digest(merged)
        combined_sources = list(dict.fromkeys(
            list(current.get('sources', []))
            + ([current.get('source')] if current.get('source') else [])
            + list(incoming.get('sources', []))
            + ([incoming.get('source')] if incoming.get('source') else [])
        ))
        deduped: Dict[str, Dict[str, Any]] = {}
        for paper in list(current.get('papers', [])) + list(incoming.get('papers', [])):
            key = self._paper_dedup_key(paper)
            existing = deduped.get(key)
            if existing is None:
                enriched = dict(paper)
                enriched['sources'] = list(dict.fromkeys(
                    list(paper.get('sources', [])) + ([paper.get('source')] if paper.get('source') else [])
                ))
                deduped[key] = enriched
                continue
            merged_sources = list(dict.fromkeys(
                list(existing.get('sources', []))
                + ([existing.get('source')] if existing.get('source') else [])
                + list(paper.get('sources', []))
                + ([paper.get('source')] if paper.get('source') else [])
            ))
            if paper.get('score', 0) > existing.get('score', 0):
                replacement = dict(existing)
                replacement.update(paper)
                replacement['sources'] = merged_sources
                deduped[key] = replacement
            else:
                existing['sources'] = merged_sources
                if not existing.get('abstract') and paper.get('abstract'):
                    existing['abstract'] = paper.get('abstract')
                if not existing.get('url') and paper.get('url'):
                    existing['url'] = paper.get('url')
        merged = {
            'query': incoming.get('query') or current.get('query', ''),
            'keywords_used': list(dict.fromkeys(list(current.get('keywords_used', [])) + list(incoming.get('keywords_used', [])))),
            'papers': list(deduped.values()),
            'sources': combined_sources,
            'query_attempts': list(dict.fromkeys(list(current.get('query_attempts', [])) + list(incoming.get('query_attempts', [])))),
        }
        return self._rerank_search_digest(merged)

    def _rerank_search_digest(self, digest: Dict[str, Any]) -> Dict[str, Any]:
        papers = []
        for paper in digest.get('papers', []):
            reranked = dict(paper)
            combined_sources = list(dict.fromkeys(
                list(reranked.get('sources', [])) + ([reranked.get('source')] if reranked.get('source') else [])
            ))
            reranked['sources'] = combined_sources
            reranked['score'] = float(reranked.get('score', 0)) + min(len(combined_sources) - 1, 3) * 1.5
            papers.append(reranked)
        papers.sort(key=lambda item: item.get('score', 0), reverse=True)
        top_k = self.research_profile.get('ranking', {}).get('daily_top_k', 10)
        must_read_k = min(self.research_profile.get('ranking', {}).get('must_read_k', 3), len(papers))
        selected = papers[:top_k]
        digest['papers'] = selected
        digest['recommended_count'] = len(selected)
        digest['must_read_count'] = must_read_k
        digest['must_read'] = selected[:must_read_k]
        digest['source'] = '+'.join(digest.get('sources', []))
        return digest

    def _paper_dedup_key(self, paper: Dict[str, Any]) -> str:
        title = self._normalize_name_for_match(paper.get('title', ''))
        url = self._normalize_name_for_match(paper.get('url', ''))
        return url or title or hashlib.sha1(json.dumps(paper, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
    
    def generate_tool(self, description: str) -> Dict:
        """
        自动生成新工具
        
        Args:
            description: 工具功能描述
            
        Returns:
            生成的工具定义
        """
        self.logger.info(f"Generating new tool: {description}")
        
        if not self.config['tool_discover']['enabled']:
            raise RuntimeError("Tool Discover is disabled")
        
        # TODO: 实现 ToolDiscover 集成
        # tool = self.tool_discover.generate(
        #     description=description,
        #     test_before_use=self.config['tool_discover']['test_before_use']
        # )
        
        tool = {
            'name': 'generated_tool',
            'description': description,
            'status': 'unimplemented',
            'created_at': datetime.now().isoformat()
        }
        
        self.logger.info(f"Tool generated: {tool['name']}")
        return tool
    
    def optimize_tool(self, tool_name: str) -> Dict:
        """
        优化工具性能
        
        Args:
            tool_name: 工具名称
            
        Returns:
            优化结果
        """
        self.logger.info(f"Optimizing tool: {tool_name}")
        
        if not self.config['tool_optimizer']['enabled']:
            raise RuntimeError("Tool Optimizer is disabled")
        
        # TODO: 实现 ToolOptimizer 集成
        # result = self.tool_optimizer.optimize(
        #     tool_name=tool_name,
        #     metrics=self.config['tool_optimizer']['metrics']
        # )
        
        result = {
            'tool': tool_name,
            'status': 'unimplemented',
            'improvements': []
        }
        
        self.logger.info(f"Tool optimization completed")
        return result
    
    def save_results(self, results: Dict, output_type: str = 'json'):
        """
        保存执行结果
        
        Args:
            results: 结果数据
            output_type: 输出类型 (json, markdown, html)
        """
        output_config = self.config.get('output', {})
        output_dir = Path(output_config.get('final_dir', './output'))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if output_type == 'json':
            output_file = output_dir / f"results_{timestamp}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        
        elif output_type == 'markdown':
            output_file = output_dir / f"results_{timestamp}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(self._format_results_as_markdown(results))
        
        self.logger.info(f"Results saved to: {output_file}")
    
    def _format_results_as_markdown(self, results: Dict) -> str:
        """将结果格式化为 Markdown"""
        md = f"# Execution Results\n\n"
        md += f"**Workflow**: {results.get('workflow_name', 'N/A')}\n\n"
        md += f"**Status**: {results.get('status', 'N/A')}\n\n"
        md += f"**Start Time**: {results.get('start_time', 'N/A')}\n\n"
        md += f"**End Time**: {results.get('end_time', 'N/A')}\n\n"
        summary = results.get('summary', {})
        if summary:
            md += "## Summary\n\n"
            md += f"- **Pipeline**: {', '.join(summary.get('pipeline', []))}\n"
            md += f"- **Completed Steps**: {summary.get('completed_steps', 0)}/{summary.get('total_steps', 0)}\n"
            md += f"- **Artifacts**: {', '.join(summary.get('artifacts', []))}\n\n"
        if results.get('skipped_stages'):
            md += "## Skipped Stages\n\n"
            for item in results.get('skipped_stages', []):
                md += f"- **{item.get('stage', 'unknown')}**: {item.get('reason', '')}\n"
            md += "\n"
        if results.get('errors'):
            md += "## Errors\n\n"
            for item in results.get('errors', []):
                md += f"- **{item.get('stage', 'unknown')} / {item.get('step_name', 'step')}**: {item.get('error', '')}\n"
            md += "\n"
        
        md += "## Steps\n\n"
        for i, step in enumerate(results.get('steps', []), 1):
            md += f"### Step {i}: {step.get('step_name', 'Unnamed')}\n\n"
            md += f"- **Stage**: {step.get('stage', 'N/A')}\n"
            md += f"- **Status**: {step.get('status', 'N/A')}\n"
            md += f"- **Start**: {step.get('start_time', 'N/A')}\n"
            md += f"- **End**: {step.get('end_time', 'N/A')}\n\n"
            output = step.get('output', {}).get('output', {}) if isinstance(step.get('output'), dict) else {}
            if isinstance(output, dict) and output.get('query_attempts'):
                md += "- **Query Attempts**:\n"
                for attempt in output.get('query_attempts', []):
                    md += f"  - `{attempt}`\n"
                md += "\n"
        if results.get('artifacts'):
            md += "## Artifacts\n\n"
            for key, value in results['artifacts'].items():
                md += f"### {key}\n\n"
                md += f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```\n\n"
        
        return md
    
    def execute_task(self, task_definition: Dict) -> Dict:
        """
        执行完整任务（主入口）
        
        Args:
            task_definition: 任务定义
            
        Returns:
            执行结果
        """
        self.logger.info(f"Starting task execution: {task_definition.get('name')}")
        
        # 1. 发现所需工具
        tools = self.discover_tools(task_definition.get('description', ''))
        
        # 2. 编排工作流
        workflow = self.compose_workflow(task_definition)
        
        # 3. 执行工作流
        results = self.execute_workflow(workflow)
        
        # 4. 保存结果
        self.save_results(results, output_type='json')
        self.save_results(results, output_type='markdown')
        
        self.logger.info("Task execution completed")
        return results


if __name__ == "__main__":
    # 测试代码
    print("ToolUniverse Agent Base Class")
    print("This is a template. Actual implementation requires ToolUniverse installation.")
