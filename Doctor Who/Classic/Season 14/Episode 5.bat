vspipe "Episode 5.vpy" -o 3 -c y4m - | x264 --demuxer y4m --preset veryslow --level 41 --me umh --rc-lookahead 250 --profile high --crf 16 --deblock -2:-2 --no-mbtree --qcomp 0.65 --aq-mode 2 --aq-strength 0.80 --merange 32 --ipratio 1.30 --pbratio 1.20 --psy-rd 0.95 --no-dct-decimate --ref 16 -o out.264 -
ffmpeg -i "D:\THE_HAND_OF_FEAR\BDMV\STREAM\00021 PID 1100 L+R 48 1536 DELAY 0ms.dts" -b:a 320k -c:a libopus "English Stereo.opus"
ffmpeg -i "D:\THE_HAND_OF_FEAR\BDMV\STREAM\00021 PID 1101 L+R 48 1536 DELAY 0ms.dts" -b:a 320k -c:a libopus "English Commentary.opus"