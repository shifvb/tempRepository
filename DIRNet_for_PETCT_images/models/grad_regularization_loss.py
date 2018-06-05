import tensorflow as tf


def grad_xy(deformation_field_matrix):
    """
    得到一阶梯度正则项
    :param deformation_field_matrix: 形变场矩阵（Tensor）
    :return: 正则项
    对于一个矩阵
    [[3 4 5],
     [6 7 8],
     [9 1 2]]
    grad_x = |4 - 3| + |5 - 4| + |7 - 6| + |8 - 7| + |1 - 9| + |2 - 1|
    grad_y = |6 - 3| + |7 - 4| + |8 - 5| + |9 - 6| + |1 - 7| + |2 - 8|
    grad = grad_x + grad_y
    """
    _v = deformation_field_matrix
    _grad = tf.Variable(0, dtype=tf.float32, trainable=False)
    for batch in range(_v.shape[0]):
        for channel in range(_v.shape[3]):
            _grad_x = tf.Variable(0, dtype=tf.float32, trainable=False)
            for row in range(_v.shape[1]):
                for column in range(_v.shape[2] - 1):
                    _grad_x += tf.abs(_v[batch, row, column + 1, channel] - _v[batch, row, column, channel])
            _grad_y = tf.Variable(0, dtype=tf.float32, trainable=False)
            for row in range(_v.shape[1] - 1):
                for column in range(_v.shape[2]):
                    _grad_y += tf.abs(_v[batch, row + 1, column, channel] - _v[batch, row, column, channel])
            _grad += _grad_x + _grad_y
    return _grad
