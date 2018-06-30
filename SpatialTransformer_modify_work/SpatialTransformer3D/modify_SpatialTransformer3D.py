import os
import numpy as np
import tensorflow as tf
from PIL import Image
from SpatialTransformer_modify_work.SpatialTransformer3D.SpatialTransformer3D import SpatialTransformer3D


def main():
    pass


def load_arrs(load_dir, n):
    load_dir = os.path.abspath(load_dir)
    img_names = [os.path.join(load_dir, _) for _ in os.listdir(load_dir)]
    _L = []
    for batch_num in range(n):
        # 获取单个batch并排序
        batch_img_names = list(filter(lambda _: "batch_{}".format(batch_num) in _, img_names))
        batch_img_names.sort(key=lambda _: int(os.path.split(_)[-1].split(".")[0].split("_")[-1]))
        # 加载图像
        _arr = np.stack([np.array(Image.open(_)) for _ in batch_img_names], axis=2)  # [height, width, depth, channel]
        _L.append(_arr)
    _arrs = np.stack(_L, axis=0)  # [batch, height, width, depth, channel]
    return _arrs


def save_arrs(arrs, save_dir):
    # 删除
    if os.path.exists(save_dir):
        [os.remove(os.path.join(save_dir, _)) for _ in os.listdir(save_dir)]
        os.rmdir(save_dir)
    os.mkdir(save_dir)
    # 保存
    name = os.path.join(os.path.abspath(save_dir), "batch_{}_depth_{}.jpg")
    for batch_num in range(arrs.shape[0]):
        for depth_num in range(arrs.shape[3]):
            _arr = arrs[batch_num, :, :, depth_num, :]
            Image.fromarray(_arr).save(name.format(batch_num, depth_num))


if __name__ == '__main__':
    main()
