ffmpeg -i "00000 PID 1100 L+R 48 1536 DELAY 0ms.dts" -b:a 128k -c:a libopus "English Stereo.opus"
ffmpeg -i "00000 PID 1101 C+L+R+SL+SR 48 1536 DELAY 0ms.dts" -b:a 256k -ac 6 -c:a libopus "English Surround.opus"
ffmpeg -i "00000 PID 1102 L+R 48 1536 DELAY 0ms.dts" -b:a 128k -c:a libopus "English Commentary.opus"