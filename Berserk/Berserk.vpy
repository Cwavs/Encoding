import vapoursynth as vs
import lvsfunc as lvf
import EoEfunc as eoe
import kagefunc as kaf
import vsutil
core = vs.core

#Load Source file
src_file = "00002.m2ts"
src = lvf.src(src_file)

#Crop out the black bars
cropped = core.std.Crop(src, left = 240, right = 240)

#Create reference denoised image with KNLM
denoised_ref = core.knlm.KNLMeansCL(cropped, 10, 10, 4)
#Denoise fully with EOE's BM3D wrapper
denoised = eoe.denoise.BM3D(cropped, ref=denoised_ref, radius=2, fast=False)

#Create adaptive grain mask from the denoised version
mask = kaf.adaptive_grain(denoised, static=True, show_mask=True)

#Regrain with MaskedMerge
regrained = core.std.MaskedMerge(denoised, cropped, mask)

#Take chroma from denoised and combine it with regrained luma, Thanks Riven
u, v = vsutil.split(denoised)[1:]
regrain = vsutil.join(
[vsutil.get_y(regrained),
u,
v])

#Set outputs (sending denoised, regrained and cropped for easy comparision on vspreview
regrain.set_output(0)
regrained.set_output(1)
denoised.set_output(2)
cropped.set_output(3)