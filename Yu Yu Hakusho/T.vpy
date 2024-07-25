import vapoursynth as vs
from stgfunc import set_output
core = vs.core

src = core.dgdecodenv.DGSource("D:\\YU_YU_HAKUSHO_S1_D1\\BDMV\\STREAM\\00036.dgi")

set_output(src)