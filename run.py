import sys
sys.path.insert(0, "modules")
import __init__ as i
import video_func as vid
from datetime import datetime
startTime = datetime.now()

tmax = 1000     #says itself
D = 250         #array dimensions DxD


AF = i._init_(D,tmax,
              t_r=25,
              v=0.1,
              threshold=1.95,
              limit=50,
              dys_link_prob=0.085,
              dys_cell_prob=0.04,
              pulse_time = 100)
AF.init(break_links=True,
        treatment=True,
        skip_first_loop = True)

vid1 = vid.video()
vid1.side_by_side(fps=1.75)

print('script took: %s to complete'%(datetime.now() - startTime))