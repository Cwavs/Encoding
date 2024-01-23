import vapoursynth as vs
from vstools import set_output, depth, get_y
from vsscale import descale
from vskernels import RobidouxSharp

core = vs.core

src = core.dgdecodenv.DGSource("E:\\Parasyte BD-1\\BDMV\\STREAM\\00006.dgi")

src = depth(get_y(src), 16)

descaled = descale(src, height=[960], kernels=[RobidouxSharp], result=True)
rescaled = descaled.rescaled
descaled = descaled.descaled

set_output(src)
set_output(descaled)
set_output(rescaled)