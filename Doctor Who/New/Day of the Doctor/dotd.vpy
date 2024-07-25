import vapoursynth as vs
import lvsfunc as lvf
import havsfunc as haf
import kagefunc as kgf
import EoEfunc as eoe

import vsutil

core = vs.core

src_file = "00004.m2ts"
src = lvf.src(src_file)

dep = vsutil.depth(src, 16)

u, v = vsutil.split(dep)[1:]
y = vsutil.get_y(dep)

denoisedU = core.knlm.KNLMeansCL(u)
denoiseda = core.knlm.KNLMeansCL(y)
denoisedV = core.knlm.KNLMeansCL(v)
denoisedU = eoe.denoise.BM3D(u, ref = denoisedU, sigma=20)
denoisedV = eoe.denoise.BM3D(v, ref = denoisedV, sigma=20)
denoised = eoe.denoise.BM3D(y, ref = denoiseda, sigma=20)
denoisedb = eoe.denoise.BM3D(y, ref = denoiseda, sigma=1)

mask = kgf.adaptive_grain(y, static=True, show_mask=True)
denoisedL = core.std.MaskedMerge(denoisedb, denoised, mask)

denoisedFinal = vsutil.join([denoisedL, denoisedU, denoisedV])

final = vsutil.depth(denoisedFinal, 8)

#fragment = 1
frag_size = 22987
fs = (int(fragment) - 1) * frag_size
fe = fs + frag_size
chunk = final[fs:fe]

chunk.set_output(0)
#denoisedFinal.set_output(1)
#denoisedU.set_output(2)
#denoisedV.set_output(3)
#u.set_output(4)
#v.set_output(5)
src.set_output(1)