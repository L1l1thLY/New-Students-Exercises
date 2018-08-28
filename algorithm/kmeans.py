import numpy as np
import matplotlib.pyplot as plt
# 载入iris数据
def load_file_data(file_path):
    return np.loadtxt(file_path, dtype=float, comments='@', delimiter=',')

# 去除最后一列的类 tag 后，将训练样本转化为列向量
def presolve_data(unsolved_array):
    class_colomn_removed = unsolved_array[:, 0:4]
    return class_colomn_removed.T

# 随机选取 k 个初始均值向量
def get_init_u(data_set, k):
    init_u = np.zeros((data_set.shape[0], k))
    for i in range(k):
        randint = np.random.randint(0, 150)
        init_u[:, i] = data_set[:, randint]
    return init_u

# 算每个数据到每个均值向量的距离
# 若数据量为 m 个，均值向量为 k 个，求出距离使用 k 行 m 列
# 每列分量代表此列数据距离 k 个均值向量的距离
def distance(data, average_vector):

    number_of_u = average_vector.shape[1]
    number_of_data = data.shape[1]

    distance_mat = np.zeros((number_of_u, number_of_data))

    for i in range(number_of_u):
        distance_mat[i, :] = np.linalg.norm((data - average_vector[:, i].reshape(-1, 1)),
                                            ord=None,
                                            axis=0,
                                            keepdims=True)
    return distance_mat


# 根据距离向量来给数据集合添加分类标签
# 返回一个长度为样本数的分类列向量
def taging(distance_mat):
    number_of_data = distance_mat.shape[1]
    tag_mat = np.zeros((number_of_data, 1), dtype=int)

    dis_min = np.min(distance_mat, axis=0, keepdims=True)
    indices_mat = np.where(distance_mat == dis_min)

    # indices_mat[1] 为样本编号，其对应的 indices_mat[0] 为此样本的分类标记
    data_indexes = indices_mat[1]
    tags = indices_mat[0]

    for i, data_index in enumerate(data_indexes):
        tag_mat[data_index, 0] = tags[i]

    return tag_mat

# 计算新的均值向量
# 利用 where 计算出掩码，和数据集进行点乘求和
def get_new_u(data_set, tag_mat):
    class_num = int(np.max(tag_mat))
    new_average_vectors = np.zeros((data_set.shape[0], class_num + 1))
    for i in range(class_num + 1):
        tag_masks = np.where(tag_mat == i, 1, 0)
        average_vector = 1.0 / np.sum(tag_masks) * np.dot(data_set, tag_masks)
        new_average_vectors[:, i] = average_vector[:, 0]

    return new_average_vectors

# 输入数据应该转换为列向量 * 样本数矩阵
# k 应该少于数据集
def k_means(dataset, k):
    assert (dataset.ndim == 2)
    assert (dataset.shape[1] > k)
    while True:
        average_vector = get_init_u(dataset, k)
        distance_mat = distance(dataset, average_vector)
        tag_vector = taging(distance_mat)
        new_average_vector = get_new_u(dataset, tag_vector)
        if (new_average_vector == average_vector).all:
            break
        else:
            average_vector = new_average_vector
    return tag_vector



def test_function():
    test_dis = np.array([[1,2,3],
                         [3,2,1],
                         [4,1,4]])
    print("Test dis is\n" , test_dis)

    max_mat = np.max(test_dis, axis=0, keepdims=True)

    print("max_mat is" , max_mat)

    indices = np.where(test_dis == max_mat)
    for index, data_index in enumerate(indices[1]):
        print(indices[0][index], data_index)


if __name__ == '__main__':
    data = load_file_data("./TestData/iris.txt")
    #plt.scatter(data[:, 2], data[:, 3], s=10, c=data[:, 4])

    solved = presolve_data(data)
    result = k_means(dataset=solved, k=3)
    for i, value in enumerate(result):
        print("The data ", i , "is", value, "class")

    plt.scatter(data[:, 2], data[:, 3], s=10, c=(result[:, 0] + 2))
    plt.show()
