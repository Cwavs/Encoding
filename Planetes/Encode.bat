ffmpeg -i "D:\PlanetesFrag\output.264" -f yuv4mpegpipe - | x265 --y4m --preset slow --no-rect --no-amp --no-open-gop --no-cutree --rskip 0 --ctu 64 --min-cu-size 8 --rdoq-level 2 --max-merge 5 --rc-lookahead 60 --ref 4 --bframes 16 --rd 4 --subme 5 --merange 57 --high-tier --range limited --aud --repeat-headers --cbqpoffs 1 --crqpoffs 1 --qcomp 0.70 --aq-mode 4  --aq-strength 0.75 --deblock -2:-1 --ipratio 1.30 --pbratio 1.20 --psy-rd 0.75 --psy-rdoq 1.00 --no-sao --no-strong-intra-smoothing --crf 16 - -o out.265