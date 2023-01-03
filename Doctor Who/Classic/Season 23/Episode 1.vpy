import vapoursynth as vs
import jvsfunc as jvf
from havsfunc import ChangeFPS
from vsutil import depth

core = vs.core

src = core.dgdecodenv.DGSource("D:\\Trial_of_a_time_lord_volume_1\\BDMV\\STREAM\\00021.dgi")
src = depth(src, 16)

#Create base deinterlaced pass with nnedi3
deint = src.nnedi3.nnedi3(3)
#Doubled pass to match the double rate nnedi3 pass
deobuled = ChangeFPS(src, 50)

#Split the base pass up into the desired segments and created a vinversed pass of the fade after the title sequence
title = deint[0:1756]
fade = jvf.vinverse(deobuled[1756:1794])
model = deobuled[1794:3820]
episode = deint[3820:75128]

#Combine into final deinterlaced section
finalDeint = title + fade + model + episode

final = depth(finalDeint, 8)
final = final.std.Crop()

src.set_output(0)
finalDeint.set_output(1)
final.set_output(2)