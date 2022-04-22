import vapoursynth as vs
import lvsfunc as lvf
import vsutil
import kagefunc as kgf
import fvsfunc as fvf
import EoEfunc as eoe
import awsmfunc as awf
core = vs.core

#Load Source file
src_file = "00000.m2ts"
src = lvf.src(src_file)

#src = awf.SelectRangeEvery(src, every=1500, length=250, offset=[15214, 18084])

src = fvf.Depth(src, 16)

y, u, v = kgf.split(src)
height = 720
width = vsutil.get_w(height)

descale = core.descale.Debilinear(y, width, height)
descaleM = fvf.DebilinearM(y, width, height)
descale = core.remap.Rfs(descale, descaleM, mappings="[0 3202] [32262 34418]")
u, v = u.resize.Bicubic(width, height, filter_param_a=0, filter_param_b=1), v.resize.Bicubic(width, height, filter_param_a=0, filter_param_b=1)
descale_catmull = kgf.join([descale, u, v])

denoised = eoe.denoise.BM3D(descale_catmull)

deband = fvf.GradFun3(denoised)

final = vsutil.depth(deband, 10)
grain = kgf.adaptive_grain(final, static=True)

#Set outputs (sending denoised, regrained and cropped for easy comparision on vspreview)
grain.set_output(0)
descale.set_output(1)
descale_catmull.set_output(2)
denoised.set_output(3)
src.set_output(4)