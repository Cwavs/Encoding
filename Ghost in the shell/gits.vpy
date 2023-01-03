import vapoursynth as vs
import lvsfunc as lvf
import EoEfunc as eoe
from vsmlrt import DPIR, DPIRModel, Backend
import havsfunc as haf
import stgfunc as stg
import awsmfunc as aws
import vsutil

core = vs.core

src = lvf.src("VTS_01_12.dgi")
src = vsutil.depth(src, 16)

#Denoise the clip
#denref = haf.KNLMeansCL(comb, d=0, a=10, s=2)
#den = eoe.denoise.BM3D(comb, ref=denref, profile="high")
den = DPIR(src.resize.Bicubic(format=vs.RGBS, matrix_in=5, transfer_in=5, primaries_in=5, range=0).std.Limiter(), strength=5, model=DPIRModel.drunet_color, backend=Backend.ORT_CUDA()).resize.Bicubic(format=vs.YUV420P16, matrix=5, transfer=5, primaries=5, range=0).std.Limiter()

#Generate brightness mask and mergethe grain back on based on the mask
#mask = stg.adaptivegrainmod(comb, show_mask=True)
#regrain = core.std.MaskedMerge(den, comb, mask)

#Merge the denoised chroma into grained luma
#u, v = vsutil.split(den)[1:]
#regrained = vsutil.join([vsutil.get_y(regrain), u, v])

crop = aws.bbmod(den.std.Crop(0, 0, 2, 2), bottom=3, right=2)

final = vsutil.depth(crop, 10)
final = stg.adaptivegrainmod(final, strength=[1,0], luma_scaling=0, static=True)

#fragment=1
frag_num = 3
frag_size = 39968
fs = (int(fragment) - 1) * frag_size
fe = fs + frag_size
chunk = final[fs:fe]

chunk.set_output(0)