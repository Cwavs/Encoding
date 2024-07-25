import vapoursynth as vs
from stgfunc import set_output
from vsdenoise import MVTools, MVToolsPresets
from debandshit import f3kpf, f3kbilateral
import vsutil

core = vs.core

src = core.dgdecodenv.DGSource("D:/BOOGIEPOP_PHANTOM_BD1/BDMV/STREAM/00001.dgi")
src = vsutil.depth(src, 16)

cmde = MVTools(src, **MVToolsPresets.CMDE)
denCMD = cmde.degrain()

deband = vsutil.depth(f3kpf(denCMD), 8)
deband2 = vsutil.depth(f3kbilateral(denCMD), 8)

set_output(src)
set_output(denCMD)
set_output(deband)
set_output(deband2)