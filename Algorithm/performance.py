import utils
from collections import defaultdict


# 为点平衡率做准备 记录每次粗划分的节点平衡率
@utils.Getruntime_matched(return_=True)
def get_vertex_map_number(ver_q, adj):
    '''
    功能描述：记录当前图的节点，代表上一个图的多少节点
    输入参数：存储上次节点数量的队列，以及新图和旧图的节点映射关系
    输出参数：存储本次图节点数量的队列。
    '''
    vertex_map_num = [0 for i in range(len(adj))]
    # 第一次插入 队列为空
    if ver_q.qsize() == 0:
        for key in adj.keys():
            if isinstance(adj[key], int):
                vertex_map_num[key] += 1
            else:    
                vertex_map_num[key] += len(adj[key])
        ver_q.put(vertex_map_num)
    # 后期插入依赖于前面的节点
    # 之后的插入，先取出上次的结果
    else:
        adj_ = ver_q.get()
        # 按照本次的 value 遍历
        for key, values in adj.items():
            for value in values:
                # 依次累加
                vertex_map_num[key] += adj_[value]

        ver_q.put(vertex_map_num)

    return ver_q


# 为点边割率做准备 记录每次粗划分的节点间映射关系
@utils.Getruntime_matched(return_=True)
def get_vertex_map_relation(edge_q, adj):
    '''
    功能描述：思想同 get_vertex_map_number 函数，将数量改为序列
    输入参数：存储上次节点映射关系的队列，以及新图和旧图的节点映射关系
    输出参数：存储本次图节点映射关系的队列。
    '''
    vertex_map = defaultdict(list)
    # 第一次插入
    if edge_q.qsize() == 0:
        edge_q.put(adj)
    # 后期插入依赖于前面的节点
    else:
        adj_ = edge_q.get()
        for key, values in adj.items():
            for value in values:
                # 叠加上次的映射关系
                vertex_map[key].extend(adj_[value])
        edge_q.put(vertex_map)

    return edge_q


# 计算节点均衡
@utils.Getruntime_matched()
def print_vertex_balance(ver_q, ver_size_list):
    '''
    功能描述：分区中节点最大值 × 分区数 / 原图节点数
    输入参数：每个分区代表的节点数，历史图粗划分的节点规模
    输出参数：打印节点平衡率
    '''
    vertex_map_num = ver_q.get()
    ver_balance = max(vertex_map_num) * len(vertex_map_num) / ver_size_list[0]
    print('Vertex balance is {:.2f}'.format(ver_balance))


@utils.Getruntime_matched()
def print_edge_cut(edge_q, edge_size_list, origin_graph):
    '''
    功能描述：分区中节点对应回原图，在原图中切割，切割边 / 总边数 为边割率
    输入参数：分区中每个节点对应原图的哪些节点，历史图划分的边规模，原图
    输出参数：打印边割率
    '''
    # 边割率
    # vertex_map 表示新图的点代表旧图的哪些点
    vertex_map = edge_q.get()
    # 建立反映射，降低时间复杂度
    # 即新图的点在旧图中为哪一个
    vertex_map_reverse = {}
    for key, values in vertex_map.items():
        for value in values:
            vertex_map_reverse[value] = key

    edge_cut = 0
    for key, values in vertex_map.items():
        for ver1 in values:
            # 寻找节点的邻居节点，邻居节点和自己在一个分区，则不算边数，如果不再，切割边++
            neibors = origin_graph.get_all_neighbors(ver1)
            for ver2 in neibors:
                if vertex_map_reverse[ver2] != key:
                    edge_cut += 1

    print("Edge Cut is: {:.2f}".format(edge_cut / 2 / edge_size_list[0]))
