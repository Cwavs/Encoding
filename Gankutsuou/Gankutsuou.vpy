import vapoursynth as vs
import vsutil
import EoEfunc as eoe
import fvsfunc as fvf
import havsfunc as hav
import lvsfunc as lvf
import kagefunc as kgf
import stgfunc as stg
core = vs.core

#Load Source file
src_file = "00000.m2ts"
src = lvf.src(src_file)

src = vsutil.depth(src, 16)

denoised = eoe.denoise.BM3D(src, sigma=1)

deband = fvf.GradFun3(denoised, smode=2, thr=1)

final = vsutil.depth(deband, 10)
grain = kgf.adaptive_grain(final, static=True)

#Set outputs
grain.set_output(0)
deband.set_output(1)
denoised.set_output(2)
src.set_output(3)