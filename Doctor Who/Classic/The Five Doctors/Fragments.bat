for /l %%x in (9, 1, 100) do vspipe "The Five Doctors.vpy" -a fragment=%%x -c y4m - | x264 --preset ultrafast --qp 0 --demuxer y4m -o "D:\New folder (3)\fragment%%x.264" -