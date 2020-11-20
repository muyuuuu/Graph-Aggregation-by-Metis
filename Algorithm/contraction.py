import utils
from collections import defaultdict
import graph_tool.all as gt


# 收缩函数
@utils.Getruntime_matched(return_=True, visit=False)
def contract(graph, M):
    '''
    功能描述：节点收缩
    输入参数：图结构，映射关系
    返回参数：邻接列表，收缩后的图结构
    '''
    
    # 获取节点数量
    ver_num = utils.get_graph_vertex_num(graph)

    # 创建向量C 默认值为 -1，防止映射混乱
    C = [-1 for i in range(0, ver_num)]
    # 辅助结构，降低时间负责度
    # C(u) = C(v) = a
    # ass_C[a].append(C(u), C(v))
    ass_C = [[] for i in range(0, ver_num)]

    # 获取 C 的映射关系
    for idx, item in enumerate(M):
        # 防止 [0, 1, 2, 3, 4] 这样的序列被映射
        if M[item] == idx and C[idx] == -1 and C[item] == -1 and item != idx:
            ass_C[idx].append(idx)
            ass_C[idx].append(item)
            C[idx] = C[item] = idx

    # 创建邻接列表
    adj = defaultdict(list)
    
    # 按照向量 C 获取邻接列表
    # 值为 -1, 邻接点为自己，否则，邻接点就是两个
    flag = 0
    C1 = C.copy()
    for idx, item in enumerate(C):
        if item == -1:
            adj[flag].append(idx)
            flag += 1
        # 防止重复添加
        elif len(adj[flag]) == 0 and C1[idx] >= 0:
            idx, idx1 = ass_C[idx][0], ass_C[idx][1]
            adj[flag].append(idx)
            adj[flag].append(idx1)
            # 后面的节点移除序列，防止二次查找
            # 比如 [1, 2, 3, 1]，第四个 1 不用查找
            C1[idx1] = C1[idx] = -2
            flag += 1

    # 一个 bug，list类型的字典最后一个永远是空的，别问，我也不知道为啥
    if len(adj[flag]) == 0:
        del adj[flag]

    return graph, adj


# 生成新图的函数
@utils.Getruntime_matched(return_=True, visit=False)
def get_new_graph(graph, adj, M):
    """
    功能描述：根据提供原始图节点与将生成的图节点间映射关系，生成融合后的图，并且将其返回
    输入参数：图结构，原始图节点与将生成的图节点间映射关系adj
    输出参数：节点融合后的图
    """
    # 获取节点数量
    vertices_num = utils.get_graph_vertex_num(graph)
    
    # 用于表示节点合并后的新图
    new_graph = gt.Graph(directed=False)
    
    # 用于记录合并后得到的新图上的边
    # key值表示生成的新图上的边，value表示这样新边有几条
    new_edges = defaultdict(float)

    # 原始图上的节点映射到新图上的节点
    # 下标表示原始图的节点，列表内容并表示对应下标节点在新图上的索引
    old_mapping_new = [-1 for i in range(vertices_num)]
    
    # 根据原始图和融合后的图节点的映射关系，求出原始图每一个点与新图的映射关系
    # index表示原始图节点索引，old_mapping_new[index]表示原图中index节点在新图的索引
    for new_ver, old_vers in adj.items():
        for old_ver in old_vers:
            old_mapping_new[old_ver] = new_ver
    
    # 获取图的边集
    edges = graph.edges()

    # 判断当前边两个点是否进行融合
    # 如果两个点进行融合，那么这两个顶点在新图上的映射节点相同，则对应边不用考虑
    # 若当前边的两个顶点没有进行融合，则按照新旧图上的映射关系，将边上的顶点换成映射新图上顶点，并将边加入新图边的集合
    for edge in edges:
        source, target = edge
        # 取节点的索引
        s_index = graph.vertex_index[source]
        t_index = graph.vertex_index[target]
        # 旧边的两个节点没有融合
        if old_mapping_new[s_index] != old_mapping_new[t_index]:
            if old_mapping_new[s_index] < old_mapping_new[t_index]:
                new_edges[(old_mapping_new[s_index], old_mapping_new[t_index])] += 1
            else:
                new_edges[(old_mapping_new[t_index], old_mapping_new[s_index])] += 1

    # 获取新生成的图的节点个数
    new_graph_vertices_num = len(adj)
    
    # 给新生成的图添加节点
    new_graph.add_vertex(new_graph_vertices_num)
    
    # 给新生成的图添加边
    for edge in new_edges.keys():
        new_graph.add_edge(edge[0], edge[1])
    
    return new_graph
