实验室杂项代码的集合仓库,集中管理避免散乱

添加其他仓库到子目录
> git remote add -f <new_work> https://github.com/tony-ch/new_work.git  
> git subtree add --prefix=<new_work> <new_work> master

分离出分支
> git subtree split -P <new_work> -b <new_work>

用分离出的分支另建立仓库
> cd ..
> mkdir <new-repo>
> cd <new-repo>
> git init
> git pull </path/to/big-repo>  <name-of-new-branch>

克隆指定分支并使用浅克隆
> git clone --depth 1 -b <target_branch> git@github.com:tony-ch/homework.git
