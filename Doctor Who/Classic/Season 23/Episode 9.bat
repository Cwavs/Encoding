vspipe "Episode 9.vpy" -o 2 -c y4m - | x264 --demuxer y4m --preset veryslow --level 41 --me umh --rc-lookahead 250 --profile high --crf 16 --deblock -2:-2 --no-mbtree --qcomp 0.65 --aq-mode 2 --aq-strength 0.80 --merange 32 --ipratio 1.30 --pbratio 1.20 --psy-rd 0.95 --no-dct-decimate --ref 16 -o out.264 - 