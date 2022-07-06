ffmpeg -i 00066.m2ts -map 0:v:0 -f yuv4mpegpipe - | x265 --y4m --crf 20 - -o out.265
ffmpeg -i 00066.m2ts -map 0:a:0 -b:a 256000 eng.opus
ffmpeg -i 00066.m2ts -map 0:a:2 -b:a 256000 jp.opus