import os, json, queue
import utils, aggregate, contraction, performance
import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt


# 大规模真实数据
@utils.Getruntime_matched()
def run(scale, file_name):
    '''
    功能描述：完成收缩与聚合，实现粗划分，保留划分记录。
    输入参数：图要收缩到的规模，读取的文件。
    输出参数：图的性能评价：节点平衡率和边割率，图的历史规模（点、边）都可以输出。
    '''

    # 加载图文件
    print("读取数据中")
    graph = utils.read_data(file_name)
    origin_graph = graph.copy()

    # 开始迭代
    # 获取每次的图规模, 当图节点小于一定时停止
    ver_size = utils.get_graph_vertex_num(graph)
    # 存储历史图规模
    ver_size_list = []
    ver_size_list.append(ver_size)
    # 边规模
    edge_size = utils.get_graph_edge_num(graph)
    edge_size_list = []
    edge_size_list.append(edge_size)

    print("当前图节点数{}，边数{}".format(ver_size, edge_size))

    # 记录循环次数
    loop = 0
    # 记录点平衡率
    ver_q = []
    # 记录边割率
    edge_q = []

    # 节点限制
    constrain = (ver_size / scale) * (1 + 0.2)

    while ver_size > scale:

        if len(ver_size_list) >= 2:
            if ver_size_list[-1] >= ver_size_list[-2]:
                break

        # print("第{}次循环".format(loop))

        # 边融合
        # print("边合并开始了")
        M, visited = aggregate.edge_merge(graph, constrain, loop, ver_q)

        # 叶子融合
        # print("叶子合并开始了")
        M, visited = aggregate.leaf_merge(graph, M, visited)

        # 双胞胎融合
        # print("双胞胎合并开始了")
        M, visited = aggregate.twin_merge(graph, M, visited)

        # 亲戚节点融合
        # print("亲戚节点合并开始了")
        M, visited = aggregate.relative_merge(graph, M, visited)

        # 开始收缩
        # print("收缩开始了")
        graph, adj = contraction.contract(graph, M)
        # 保存旧图与新图之间的映射关系，并生成节点的平衡率
        with open('map/real_data_' + str(loop) + '.json', 'w') as outfile:
            # 获取新图的一个节点代表旧图的几个节点，是数量
            ver_q = performance.get_vertex_map_number(ver_q, adj)
            # 获取新图的一个结点代表旧图的哪些节点，是列表
            edge_q = performance.get_vertex_map_relation(edge_q, adj)
            json.dump(adj, outfile, indent=4)

        # 开始产生新图
        # print("产生新图开始了")
        graph = contraction.get_new_graph(graph, adj, M)

        # 获取新图的规模
        ver_size = utils.get_graph_vertex_num(graph)
        ver_size_list.append(ver_size)
        edge_size = utils.get_graph_edge_num(graph)
        edge_size_list.append(edge_size)
        
        print("当前图节点数是{}，边数是{}".format(ver_size, edge_size), end=', ')
        
        # 小到一定规模就可视化
        if ver_size < 200:
            gt.graph_draw(graph, vertex_text=graph.vertex_index, output="output/real_graph_"+str(loop)+".png")

        loop += 1

        # 节点平衡率
        performance.print_vertex_balance(ver_q, ver_size_list)

        # 边割率
        performance.print_edge_cut(edge_q, edge_size_list, origin_graph)
