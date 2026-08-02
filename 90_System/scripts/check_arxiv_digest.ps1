# check_arxiv_digest.ps1 - Scan arxiv-auto for blank analysis sections
# Usage: powershell -File 90_System/scripts/check_arxiv_digest.ps1
# Criteria (same as arxiv_daily_and_sync.sh step 1.5):
#   S1 (core innovation) / S2 (value analysis): section body empty (only placeholder "、")
#   S3 (suggestions): "answer:" followed by nothing

param(
    [string]$Dir = 'D:\Obsidian\vault\20_Processing\20_KnowledgeBase\arxiv-auto'
)

$files = Get-ChildItem -LiteralPath $Dir -File -Filter '*.md' |
    Where-Object { $_.Name -notmatch '-index' }

$bad = @()
foreach ($f in $files) {
    $c = Get-Content -LiteralPath $f.FullName -Raw -Encoding UTF8
    $s1empty = $c -match '(?s)## 1\. 核心创新\s*[、，,\.\s]*\r?\n\s*## 2'
    $s2empty = $c -match '(?s)## 2\. 对 TCC / iNEST 的价值分析\s*[、，,\.\s]*\r?\n\s*## 3'
    $s3noans = $c -match '(?s)answer:\s*(\r?\n\s*)*(##|---|\*自动抓取)'
    if ($s1empty -or $s2empty -or $s3noans) {
        $bad += [PSCustomObject]@{ File = $f.Name; S1 = $s1empty; S2 = $s2empty; S3 = $s3noans }
    }
}

Write-Host ("Scanned: {0} files | Broken: {1}" -f $files.Count, $bad.Count)
if ($bad.Count -gt 0) {
    Write-Host ("S1 empty: {0}  S2 empty: {1}  S3 no-answer: {2}" -f `
        (($bad | Where-Object S1).Count), (($bad | Where-Object S2).Count), (($bad | Where-Object S3).Count))
    Write-Host "Details:"
    $bad | Format-Table -AutoSize
} else {
    Write-Host "OK - all analysis sections complete"
}
