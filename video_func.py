import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import glob
# import imageio
from time import sleep


class video:
    def __init__(self,N=None,step=None,t_r=None,cells_killed=None):
        if N == None:
            self.N = np.zeros((5,5))
        else:
            self.N = N
        self.step = step
        self.t_r = t_r
        self.cells_killed = cells_killed
        self.col_map = plt.cm.get_cmap('binary', 40)
        self.cells_killed = self.cells_killed
        if self.cells_killed == None:
            self.filename = 'before treatment'
            self.img_save_dir = 'temp'
        else:
            self.filename = 'after treatment s'
            self.img_save_dir = 'temp2'


    def anim_plot(self, tmax_break=False):
        if tmax_break != True:
            fig, ax = plt.subplots()
            data = np.zeros((len(self.N), len(self.N)))
            for (i, j), entry in np.ndenumerate(self.N):
                if len(entry) > 2:
                    if entry[0] == 1:
                        data[i, j] = 10
                    else:
                        data[i, j] = entry[1]*10
                else:
                    data[i, j] = -10
            plt.imshow(data, cmap=self.col_map)
            plt.title(self.filename)
            if os.path.isdir(self.img_save_dir) == False:
                os.mkdir(self.img_save_dir)
            plt.savefig((self.img_save_dir + '/pic %s.png' % (self.step)))
            plt.close()
            plt.clf()
        #     self.graph2vid_fluid(tmax_break=tmax_break, filename=title,imgdir=self.img_save_dir)
        if tmax_break == True:
            #     self.graph2vid_fluid(tmax_break=tmax_break, filename=title,imgdir=self.img_save_dir)
            print('done with ' + self.filename)

    def signal_measure(self,cells_in_t, col=-2):
        final_signal_in_t = []
        last_column_list = []

        for i in range(len(cells_in_t)):
            arr = cells_in_t[i]
            column = arr[:,col]
            last_column_list.append(column)
        for i in range(len(last_column_list)):
            signal_in_t = []
            for j in range(len(last_column_list)):
                if last_column_list[j][0] == 1:
                    signal_in_t.append(10)
                else:
                    signal_in_t.append(0)
            final_signal_in_t.append(np.mean(signal_in_t) / 10 * 100)

        time = np.arange(len(final_signal_in_t))
        plt.plot(time, final_signal_in_t, 'b')
        plt.xlabel('time step')
        plt.ylabel('signal %')
        plt.show()


    def graph2vid(self, options='video', fpsrate=1, empty_dir_on_done=True): #turns a series of n pictures in directory into a video of the .avi type or a gif
        list1 = os.listdir(self.img_save_dir)
        img_array = []

        size = (800,600)

        if options == 'video':
            for i in range(len(list1)):
                img = cv2.resize(cv2.imread(self.img_save_dir + '/pic %s.png' %(i)),size)
                for n in range(fpsrate):
                    img_array.append(img)
                    if (i + 1) % (len(list1)) == 0:
                        for i in range(fpsrate + 3):
                            img_array.append(img)
            out = cv2.VideoWriter(self.filename + '.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
            for i in range(len(img_array)):
                out.write(img_array[i])
            out.release()
            print('Video made')
        if empty_dir_on_done == True:
            files = glob.glob(self.img_save_dir+'/*')
            for f in files:
                os.remove(f)

    # def graph2vid_fluid(self,imgdir,step=None,tmax_break=None,img_array=[]): # not currently working
    #
    #     size = (800, 600)
    #     if tmax_break != True:
    #         range_start = step - 18
    #         for i in range(range_start,step+1):
    #             img = cv2.resize(cv2.imread(imgdir + '/pic %s.png' % (i)), size)
    #             img_array.append(img)
    #         files = glob.glob(imgdir + '/*')
    #         for f in files:
    #             os.remove(f)
    #     else:
    #         print('it is true')
    #         list1 = os.listdir(imgdir)
    #         for i in range(self.step-len(list1)+1,self.step):
    #             img = cv2.resize(cv2.imread(imgdir + '/pic %s.png' % (i)), size)
    #             img_array.append(img)
    #             out = cv2.VideoWriter(self.filename + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    #         for i in range(len(img_array)):
    #             out.write(img_array[i])
    #         out.release()
    #         print('Video made')
    #
    #         files = glob.glob(imgdir + '/*')
    #         for f in files:
    #             os.remove(f)

    def side_by_side(self,vid1_dir = 'before treatment',vid2_dir = 'after treatment',filename='side by side',stream_live=False, fps=1):
        cap = cv2.VideoCapture(vid1_dir+'.avi', 0)
        cap1 = cv2.VideoCapture(vid2_dir+'.avi', 0)
        size = (1600, 600)
        out = cv2.VideoWriter(filename + '.avi',
                              cv2.VideoWriter_fourcc(*'DIVX'),
                              cap.get(cv2.CAP_PROP_FPS)*fps, (size))
        frame_arr = []
        frame1_arr = []
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                return 0
            ret1, frame1 = cap1.read()
            if ret1 == False:
                return 1
            frame_arr.append(frame)
            frame1_arr.append(frame1)
            print(frame_arr[0].shape)
            if ret == True and ret1 == True:
                h, w, c = frame_arr[-1].shape
                h1, w1, c1 = frame1_arr[-1].shape
                if h != h1 or w != w1:
                    break
                both = np.concatenate((frame_arr[-1], frame1_arr[-1]), axis=1)
                if stream_live == True:
                    sleep(0.028)
                    cv2.imshow(filename, both)
                out.write(both)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        out.release()
        print('finished with video. Filename: '+filename+'.avi')
        # return len()