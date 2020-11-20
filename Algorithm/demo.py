import metis


if __name__ == "__main__":
    # 当图节点小于 scale 时，停止粗划分
    # [1157828, 644106, 366780, 214506, 131004, 84895, 59219, \
    # 44668, 36337, 31392, 28435, 26609, 25439, 24625]
    file_name, scale = 'data/com-youtube.ungraph.txt', 25000
    # file_name, scale = 'data/roadNet-CA.txt', 9000
    # file_name, scale = 'data/email-Eu-core.txt', 100
    # file_name, scale = 'data/musae_git_edges.csv', 200
    metis.run(scale=scale, file_name=file_name)
