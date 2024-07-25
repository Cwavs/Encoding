import vapoursynth as vs
from stgfunc import set_output, adaptivegrainmod as grain
from vsdenoise import MVTools, MVToolsPresets, BM3DCuda, bm3d
from kagefunc import inverse_scale
from vodesfunc import Waifu2x_Doubler
from vsutil import depth

credits = "[264 383] [519 694] [723 970] [1191 1267] [1274 1448] [1632 1713] [1831 1928] [2080 2165] [3175 3380] [33928 34429] [34670 34789]"

core = vs.core

src = depth(core.dgdecodenv.DGSource("D:\\BIG ORDER\\BDMV\\STREAM\\00000.dgi"), 32)

descaled = inverse_scale(src, 1280, 720, "bicubic", b=0, c=1, mask_detail=True, descale_mask_zones=credits)

den = BM3DCuda(descaled, 3, profile=bm3d.Profile.HIGH).final(descaled, ref=MVTools(descaled, **MVToolsPresets.CMDE).degrain())

upscale = depth(Waifu2x_Doubler(False).double(den), 10).resize.Spline36(1920, 1080)

final = grain(upscale, strength=[10, 0], luma_scaling=1)

#frag_size = 871 #40 Fragments
#fs = (int(fragment) - 1) * frag_size
#fe = fs + frag_size
#chunk = final[fs:fe]

set_output(src)
set_output(descaled)
set_output(den)
set_output(upscale)
set_output(final, False)
#set_output(chunk, False)