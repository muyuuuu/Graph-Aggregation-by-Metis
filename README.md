# 简介

一种大规模图的融合算法，即：将一个大图融合成一个便于处理的小图。论文地址：http://glaros.dtc.umn.edu/gkhome/node/1186 ，使用`python`和`graph-tool`复现了论文的第四章算法。

和我可爱的[师姐](https://github.com/dajiaozhu)一起开发的(其余工作正在进行中，原仓库目前不便开源)。

# 依赖

- `python: 3.7`
- `graph-tool: 2.35`(建议用`conda`安装)

# 结果

能将[上万节点的图](http://networkrepository.com/email-EU.php)处理成如下所示的模样：

融合到200个节点：
![](figure/2.jpg)

融合到7个节点：
![](figure/1.jpg)

# 实现步骤

等我博客。