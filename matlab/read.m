video = VideoReader('Test Your Awareness.avi');

x = [time, type1, LporX, LporY, RporX, RporY];

video = video + x;

while hasFrame(video)
    frame = readFrame(video);
    imshow(frame);
end