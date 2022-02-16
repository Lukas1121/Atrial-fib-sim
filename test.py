import numpy as np
import cv2
import  os
import glob
from PIL import Image


def signal_measure(cells_in_t, col=-1):
    final_signal_in_t = []
    for i in range(len(cells_in_t)):
        signal_in_t = []
        for j in range(len(cells_in_t[i][:, col])):
            if cells_in_t[i][:, col][j] == 10:
                signal_in_t.append(10)
            else:
                signal_in_t.append(0)
        final_signal_in_t.append(np.mean(signal_in_t) / 10 * 100)

    time = np.arange(len(final_signal_in_t))
    return time, final_signal_in_t

time, final_signal_in_t = signal_measure(cells_in_t_fibril)
plt.plot(time, final_signal_in_t, 'k')
plt.xlabel('time step')
plt.ylabel('signal %')



