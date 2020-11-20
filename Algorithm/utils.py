'''
File: utils.py
Project: Graph Partition
===========
File Created: Thursday, 23rd July 2020 10:36:53 am
Author: <<LanLing>> (<<lanlingrock@gmail.com>>)
===========
Last Modified: Thursday, 23rd July 2020 10:37:00 am
Modified By: <<LanLing>> (<<lanlingrock@gmail.com>>)
===========
Description: 封装常用函数
Copyright <<2020>> - 2020, <<XDU>>
'''
import logging, time, re
import graph_tool.all as gt
from numpy.random import randint, seed


# 日志
logging.basicConfig(level=logging.INFO,
                    filemode='w',
                    filename='./log.txt',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 计时函数
# 记录程序执行时间并输出到日志，记录哪里比较耗时，针对性优化
def Getruntime_matched(return_=False, visit=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            since = time.time()
            # 有参数返回，需要返回结果
            if return_ == True:
                # 执行有参数返回的函数时，相当于执行了 wrapper 但后者返回值是空
                result = func(*args, **kwargs)
                end = time.time()
                logger.info((func.__name__).ljust(25, ' ') + "was called, executed: "\
                    + str(round((end - since), 3)) + "s")
                if visit == True:
                    visited = result[1]
                    match_prob = visited.count(True) / len(visited)
                    logger.info("After " + (func.__name__).ljust(18, ' ') + " matching, matched {:.2%}"\
                    .format(match_prob))
                return result
            # 没有参数返回，直接执行
            else:
                func(*args, **kwargs)
                end = time.time()
                logger.info((func.__name__).ljust(25, ' ') + "was called, executed: "\
                    + str(round((end - since), 3)) + "s")
        return wrapper

    return decorator


# 生成图函数
@Getruntime_matched(return_=False, visit=False)
def gene_data(file_name, ver_num, edge_num):
    '''
    输入参数：要保存的文件名，顶点数，边数
    返回：保存图数据的文件
    '''

    seed(100)

    g = gt.Graph(directed=False)
    g.add_vertex(ver_num)

    # 在随机顶点之间添加边
    for s,t in zip(randint(0, ver_num, edge_num), randint(0, ver_num, edge_num)):
        # 如果边已经存在就不添加
        # 自己和自己也不添加
        if g.vertex(s) in g.vertex(t).out_neighbors() or s == t:
            pass
        else:
            g.add_edge(g.vertex(s), g.vertex(t))

    # save graph
    g.save(file_name)


# 统计图内节点个数
@Getruntime_matched(return_=True, visit=False)
def get_graph_vertex_num(graph):
    return max(graph.vertex_index) + 1


# 统计图内边的数量
@Getruntime_matched(return_=True, visit=False)
def get_graph_edge_num(graph):
    return max(graph.edge_index) + 1


# 读取外部文件
@Getruntime_matched(return_=True, visit=False)
def read_data(file_name):
    '''
    功能描述：根据所给文件数据完成图的构建
    输入参数：需要加载的数据的路径， 根据根据所给出的数据构建完图之后进行保存的路径
    输出参数：返回有所给文件数据构建一个图
    '''
    regex = ",|，|\\s+|\t"
    g = gt.Graph(directed=False)

    with open(file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            # 文件中的数据的每一行是图上的每一条边的两个顶点
            temp = re.split(regex, line)
            g.add_edge(int(temp[0]), int(temp[1]))
        
        f.close()
    
    return g
