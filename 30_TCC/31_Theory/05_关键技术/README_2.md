# Get 导出导入脚本

用法：
- 将 Get 笔记导出为 Markdown（zip 或文件夹）
- 在本机运行：
  - `import_get_export.bat "<导出 zip 或目录路径>"`

输出位置：
- Markdown：`00_KnowledgeBase_知识库/03_Inbox_文献与碎片/Get/YYYY-MM/`
- 资源：`assets/get/YYYY-MM/<笔记名>/`

说明：
- 默认会尝试把笔记里的远程图片下载到本地 assets，并将链接替换为相对路径
- 如果下载失败，会保留原始链接
