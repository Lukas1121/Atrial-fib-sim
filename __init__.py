import main as main_func
import video_func as vid
import numpy as np
import random


class _init_:
    def __init__(self, D, tmax, dt=1, t_r=5, v=0.5, threshold=2, dys_cell_prob=0.05, limit=10, dys_link_prob=0.05):
        self.dys_cell_prob = dys_cell_prob
        self.dys_link_prop = dys_link_prob
        N = np.frompyfunc(list, 0, 1)(np.empty((D, D), dtype=object))
        self.N = self.listify_N(N)
        self.tmax = tmax
        self.dt = dt
        self.t_r = t_r
        self.v = v
        self.threshold = threshold
        self.limit = limit

    def prob_dys_cell(self):
        r = np.random.uniform(0, 1)
        if -self.dys_cell_prob <= r <= self.dys_cell_prob:
            return True
        else:
            return False

    def apply_dys_cells(self):
        dysfunctioning = [0, 0, 1, 1, 1, 1, 1]
        print('%s dysfunctional cells in array' % len(self.index_list))
        for i in range(len(self.index_list)):
            row = self.index_list[i][0]
            column = self.index_list[i][1]
            self.N[row, column] = dysfunctioning

    def listify_N(self, N):
        val = [0, 0, 1, 1, 1, 1, 0]
        saved_index = []
        for (i, j), entry in np.ndenumerate(N):
            entry = val
            N[i, j] = entry
            if i >= 1 and j >= 2:
                if self.prob_dys_cell() == True:
                    saved_index.append([i, j])
        self.index_list = saved_index
        return N

    def set_boundary_of_array(self):
        self.N[0, :] = [list([0])]
        self.N[-1, :] = [list([0])]
        self.N[:, 0] = [list([0])]
        self.N[:, -1] = [list([0])]

    def update_adjacent_links(self, idx, entry, adjacent_entry):
        if len(adjacent_entry) == 1:
            entry[idx] = 0
        return entry

    def entry_neighbours(self, row, column):
        left = np.copy(self.N[row, column - 1])
        down = np.copy(self.N[row - 1, column])
        right = np.copy(self.N[row, column + 1])
        up = np.copy(self.N[row + 1, column])
        return (left, down, right, up)

    def update_border_links(self):
        for (i, j), main_entry in np.ndenumerate(self.N):
            if len(main_entry) > 2:
                (left, down, right, up) = self.entry_neighbours(row=i, column=j)
                if len(left) < 2:
                    entry = np.copy(self.N[i, j])
                    entry = self.update_adjacent_links(entry=entry, adjacent_entry=left, idx=2)
                    self.N[i, j] = entry
                if len(down) < 2:
                    entry = np.copy(self.N[i, j])
                    entry = self.update_adjacent_links(entry=entry, adjacent_entry=down, idx=3)
                    self.N[i, j] = entry
                if len(right) < 2:
                    entry = np.copy(self.N[i, j])
                    entry = self.update_adjacent_links(entry=entry, adjacent_entry=right, idx=4)
                    self.N[i, j] = entry
                if len(up) < 2:
                    entry = np.copy(self.N[i, j])
                    entry = self.update_adjacent_links(entry=entry, adjacent_entry=up, idx=5)
                    self.N[i, j] = entry

    def pulse_start(self):
        self.apply_dys_cells()
        self.set_boundary_of_array()
        self.update_border_links()

    def break_link(self):
        p = 1 - (1 - self.v) ** 2
        x = random.random()
        if x < p:
            return 1
        else:
            return 0

    def iterate_links(self):
        broken_links_counter_h = 0
        broken_links_counter_v = 0
        for i in range(self.limit, len(self.N) - self.limit):
            for j in range(self.limit, len(self.N) - self.limit):
                if len(self.N[i, j]) > 2:
                    entry = np.copy(self.N[i, j])
                    control = np.copy(entry)
                    # entry[2] = self.break_link()
                    entry[3] = self.break_link()
                    self.N[i, j] = entry
                    if control[2] != entry[2]:
                        broken_links_counter_h += 1
                    if control[3] != entry[3]:
                        broken_links_counter_v += 1
        print('i broke %s horizontal links' % (broken_links_counter_h))
        print('i broke %s vertical links' % (broken_links_counter_v))

    def induced_cell_kill(self):
        killed_cells = []
        for i in range(self.limit, len(self.N) - self.limit):
            for j in range(self.limit, len(self.N) - self.limit):
                if len(self.N[i, j]) > 2:
                    r = np.random.normal(0, 1)
                    if -self.threshold <= r <= self.threshold:
                        continue
                    else:
                        killed_cells.append([i, j])
        return killed_cells

    def apply_dead_cells(self):
        dead_cell = [list([0])]
        killed_cell_idx = self.induced_cell_kill()
        print('killing %s cells' % len(killed_cell_idx))
        for i in range(len(killed_cell_idx)):
            row = killed_cell_idx[i][0]
            column = killed_cell_idx[i][1]
            self.N[row, column] = dead_cell
        return len(killed_cell_idx)

    def init(self, break_links=None, treatment=None, skip_first_loop=None):
        if skip_first_loop != True:
            self.pulse_start()
            if break_links == True:
                self.iterate_links()
            np.save('arrays.npy', self.N)
            start = main_func.AF(self.N, self.tmax, self.dt, self.t_r, dys_link_prob=self.dys_link_prop)
            print('Running first loop')
            start.main()
            vid1 = vid.video()
            vid1.graph2vid()

        if treatment or skip_first_loop == True:
            print('Running treatment')
            self.N = np.load('arrays.npy', allow_pickle=True)
            killed_cells = self.apply_dead_cells()
            start = main_func.AF(self.N, self.tmax, self.dt, self.t_r, dys_link_prob=self.dys_link_prop,
                                 img_save_dir='temp2', )
            start.main()
            vid1 = vid.video()
            # vid1.side_by_side(vid2_dir='')
            vid1.graph2vid()
