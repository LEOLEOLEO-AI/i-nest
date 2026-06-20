
进入从 Genspark Claw下载的 Gitee知识库压缩包，解压缩后进入 Workspace 文件夹，右键选择：Open Git Bash here

点击这个选项后，会弹出一个黑色的命令行窗口。然后您把刚才的那 6 行代码一次性复制，然后在黑框里右键点击“Paste（粘贴）”，再按一下回车键 (Enter) 就可以了：

git init
git add .
git commit -m "First commit from local Obsidian"
git branch -M main
git remote add origin https://gitee.com/iBrainNest/i-nest.git
git push -u origin main

如果 Obsidian 里做了修改，可以在 Git 中敲这个命令，把修改推到 Git 里。

git commit -am "改了一点想法"
git push
