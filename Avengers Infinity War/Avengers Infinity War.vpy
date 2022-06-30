import vapoursynth as vs
import lvsfunc as lvf
import EoEfunc as eoe
import kagefunc as kgf
import vsutil

core = vs.core

src = lvf.src("00801.m2ts")

cropped = core.std.Crop(src, top=138, bottom=138)

dep = vsutil.depth(cropped, 16)

u, v = vsutil.split(dep)[1:]
y = vsutil.get_y(dep)

denoisedUa = core.knlm.KNLMeansCL(u)
denoiseda = core.knlm.KNLMeansCL(y)
denoisedVa = core.knlm.KNLMeansCL(v)
denoisedU = eoe.denoise.BM3D(u, ref = denoisedUa, sigma=20)
denoisedUb = eoe.denoise.BM3D(u, ref = denoisedUa, sigma=1)
denoisedV = eoe.denoise.BM3D(v, ref = denoisedVa, sigma=20)
denoisedVb = eoe.denoise.BM3D(v, ref = denoisedVa, sigma=1)
denoised = eoe.denoise.BM3D(y, ref = denoiseda, sigma=20)
denoisedb = eoe.denoise.BM3D(y, ref = denoiseda, sigma=1)

mask = kgf.adaptive_grain(dep, static=True, show_mask=True, luma_scaling=3)

denoisedLa = vsutil.join([denoised, denoisedU, denoisedV])
denoisedLb = vsutil.join([denoisedb, denoisedUb, denoisedVb])

denoisedFinal = core.std.MaskedMerge(denoisedLa, denoisedLb, mask)

final = vsutil.depth(denoisedFinal, 8)

cropped.set_output(0)
denoisedFinal.set_output(1)
final.set_output(2)