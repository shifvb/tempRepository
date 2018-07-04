import os
import sys
import pickle
import numpy as np


class MyBatch(object):
    def __init__(self, x_dir: str, y_dir: str, batch_size: int, shuffle: bool):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.shuffle = shuffle
        self.batch_size = batch_size

        self.x_names = [os.path.join(self.x_dir, _) for _ in os.listdir(self.x_dir)]
        self.y_names = [os.path.join(self.y_dir, _) for _ in os.listdir(self.y_dir)]
        self.len = len(self.x_names)
        self._shuffle()

        self.cursor = 0
        self.max_cursor = self.len // self.batch_size

    def next_batch(self):
        _start = self.cursor * self.batch_size
        _end = _start + self.batch_size
        _result = self.rand_x_names[_start: _end], self.rand_y_names[_start: _end]
        self.cursor += 1

        if self.cursor == self.max_cursor:
            self.cursor = 0
            self._shuffle()
        return _result

    def _shuffle(self):
        if self.shuffle:
            rand_idx = np.array(range(self.len), dtype=np.int32)
            np.random.shuffle(rand_idx)
            self.rand_x_names = [self.x_names[_] for _ in rand_idx]
            self.rand_y_names = [self.y_names[_] for _ in rand_idx]
        else:
            self.rand_x_names, self.rand_y_names = self.x_names, self.y_names


def main():
    train_batches = MyBatch(
        x_dir=r"F:\KHJ\3D volume\ct_volume",
        y_dir=r"F:\KHJ\3D volume\pt_volume",
        shuffle=True,
        batch_size=2
    )
    f = open("f:\\t.txt", 'w')
    for i in range(5236):
        _bx, _by = train_batches.next_batch()

        print(_bx, _by, file=f)
        if i % 100 == 0:
            print("iter{}".format(i))
    f.close()


if __name__ == '__main__':
    main()
