import cv2


def test():
	videoFile = cv2.VideoCapture('2001_03_16_19_00.mpg')
	framecount = videoFile.get(cv2.CAP_PROP_FRAME_COUNT)
	print(framecount)
	fps = videoFile.get(cv2.CAP_PROP_FPS)
	print(fps)
	duration = int(framecount/fps)
	print(duration)
	k = 0
	while videoFile.isOpened():
		ret, frame = videoFile.read()
		if ret != True:
			break
		k += 1
	print(k)



test()