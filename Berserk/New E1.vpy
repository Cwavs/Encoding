from typing import final
from EoEfunc import denoise
import vapoursynth as vs
import awsmfunc as awf
from kagefunc import retinex_edgemask as retinexEdge
from stgfunc import adaptivegrainmod as adaptiveGrain
import EoEfunc as eoe
import vsutil

core = vs.core

##Load clip and basic processes
#Using best source to open the clip because lvf.src is currently broken due to vs-package updates
src = core.bs.VideoSource("D:\\BERSERK_SERIES_DISC_1\\BDMV\\STREAM\\00002.m2ts", hwdevice="d3d11va")
#Dithering to 32 bits for denoising.
src = vsutil.depth(src, 16)
#Cropping out the black bars and fixing the slight dirty lines on the edges of the frame.
crop = awf.bbmod(src.std.Crop(240, 240, 0, 0), 0, 0, 1, 1, blur=100)

##Denoising and graining
#Create a line mask to avoid denoising the lines into being smooth
lineMask = retinexEdge(crop)
#Denoised with BM3D, converting rgb because weird chroma grain or smth, idk Riven's explination kinda washed over me
denoised = denoise.BM3D(crop.resize.Bicubic(format=vs.RGB24), sigma=20, profile="np").resize.Bicubic(format=vs.YUV420P16, matrix=1)
#Merge the line mask in
finalDenoised = core.std.MaskedMerge(denoised, crop, lineMask)
#Get the Luma and use chickendream to generate grain, only graining the luma to avoid chroma grain. This is very slow, I'll probably replace it with adaptvie grain mod or something
#noisedLuma = vsutil.get_y(finalDenoised).chkdr.grain(0)
noised = adaptiveGrain(finalDenoised, [20, 0])

#Get denoised chroma channels
#u, v = vsutil.split(finalDenoised)[1:]
#Merge Grained luma into the denoised chroma, creating a final grained version.
#noised = vsutil.join([noisedLuma, u, v])

final = vsutil.depth(noised, 10)

final.set_output(0)

#src.set_output(0)
#crop.set_output(1)
#denoised.set_output(2)
#finalDenoised.set_output(3)
#noised.set_output(4)