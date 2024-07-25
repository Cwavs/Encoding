import vapoursynth as vs
import lvsfunc as lvf
from vsmlrt import DPIR, DPIRModel, Backend
import vsutil

core = vs.core

core.std.LoadPlugin(path=r"chickendream.dll")

src = lvf.src("A2_t00.mkv")
src = vsutil.depth(src, 16)

den = DPIR(src.resize.Bicubic(format=vs.RGBS, matrix_in=6, transfer_in=6, primaries_in=6, range=0).std.Limiter(), strength=50, model=DPIRModel.drunet_deblocking_color, backend=Backend.ORT_CUDA()).resize.Spline16(657, src.height).std.AddBorders(left=1)

grain = den.chkdr.grain(cp=True, draft=True).resize.Bicubic(format=vs.YUV420P16, matrix=6, transfer=6, primaries=6, range=0).std.Limiter()

final = vsutil.depth(grain, 8)[0:169530]

frag_size = 84765
fs = (int(fragment) - 1) * frag_size
fe = fs + frag_size
chunk = final[fs:fe]

chunk.set_output(0)
