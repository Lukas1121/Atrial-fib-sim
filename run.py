import __init__ as i
import video_func as vid
from datetime import datetime
startTime = datetime.now()

tmax = 500     #says itself
D = 100         #array dimensions DxD


AF = i._init_(D,tmax,
              t_r=15,
              v=0.15,
              threshold=1.15,
              limit=10,
              dys_link_prob=0.07,
              dys_cell_prob=0.07)
AF.init(break_links=True,
        treatment=True,
        skip_first_loop=True)

vid1 = vid.video()
vid1.side_by_side(fps=1.75)

print('script took: %s to complete'%(datetime.now() - startTime))