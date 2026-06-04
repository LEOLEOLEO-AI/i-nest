@echo off
cd /d D:\Obsidian\scripts
C:\Users\LEO\AppData\Local\Programs\Python\Python310\python.exe iNEST_crawler.py >> D:\Obsidian\scripts\crawl_log.txt 2>&1
echo Crawl completed at %date% %time% >> D:\Obsidian\scripts\crawl_log.txt
