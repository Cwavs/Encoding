import vapoursynth as vs
import lvsfunc as lvf
import vsutil

core = vs.core

src = lvf.src("VTS_02_1.dgi")
src = src.resize.Bicubic(format=vs.GRAYS)
src = lvf.deinterlace.PARser(src, 697, lvf.types.Dar.FULL, region=lvf.types.Region.PAL)

deint = src.nnedi3.nnedi3(1)

src.set_output(0)
deint.set_output(1)