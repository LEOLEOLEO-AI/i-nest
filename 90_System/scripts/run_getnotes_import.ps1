='utf-8'
python D:\Obsidian\scripts\getnotes_importer.py 2>&1 | Out-File -FilePath D:\Obsidian\scripts\getnotes_log.txt -Append -Encoding UTF8
Write-Host (Get-Date -Format "yyyy-MM-dd HH:mm:ss") "Import completed"
