import vapoursynth as vs
from vstools import set_output
from vskernels import Bilinear
from getfnative import descale_cropping_args

core = vs.core

src = core.dgdecodenv.DGSource("E:\\Hellsing_Ultimate_1-4_Disc1\\BDMV\\STREAM\\00008.dgi")

dArg = descale_cropping_args(src, 719.85, 1920, 1080)

descale = Bilinear.descale(src, **dArg)

up = desc

set_output(src)
set_output(descale)