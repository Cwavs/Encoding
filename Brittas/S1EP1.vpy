from turtle import back
import vapoursynth as vs
from vsparsedvd import IsoFile
from vsmlrt import DPIR, Backend, DPIRModel
import vsutil
import EoEfunc as eoe

core = vs.core

brittas = IsoFile(r"D:/Brit S1 DVD9.ISO")

src = brittas.get_title(0)
src = vsutil.depth(src, 16)

#deinterlace
deint = src.nnedi3.nnedi3(field=3)

#Honestly I have no fucking clue whats going on with this video, my best guess is they're either really badly digitised already bad tapes, or they took the earlier vhs release, and digitised that, I have no explination for most of the artifacting here.
final = deint.std.Crop(4, 8, 0, 0)
final = vsutil.depth(final, 10)

final.set_output(0)