import numpy as np
import video_func as vid
import time

def timeit(f):

    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result

    return timed

class AF:
    def __init__(self,N,tmax,dt,t_r,dys_link_prob,img_save_dir='temp',pulse_time=100,killed_cells = None):
        self.N = self.update_broken_links(N)
        self.tmax = tmax
        self.dt = dt
        self.t_r = t_r
        self.activate = 1
        self.dys_cell_prob = dys_link_prob
        self.img_save_dir = img_save_dir
        self.pulse_time = pulse_time
        self.killed_cells = killed_cells

    def update_broken_links(self,N):
        broken_left_link_list = []
        broken_down_link_list = []
        broken_right_link_list = []
        broken_up_link_list = []
        for (i, j), main_entry in np.ndenumerate(N):
            if len(main_entry) > 2:
                if main_entry[2] == 0:
                    if len(N[i,j-1]) > 2:
                        broken_left_link_list.append([i,j])
                if main_entry[3] == 0:
                    if len(N[i-1, j]) > 2:
                        broken_down_link_list.append([i,j])
                if main_entry[4] == 0:
                    if len(N[i, j+1]) > 2:
                        broken_right_link_list.append([i,j])
                if main_entry[5] == 0:
                    if len(N[i+1, j]) > 2:
                        broken_up_link_list.append([i,j])
        N = self.update_left_link(N,broken_left_link_list)
        N = self.update_down_link(N,broken_down_link_list)
        N = self.update_right_link(N,broken_right_link_list)
        N = self.update_up_link(N,broken_up_link_list)
        return N

    def update_left_link(self,N,broken_links_list):
        for i in range(len(broken_links_list)):
            row = broken_links_list[i][0]
            column = broken_links_list[i][1]-1
            entry_to_change = np.copy(N[row,column])
            entry_to_change[4] = 0
            N[row,column] = entry_to_change
        return N

    def update_down_link(self,N,broken_links_list):
        for i in range(len(broken_links_list)):
            row = broken_links_list[i][0]-1
            column = broken_links_list[i][1]
            entry_to_change = np.copy(N[row,column])
            entry_to_change[5] = 0
            N[row,column] = entry_to_change
        return N

    def update_right_link(self,N,broken_links_list):
        for i in range(len(broken_links_list)):
            row = broken_links_list[i][0]
            column = broken_links_list[i][1]+1
            entry_to_change = np.copy(N[row,column])
            entry_to_change[2] = 0
            N[row,column] = entry_to_change
        return N

    def update_up_link(self,N,broken_links_list):
        for i in range(len(broken_links_list)):
            row = broken_links_list[i][0]+1
            column = broken_links_list[i][1]
            entry_to_change = np.copy(N[row,column])
            entry_to_change[3] = 0
            N[row,column] = entry_to_change
        return N

    def entry_neighbours(self,row,column):
        left = np.copy(self.N[row,column-1])
        down = np.copy(self.N[row-1,column])
        right = np.copy(self.N[row,column+1])
        up = np.copy(self.N[row+1,column])
        return (left,down,right,up)

    def subtract_refract(self,idx_refractory):
        for i in range(len(idx_refractory)):
            row = idx_refractory[i][0]
            column = idx_refractory[i][1]
            entry = np.copy(self.N[row, column])
            entry[1] -= 1
            self.N[row,column] = entry

    def spread_pulse(self,idx_active):
        for i in range(len(idx_active)):
            row = idx_active[i][0]
            column = idx_active[i][1]
            entry = self.N[row,column]
            entry[0] = 0
            entry[1] = self.t_r
            self.N[row, column] = entry
            (left,down,right,up) = self.entry_neighbours(row,column)
            if len(left) > 2:
                if entry[2] != 0:
                    if left[1] == 0:
                        if left[6] != 1:
                            left[0] = self.activate
                            self.N[row,column-1] = left
                        # else:
                        #     if self.prop_dys_cell_dys() == True:
                        #         continue
            if len(down) > 2:
                if entry[3] != 0:
                    if down[1] == 0:
                        if down[6] != 1:
                            down[0] = self.activate
                            self.N[row-1,column] = down
                        else:
                            if self.prop_dys_cell_dys() == True:
                                continue
            if len(right) > 2:
                if entry[4] != 0:
                    if right[1] == 0:
                        if right[6] != 1:
                            right[0] = self.activate
                            self.N[row, column+1] = right
                        # else:
                        #     if self.prop_dys_cell_dys() == True:
                        #         continue
            if len(up) > 2:
                if entry[5] != 0:
                    if up[1] == 0:
                        if up[6] != 1:
                            up[0] = self.activate
                            self.N[row+1, column] = up
                        else:
                            if self.prop_dys_cell_dys() == True:
                                continue

    def prop_dys_cell_dys(self):
        r = np.random.uniform(0, 1)
        if -self.dys_cell_prob <= r <= self.dys_cell_prob:
            return True
        else:
            return False

    def pulse_start(self):
        init_activity = list([1, 0, 1, 1, 1, 1,0])
        print('Im pulsating rn')
        for i in range(1,len(self.N)-1):
            self.N[i, 1] = init_activity

    @timeit
    def main(self):
        ts = 0
        step = 0
        N_arr_t = []
        idx_list_active = []
        idx_list_t_r = []
        while True:
            if step % self.pulse_time == 0:
                self.pulse_start()
                print('ts = %s'%step)
            vid1 = vid.video(self.N, step=step,cells_killed=self.killed_cells)
            vid1.anim_plot()
            if ts >= self.tmax:
                vid1.anim_plot(tmax_break=True)
                break
            for (i,j), entry in np.ndenumerate(self.N):
                if len(entry) > 2:
                    if entry[1] > 0:
                        idx_list_t_r.append([i,j])
                    if entry[0] > 0:
                        idx_list_active.append([i,j])
            if len(idx_list_active) > 0:
                self.spread_pulse(idx_active=idx_list_active)
            if len(idx_list_t_r) > 0:
                self.subtract_refract(idx_refractory=idx_list_t_r)
            idx_list_t_r.clear()
            idx_list_active.clear()
            N_arr_t.append(self.N)
            step += 1
            ts += 1