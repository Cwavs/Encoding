vspipe "Episode 1.vpy" -o 4 -c y4m - | x264 --demuxer y4m --preset placebo --level 41 --me umh --rc-lookahead 250 --profile high --crf 16 --deblock -2:-2 --no-mbtree --qcomp 0.65 --aq-mode 2 --aq-strength 0.80 --merange 32 --ipratio 1.30 --pbratio 1.20 --psy-rd 0.95 --no-dct-decimate --ref 16 -o out.264 -
ffmpeg -i "E:\DOCTOR_WHO_BATTLEFIELD\BDMV\STREAM\00021 PID 1100 L+R 48 1536 DELAY 0ms.dts" -b:a 320k -c:a libopus "English Stereo.opus"
ffmpeg -i "E:\DOCTOR_WHO_BATTLEFIELD\BDMV\STREAM\00021 PID 1102 L+R 48 1536 DELAY 0ms.dts" -b:a 320k -c:a libopus "English Soundtrack.opus"
ffmpeg -i "E:\DOCTOR_WHO_BATTLEFIELD\BDMV\STREAM\00021 PID 1101 C+L+R+SL+SR 48 1536 DELAY 0ms.dts" -ac 6 -b:a 320k -c:a libopus "English Surround.opus"
ffmpeg -i "E:\DOCTOR_WHO_BATTLEFIELD\BDMV\STREAM\00021 PID 1103 L+R 48 1536 DELAY 0ms.dts" -b:a 320k -c:a libopus "English Commentary.opus"
