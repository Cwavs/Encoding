import vapoursynth as vs
import lvsfunc as lvf
import awsmfunc as aws
import vsutil

src = lvf.src("00023.m2ts")
src = src.resize.Bicubic(format=vs.GRAY8)

crop = src.std.Crop(231, 231, 0, 0)
edge = aws.bbmod(crop, left=3, right=4, blur=999)

src.set_output(0)
crop.set_output(1)
edge.set_output(2)