import vapoursynth as vs
import lvsfunc as lvf
import fvsfunc as fvf
import havsfunc as haf
import EoEfunc as eoe
import kagefunc as kgf
import awsmfunc as awf
import vsutil
from vsmlrt import DPIR, DPIRModel, Backend

core = vs.core

src_file = "Episode 4 Animation.d2v"
src = lvf.src(src_file)

dep = vsutil.depth(src, 16)
denoised = eoe.denoise.BM3D(dep, profile="np", sigma=5)
u, v = vsutil.split(src)[1:]

src.set_output(0)
denoised.set_output(1)
u.set_output(2)
v.set_output(3)