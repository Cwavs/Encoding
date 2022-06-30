import vapoursynth as vs
import lvsfunc as lvf
import havsfunc as haf
import fvsfunc as fvf
import EoEfunc as eoe
import awsmfunc as awf
import kagefunc as kaf
import vsutil
from vsmlrt import DPIR, DPIRModel, Backend

core = vs.core

# (0,1276),
# (1277,6766),
# (6767,12163),
# (12164,17661),
# (17662,23172),
# (23173,28632)

#Load Source file
src_file = "VTS_10_1.d2v"
src = lvf.src(src_file)

print(src)

op = core.std.Trim(src, 0, 1276)
episode = core.std.Trim(src, 6767,12163)
combine = op + episode

#Deinterlace
deint = haf.QTGMC(combine, "Placebo")

rgb = core.resize.Bicubic(deint, format=vs.RGBS, matrix_in=5, transfer_in=5, primaries_in=5, range=0).std.Limiter()
dec = DPIR(rgb, strength=5, model=DPIRModel.drunet_color, backend=Backend.ORT_CUDA())
dec = core.resize.Bicubic(dec, format=vs.YUV420P8, matrix=5, transfer=5, primaries=5, range=0).std.Limiter()

dec = fvf.Depth(dec, 16)

crop = core.std.Crop(dec, left=10, right=8, top=2)
crop = core.fb.FillBorders(crop, bottom=1, top=1)

edge = awf.bbmod(crop, left=6, top=4, blur=999)

final = fvf.Depth(edge, 8)
final = kaf.adaptive_grain(final, strength=0.4, static=True)

#Set outputs
final.set_output(0)
dec.set_output(1)
src.set_output(2)