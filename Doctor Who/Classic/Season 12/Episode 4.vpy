import vapoursynth as vs
from vsutil import depth
from stgfunc import set_output, bbmod_fast

core = vs.core

def denChroma(clip: vs.VideoNode):
    #Import vsutil and vsdenoise
    from vsutil import split, join, get_y
    from vsdenoise import MVTools, MVToolsPresets

    #Create MV instance for first chroma chanel
    denChroma1 = MVTools(split(clip)[1], **MVToolsPresets.CMDE).degrain()

    #Same as above but for the second channel
    denChroma2 = MVTools(split(clip)[2], **MVToolsPresets.CMDE).degrain()

    #Recombine the seperated channels and return the clip
    return join([get_y(clip), denChroma1, denChroma2])

src = core.dgdecodenv.DGSource("D:\\Doctor_Who_Robot\\BDMV\\STREAM\\00024.dgi")
src = depth(src, 16)

deint = src.nnedi3cl.NNEDI3CL(3)
den = denChroma(deint)

final = depth(den, 8)
final = final.std.Crop(244, 244)

set_output(src)
set_output(deint)
set_output(den)
set_output(final, False)