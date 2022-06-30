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

dep = vsutil.depth(src, 16)

edge = awf.bbmod(dep, bottom=5, left=4, right=7)

denoisedRef = core.knlm.KNLMeansCL(edge)
denoised = eoe.denoise.BM3D(edge, ref=denoisedRef, sigma=1, profile="high")

aa = lvf.aa.upscaled_sraa(denoised)
aaMask = kgf.retinex_edgemask(denoised)

aaMasked = core.std.MaskedMerge(denoised, aa, aaMask)

final = vsutil.depth(aaMasked, 8)
final = kgf.adaptive_grain(final, static=True)

frag_size = 8996
fs = (int(fragment) - 1) * frag_size
fe = fs + frag_size
chunk = final[fs:fe]

#Set outputs
chunk.set_output(0)

#final.set_output(0)
#denoised.set_output(1)
#aa.set_output(2)
#aaMasked.set_output(3)
#edge.set_output(4)
#dep.set_output(5)
#src.set_output(6)

#4297