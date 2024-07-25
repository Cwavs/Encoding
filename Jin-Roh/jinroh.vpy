from lvsfunc.kernels import Catrom
import vapoursynth as vs
import lvsfunc as lvf
import kagefunc as kgf
import EoEfunc as eoe
import awsmfunc as awf
from vskernels import kernels
import vsutil

core = vs.core

#Load source file and dither to 16 bits
src = lvf.src("00000.m2ts")
src = vsutil.depth(src, 16)

#Source is (probably) native 1080, so no need to descale (lets go), moving straight onto denoising
#Use BM3D with vn profile seems to do pretty good
denoised = eoe.denoise.BM3D(src, sigma=30, profile="vn")

#Using kagefunc to basically generate a brightness mask for regraining the darker areas (where grain is going to be most useful)
grnmsk = kgf.adaptive_grain(denoised, static=True, show_mask=True, strength=1, luma_scaling=20)
#Merge the grain back into the denoised version, pretty self explanatory
regrained = core.std.MaskedMerge(denoised, src, grnmsk)

#Take the regrained luma and merge it with the denoised chroma to eliminate chroma noise (Thanks Riven)
u, v = vsutil.split(denoised)[1:]
regrain = vsutil.join(
[vsutil.get_y(regrained),
u,
v])

#Shift the image up one to allow for proper cropping of the borders
shifted = Catrom().scale(regrain, 1920, 1080, shift=(1, 0))
#Crop out the top and bottom black borders
crop = core.std.Crop(shifted, top=18, bottom=20)

#Fix some small dirty lines that appear in some scenes
dirt = awf.bbmod(crop, top=2, bottom=4, left=1, right=2)

#Dither back to 10 bit
final = vsutil.depth(dirt, 10)

#Split output up into various chunks for filtering (comment out the fragment variable to modify it in command with vspipe)
fragment=1
frag_size = 6113 #or 18339
fs = (int(fragment) - 1) * frag_size
fe = fs + frag_size
chunk = final[fs:fe]

#Set outputs
chunk.set_output(0)

final.set_output(1)
denoised.set_output(2)
src.set_output(3)
#Overall source looks pretty good, there might be some aliasing issues, but they probably won't bother me too much which is who this encode is for.