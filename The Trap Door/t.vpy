import vapoursynth as vs
import lvsfunc as lvf
core = vs.core

src = lvf.src("VTS_10_1.d2v")

src = core.std.Trim(src, 9062, 9187)

src.set_output(0)