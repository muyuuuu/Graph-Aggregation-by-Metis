# 简介

一种大规模图的融合算法，即：将一个大图融合成一个便于处理的小图。论文地址：http://glaros.dtc.umn.edu/gkhome/node/1186 ，使用`python`和`graph-tool`复现了论文的第四章算法。

和我可爱且聪明的[师姐](https://github.com/dajiaozhu)一起开发的(其余工作正在进行中，原仓库目前不便开源，所以这里没有显示她是贡献者)。她在双胞胎处理、亲戚节点处理、图融合上提出了关键性想法，使得程序圆满开发成功。

代码在`Algorithm`文件夹下，数据请自己下载并放到对应位置，太大了我就不传上来了。`compare`文件夹是和目前的第三方库进行的对比。

# 依赖

- `python: 3.6`
- `graph-tool: 2.33`(建议用`conda`安装)

## 对比算法的依赖库版本

- `networkx: 2.3`
- `metis: 0.2a4`
- `pymetis: 2020.1`

# 结果

能将[上万节点的图](http://networkrepository.com/email-EU.php)处理成如下所示的模样：

融合到100个节点：
![](figure/2.jpg)

融合到7个节点：
![](figure/1.jpg)

## 打印点平衡率与边割率

每一步融合都能打印点平衡率和边割率：

![](figure/4.png)

# 性能

注：我们算法的目的是实现图融合，并打印点平衡率与边割率。而[metis](https://metis.readthedocs.io/en/latest/)和[pymetis](https://github.com/inducer/pymetis)的目的都是图划分，有一些差距在。

目前性能超过当前`pip install metis`后得到的第三方库的性能，对比详见：https://muyuuuu.github.io/2020/11/20/Metis/

与`pip install pymetis`后得到的第三方库性能还有一些差距，**前路漫漫，还需努力。**

# 实现步骤

文档地址：https://muyuuuu.github.io/2020/11/20/Metis/

开发详细流程、思想、数据结构的使用都放到博客里面了。开发程序的过程中，使用了大量数据结构的使用和程序的设计技巧，如桶排序、哈系、队列、列表、字典的花式操作来降低算法时间和空间复杂度。如果不是非要用`Metis`算法和抱着必死的决心一定要读懂代码，请谨慎观看博客和代码，直接调用即可。

---

# Introduction

An algorithm of huge graph aggregation and contraction based on metis. 

Develop this algorithm with my [partner](https://github.com/dajiaozhu), who has propose the effective ideas about finding twins, finding relatives and contraction. The original repository will be opened until the paper is published so she is not a contributor in this repository.

- Algorithm: The python code of algorithm.
- compare: Performance comparison with current libraries.

# Environment

- `python: 3.6`
- `graph-tool: 2.33`( recommend install it by`conda`)

## The environment of the compared algorithm 

- `networkx: 2.3`
- `metis: 0.2a4`
- `pymetis: 2020.1`

# Results

Process the [graph](http://networkrepository.com/email-EU.php) with tens of thousands of nodes as follows:

Contract to one hundred nodes: ![](figure/2.jpg)

Contract to seven nodes: ![](figure/1.jpg)

## Print the radio of load balance and edge cut

After one contract phase, we can print the radio of load balance and edge cut:![](figure/4.png)

# Performance

Our algorithm is better than [metis](https://metis.readthedocs.io/en/latest/) and slower than [pymetis](https://github.com/inducer/pymetis), [here](https://muyuuuu.github.io/2020/11/20/Metis/) is more details.

# Document of how to implement

You can find the [document](https://muyuuuu.github.io/2020/11/20/Metis/) about how to implement this algorithm. We use some data structure and programming skills to decrease time and space complexity such as bucket, hash, queue, list and dictionary.
