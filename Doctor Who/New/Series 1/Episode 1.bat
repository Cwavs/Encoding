ffmpeg -i "E:\DOCTOR_WHO_S1D1\BDMV\STREAM\00045 PID 1100 5.1 48 1536 DELAY 0ms.dts" -f wav - | opusenc --bitrate 320 --vbr - "English Surround.opus"
ffmpeg -i "E:\DOCTOR_WHO_S1D1\BDMV\STREAM\00045 PID 1101 48 1536 DELAY 0ms.dts" -f wav - | opusenc --bitrate 320 --vbr - "English Commentary.opus"
copy "E:\DOCTOR_WHO_S1D1\BDMV\STREAM\00045 PID 1102 2.0ch 48KHz 192Kbps DELAY 0ms.ac3" "English Audio Description.ac3"
vspipe "Episode 1.vpy" -o 5 -c y4m - | x264 --demuxer y4m --preset placebo --me umh --rc-lookahead 250 --profile high --crf 19 --deblock -2:-2 --no-mbtree --qcomp 0.65 --aq-mode 3 --aq-strength 0.80 --merange 32 --ipratio 1.30 --pbratio 1.20 --psy-rd 0.95 --no-dct-decimate --ref 16 -o out2.264 -