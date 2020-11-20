import utils
from collections import defaultdict


# 边融合
@utils.Getruntime_matched(return_=True, visit=True)
def edge_merge(graph):
    '''
    功能描述：返回边的映射关系
    输入参数：图结构
    返回结果：论文中的 M(v) = u 和节点的是否被访问的向量
    '''
    # 统计一个图里面节点的数量
    ver_num = utils.get_graph_vertex_num(graph)

    # 初始化，M[u] = u，括号内为节点索引，值为合并关系
    M = [i for i in range(ver_num)]

    # 标记节点是否被 match
    visited = [False for i in range(ver_num)]

    # 限制融合
    pre_merge = []
    max_num = 0

    if loop != 0:
        pre_merge = ver_q[-1]
        # 获取当前图分区对应几个节点
        for idx, num in enumerate(pre_merge):
            if num >= constrain:
                visited[idx] = True

        max_num = max(pre_merge)
        print(max_num, min(pre_merge), sep=', ')


    # 开始合并, 相邻节点合并在一起
    # 按照边进行合并
    # 第二次改进，从度小的点开始融合
    if max_num != 0:
        for edge in graph.edges():
            # 取边的两个节点
            source, target = edge
            # 获取节点的索引
            ver1_idx = graph.vertex_index[source]
            ver2_idx = graph.vertex_index[target]
            # 节点没被匹配
            if visited[ver1_idx] == False and visited[ver2_idx] == False:
                if pre_merge[ver1_idx] <= max_num / 8 or pre_merge[ver2_idx] <= max_num / 8:
                    # print('here')
                    M[ver1_idx], M[ver2_idx] = ver2_idx, ver1_idx
                    visited[ver1_idx] = visited[ver2_idx] = True
    
    # 开始合并, 相邻节点合并在一起
    # 按照边进行合并
    for edge in graph.edges():
        # 取边的两个节点
        source, target = edge
        # 获取节点的索引
        ver1_idx = graph.vertex_index[source]
        ver2_idx = graph.vertex_index[target]
        # 节点没被匹配
        if visited[ver1_idx] == False and visited[ver2_idx] == False:
            M[ver1_idx], M[ver2_idx] = ver2_idx, ver1_idx
            visited[ver1_idx] = visited[ver2_idx] = True

    # 返回映射信息
    return M, visited


# 叶子节点融合
@utils.Getruntime_matched(return_=True, visit=True)
def leaf_merge(graph, M, visited):
    '''
    功能描述：处理叶子节点融合，并返回映射关系
    输入参数：图结构，之前的映射关系，节点是否被match的标记
    输出参数：叶子节点融合后的映射关系，节点是否被match的标记
    '''
    # 用来存储叶子结点
    L = []  
    # key表示根节点，value表示以key为根的叶子结点
    R = defaultdict(list)  

    # 遍历一遍visited，求满足要求的结点L和R
    for i in range(len(visited)):
        if visited[i] == False and graph.vertex(i).out_degree() == 1:
            L.append(i)
            root = graph.get_out_neighbors(graph.vertex(i))[0]
            R[root].append(i)

    # 根据每一个根节点追溯到以该根节点的所有叶节点，对叶节点进行两两匹配
    # Lr 是一个列表
    for Lr in R.values():
        # 至少有两个叶子节点才能合并
        if len(Lr) >= 2:
            # -1 防止 ver + 1 越界
            for ver in range(0, len(Lr) - 1, 2):
                ver1_idx, ver2_idx = Lr[ver], Lr[ver + 1]
                M[ver1_idx], M[ver2_idx] = ver2_idx, ver1_idx
                visited[ver1_idx] = visited[ver2_idx] = True

    return M, visited


# 双胞胎节点融合
@utils.Getruntime_matched(return_=True, visit=True)
def twin_merge(graph, M, visited):
    '''
    功能描述：返回双胞胎节点融合后的映射关系
    输入参数：图结构，之前的映射关系，节点是否被match的标记
    输出参数：双胞胎融合后的映射关系，节点是否被match的标记
    '''
    # 双胞胎节点非树结构中的定义
    # 度相同即认为是双胞胎节点
    # 创造节点度的桶
    radix = [[] for i in range(2, 67)]
    # 按照是否被访问选取节点, 并按照度数放入桶
    for ver in graph.vertices():
        # 取节点索引
        ver_idx = graph.vertex_index[ver]
        # 按照是否被访问和节点的度进行筛选
        degree = len(graph.get_all_neighbors(ver_idx))
        if visited[ver_idx] == False and degree >= 2 and degree <= 64:
            # 添加节点的索引
            radix[degree].append(ver_idx)

    # 按照桶内的邻接列表进行融合
    for bucket in radix:
        # 两个以上的节点才能融合
        if len(bucket) >= 2:
            # 相反，由项找索引，不然时间复杂度太高
            adj_reverse = defaultdict(list)
            for i in bucket:
                # 按照索引取节点
                # 集合的意思是取消元素顺序的影响，不然顺序会影响判断是否相等 
                # str保证可哈稀
                # adj_list[i].append(set(graph.get_out_neighbors(i)))
                adj_reverse[str(set(graph.get_out_neighbors(i)))].append(i)

            # 邻接列表相同的进行融合
            # （这里我实在不知道怎么写了，于是暴力循环了）
            # 复杂度太高，大图测试直接卡死
            # for key1 in adj_list.keys():
                # for key2 in adj_list.keys():
                    # if key1 != key2 and adj_list[key1] == adj_list[key2]:
                        # if visited[key1] == False and visited[key2] == False:
                            # visited[key1] = visited[key2] = True
                            # M[key1], M[key2] = key2, key1
            
            # 堆排序也复杂度太高
            # 以邻接列表为键，节点索引为 values
            for values in adj_reverse.values():
                if len(values) >= 2:
                    for i in range(0, len(values) - 1, 2):
                        ver1, ver2 = values[i], values[i+1]
                        if visited[ver1] == False and visited[ver2] == False:
                            visited[ver1] = visited[ver2] = True
                            M[ver1], M[ver2] = ver2, ver1

    return M, visited


# 亲戚节点融合
@utils.Getruntime_matched(return_=True, visit=True)
def relative_merge(g, M, visited):
    '''
    功能描述：处理相关节点的融合，并且返回映射关系
    输入参数：图结构，之前的映射关系，节点是否被match的标记
    输出参数：相关节点的映射关系，节点是否被match的标记
    '''
    # 用来存储所寻找的相关节点，字典中的key表示父节点，value表示以该父节点的子节点中没有被匹配的节点
    rel = defaultdict(list)  

    for i in range(len(visited)):
        # 获取每个节点的度
        node_degree = g.vertex(i).out_degree()
        # 检查未得到匹配的节点的度的大小是否>=2
        if node_degree >= 2:
            # 对于未得到匹配的节点的neighbor在进行一次审查
            for vertex in g.vertex(i).out_neighbors():
                # 查找其邻居未匹配的节点，将其存入键值为父节点的列表中
                if visited[g.vertex_index[vertex]] == False:
                    rel[i].append(g.vertex_index[vertex])

    # 对找到的所有的未匹配的相关节点进行匹配
    for vertices in rel.values():
        if len(vertices) >= 2:
            for ver in range(0, len(vertices) - 1, 2):
                ver1_idx, ver2_idx = vertices[ver], vertices[ver + 1]
                if visited[ver1_idx] == False and visited[ver2_idx] == False: 
                    M[ver1_idx], M[ver2_idx] = ver2_idx, ver1_idx
                    visited[ver1_idx] = visited[ver2_idx] = True

    return M, visited
