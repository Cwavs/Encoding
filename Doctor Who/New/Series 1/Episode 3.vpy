import vapoursynth as vs
from vsutil import depth
from vstools import set_output, get_y
from vsdeband import PlaceboGrain as grain
from rekt.rektlvls import rektlvls

core = vs.core

intro = "[2671 3701] [66173 67299]"

def denLuma(clip: vs.VideoNode):
    #Import vsutil and vsdenoise
    from vsutil import split, join
    from vsdenoise import MVTools, MVToolsPresets

    #Create MV instance for first chroma chanel
    denChroma1 = MVTools(split(clip)[1], **MVToolsPresets.CMDE).degrain()

    #Same as above but for the second channel
    denChroma2 = MVTools(split(clip)[2], **MVToolsPresets.CMDE).degrain()

    denLuma = MVTools(split(clip)[0], **MVToolsPresets.CMDE).degrain()

    #Recombine the seperated channels and return the clip
    return join([denLuma, denChroma1, denChroma2])

src = depth(core.dgdecodenv.DGSource("E:\\DOCTOR_WHO_S1D1\\BDMV\\STREAM\\00148.dgi"), 16)

deComb = src.nnedi3cl.NNEDI3CL(1)

#Alot of the darker scenes have some combing and VFX shots are interlaced so I decided it wasn't worth scene filtering and to just single rate the entire thing.

#Theres some blocking and chroma noise from the compression of already fairly bad noise due to this being a Betamax show.
den = denLuma(deComb)

dirtyLines = rektlvls(den.std.Crop(24, 24, 2, 0), colnum=[0, 1, 2, 3, 4, 5, 1866, 1867, 1868, 1869, 1870, 1871], colval=[80, 63, 43, 25, 11, 4, 2, 8, 20, 35, 55, 74], rownum=[0, 1, 2, 1073, 1074, 1075, 1076], rowval=[69, 15, -3, -6, -10, 10, 29])

#Apply some graining to cover for me being a terrible encoder
grainedIntro = grain(strength=(2, 0), luma_scaling=0).grain(dirtyLines)
grained = grain(strength=(0.5, 0), luma_scaling=50).grain(dirtyLines)

finalGrained = core.remap.Rfs(grained, grainedIntro, mappings=intro)

final = depth(finalGrained, 8)

set_output(src)
set_output(deComb)
set_output(den)
set_output(dirtyLines)
set_output(grained)
set_output(final)