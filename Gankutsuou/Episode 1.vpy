import vapoursynth as vs
from vsutil import depth
from stgfunc import set_output, adaptivegrainmod
from vsdenoise import MVTools, MVToolsPresets


core = vs.core

src = depth(core.dgdecodenv.DGSource("D:\\LE COMTE DE MONTE CRISTO VOL1\\BDMV\\STREAM\\00000.dgi"), 16)

den = MVTools(src, **MVToolsPresets.CMDE).degrain()

final = adaptivegrainmod(depth(den, 10), [5, 0])

set_output(src)
set_output(den)
set_output(final, False)