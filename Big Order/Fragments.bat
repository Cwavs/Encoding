for /l %%x in (30, 1, 40) do vspipe "Episode 1.vpy" -a fragment=%%x -o 5 -c y4m - | x264 --preset ultrafast --qp 0 --output-depth 10 --demuxer y4m -o "fragment%%x.264" -