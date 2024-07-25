import vapoursynth as vs
from vsutil import depth

core = vs.core

src = core.dgdecodenv.DGSource("D:\\Trial_Of_A_Time_Lord_Disc_3\\BDMV\\STREAM\\00021.dgi")
src = depth(src, 16)

#No funky progressive model shots or interlaced progressive fades to worry about here, so just one deint pass for the whole thing.
deint = src.nnedi3.nnedi3(3)

final = depth(deint, 8)
final = final.std.Crop(240, 240)

src.set_output(0)
deint.set_output(1)
final.set_output(2)