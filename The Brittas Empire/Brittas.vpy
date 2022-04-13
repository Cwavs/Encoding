import vapoursynth as vs
import lvsfunc as lvf
import havsfunc as haf
import awsmfunc as aws
from vsmlrt import DPIR, DPIRModel, Backend

core = vs.core

#Load Source file
src_file = "Brittas.mkv"
src = lvf.src(src_file)
#src = core.std.SetFrameProp(src, prop="_Matrix", intval=10)
print(src)

#Deinterlace
deint = haf.QTGMC(src, "Placebo")

#Deblock
edgeclean = haf.EdgeCleaner(deint, strength=30, rmode=17)
rgb = core.resize.Bicubic(edgeclean, format=vs.RGBS, matrix_in=5, transfer_in=5, primaries_in=5, range=0).std.Limiter()
dec = DPIR(rgb, strength=50, model=DPIRModel.drunet_deblocking_color, backend=Backend.ORT_CUDA())
dec = core.resize.Bicubic(dec, format=vs.YUV420P8, matrix=5, transfer=5, primaries=5, range=0).std.Limiter()

sharp = core.warp.AWarpSharp2(dec, planes=[1, 2], cplace="mpeg2")

sharp.set_output(0)
deint.set_output(1)
src.set_output(2)