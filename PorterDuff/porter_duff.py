import os
import numpy as np
from PIL import Image


class PorterDuff(object):
    CLEAR = 0  # [0, 0]
    SRC = 1  # [Sa, Sc]
    DST = 2  # [Da, Dc]
    SRC_OVER = 3  # [Sa + (1 - Sa)*Da, Rc = Sc + (1 - Sa)*Dc]
    DST_OVER = 4  # [Sa + (1 - Sa)*Da, Rc = Dc + (1 - Da)*Sc]
    SRC_IN = 5  # [Sa * Da, Sc * Da]
    DST_IN = 6  # [Sa * Da, Sa * Dc]
    SRC_OUT = 7  # [Sa * (1 - Da), Sc * (1 - Da)]
    DST_OUT = 8  # [Da * (1 - Sa), Dc * (1 - Sa)]
    SRC_ATOP = 9  # [Da, Sc * Da + (1 - Sa) * Dc]
    DST_ATOP = 10  # [Sa, Sa * Dc + Sc * (1 - Da)]
    XOR = 11  # [Sa + Da - 2 * Sa * Da, Sc * (1 - Da) + (1 - Sa) * Dc]
    DARKEN = 12  # [Sa + Da - Sa*Da, Sc*(1 - Da) + Dc*(1 - Sa) + min(Sc, Dc)]
    LIGHTEN = 13  # [Sa + Da - Sa*Da, Sc*(1 - Da) + Dc*(1 - Sa) + max(Sc, Dc)]
    MULTIPLY = 14  # [Sa * Da, Sc * Dc]
    SCREEN = 15  # [Sa + Da - Sa * Da, Sc + Dc - Sc * Dc]
    ADD = 16  # Saturate(S + D)
    OVERLAY = 17

    def __init__(self, source_arr, destination_arr):
        self._source_color = source_arr[:, :, :-1]
        self._source_alpha = source_arr[:, :, -1:]
        self._destination_color = destination_arr[:, :, :-1]
        self._destination_alpha = destination_arr[:, :, -1:]
        self._out_color = None
        self._out_alpha = None

    def alpha_composition(self, mode):
        if mode == PorterDuff.CLEAR:
            self._clear_mode()
        elif mode == PorterDuff.SRC:
            self._src_mode()
        elif mode == PorterDuff.DST:
            self._dst_mode()

        else:
            raise ValueError("Not a Valid Mode: {}".format(mode))
        return np.concatenate([self._out_color, self._out_alpha], axis=2)

    def _clear_mode(self):  # CLEAR = 0  # [0, 0]
        self._out_color = np.ones_like(self._source_color, dtype=np.uint8) * 255
        self._out_alpha = np.ones_like(self._source_alpha, dtype=np.uint8) * 255

    def _src_mode(self):  # SRC = 1  # [Sa, Sc]
        self._out_color = self._source_color
        self._out_alpha = self._source_alpha

    def _dst_mode(self):  # DST = 2  # [Da, Dc]
        self._out_color = self._destination_color
        self._out_alpha = self._destination_alpha


def porter_duff(mode):
    _pd = PorterDuff(source_arr, destination_arr)
    return _pd.alpha_composition(mode)


if __name__ == '__main__':
    source_img = Image.open(r"C:\Users\anonymous\Desktop\1\source.png").convert(mode='RGBA')
    destination_img = Image.open(r"C:\Users\anonymous\Desktop\1\destination.png").convert(mode='RGBA')
    source_arr = np.array(source_img)
    destination_arr = np.array(destination_img)

    out_path = r'C:\Users\anonymous\Desktop\1\out.png'
    out_arr = porter_duff(PorterDuff.DST)
    Image.fromarray(out_arr, "RGBA").save(out_path)
