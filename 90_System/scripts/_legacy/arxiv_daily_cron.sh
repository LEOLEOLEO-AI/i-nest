#!/bin/bash
# iNEST arXiv 日报 cron wrapper
cd /home/work
python3 /vault/scripts/arxiv_to_wiki.py >> /tmp/arxiv_wiki.log 2>&1
