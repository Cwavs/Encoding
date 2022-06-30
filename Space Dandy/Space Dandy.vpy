import vapoursynth as vs
import lvsfunc as lvf
import vsutil
import kagefunc as kgf
import fvsfunc as fvf
import EoEfunc as eoe
import awsmfunc as awf
import vardefunc as var
core = vs.core

#Load Source file
src_file = "00000.m2ts"
src = lvf.src(src_file)

#src = awf.SelectRangeEvery(src, every=1500, length=250, offset=[15214, 18084])

src = fvf.Depth(src, 16)

src = awf.bbmod(src, top=1, bottom=1, left=1, right=1)

y, u, v = kgf.split(src)
height = 720
width = vsutil.get_w(height)

descale = core.descale.Debilinear(y, width, height)
descaleM = fvf.DebilinearM(y, width, height)
descale = core.remap.Rfs(descale, descaleM, mappings="[0 3202] [32262 34418]")
#descale = awf.bbmod(descale, top=4, bottom=4, right=4, left=4, blur=999, thresh=10)
resizeda = var.scale.nnedi3cl_double(descale)
resizedb = resizeda.resize.Bicubic(1920, 1080, filter_param_a=0, filter_param_b=0)

descaled = kgf.join([resizedb, u, v])

denoised = eoe.denoise.BM3D(descaled)

deband = fvf.GradFun3(denoised)

linemask = kgf.retinex_edgemask(src)

merged = core.std.MaskedMerge(deband, src, linemask)

final = vsutil.depth(merged, 10)
grain = kgf.adaptive_grain(final, static=True, strength=1)

#Set outputs (sending denoised, regrained and cropped for easy comparision on vspreview)
grain.set_output(0)
merged.set_output(1)
deband.set_output(2)
denoised.set_output(3)
resizedb.set_output(4)
src.set_output(5)