import vapoursynth as vs
import lvsfunc as lvf
import EoEfunc as eoe
import kagefunc as kaf
import awsmfunc as awf
import fvsfunc as fvf
import vsutil
core = vs.core

#Load Source file
src_file = "00002.m2ts"
src = lvf.src(src_file)

src = vsutil.depth(src, 16)

#Create reference denoised image with KNLM
#denoised_ref = core.knlm.KNLMeansCL(src)
#Denoise with EOE's BM3D wrapper
denoised = eoe.denoise.BM3D(src, profile="np", sigma=10)

u, v = vsutil.split(src)[1:]

u2 = eoe.denoise.BM3D(u, sigma=100, profile="np")
v2 = eoe.denoise.BM3D(v, sigma=100, profile="np")

denoisedFinal = vsutil.join([vsutil.get_y(denoised), u2, v2])

#Crop out the black bars
cropped = core.std.Crop(denoisedFinal, left = 240, right = 240)

edge = awf.bbmod(cropped, left=1, right=1, bottom=1, top=1)

final = vsutil.depth(edge, 8)

#Set outputs (sending denoised, regrained and cropped for easy comparision on vspreview)
final.set_output(0)
#denoisedFinal.set_output(1)
#denoised.set_output(2)
#denoised_ref.set_output(3)
#src.set_output(4)
#u.set_output(5)
#v.set_output(6)
#u2.set_output(7)
#v2.set_output(8)