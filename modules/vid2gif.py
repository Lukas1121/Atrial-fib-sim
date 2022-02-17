import imageio
import cv2

def vid2gif(img_arr, filename, options='gif', fpsrate=1):  # turns a series of n pictures in directory into a video of the .avi type or a gif

    if options == 'video':
        out = cv2.VideoWriter(filename + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30*fpsrate)
        for i in range(len(img_arr)):
            out.write(img_arr[i])
        out.release()

    if options == 'gif':
        imageio.mimsave(filename + '.gif', img_arr)
        print('.gif made')

def vid2imgarr(vidname):
    cap = cv2.VideoCapture(vidname+'.avi', 0)
    frame_arr = []
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame_arr.append(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            vid2gif(img_arr=frame_arr,filename=vidname,fpsrate=1)
            break


video = 'name of video minus the file extension probably only works with .avi'
vid2imgarr(video)
print('done')