import vapoursynth as vs
import lvsfunc as lvf
import stgfunc as stg
from vsmlrt import DPIR, Backend, DPIRModel
import vsutil

core = vs.core

src = lvf.src("A1_t01.mkv")
gray = src.resize.Bicubic(format=vs.GRAY8).std.Limiter()

gray.set_output(0)