import vapoursynth as vs
from havsfunc import ChangeFPS
from vsutil import depth
from jvsfunc import vinverse

core = vs.core

src = core.dgdecodenv.DGSource("D:\\Trial_Of_A_Time_Lord_Disc_2\\BDMV\\STREAM\\00021.dgi")
src = depth(src, 16)

#Looks like we got a funky model shot, this time with two interlaced fades funnn
deint = src.nnedi3.nnedi3(3)
#Doubled pass to match the double rate nnedi3 pass
doubled = ChangeFPS(src, 50)

title = deint[0:1840]
fade = vinverse(doubled[1840:1890])
model = doubled[1890:2382]
fade2 = vinverse(doubled[2382:2424])
episode = deint[2424:74302]

final = depth(title + fade + model + fade2 + episode, 8)
final = final.std.Crop(240, 240)

src.set_output(0)
deint.set_output(1)
final.set_output(2)