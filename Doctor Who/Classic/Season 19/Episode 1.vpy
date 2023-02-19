import vapoursynth as vs
from vsutil import depth
from stgfunc import set_output
from havsfunc import ChangeFPS

core = vs.core

filmScenes = "[3116 4334] [4840 11712] [12492 13440] [13832 13860] [14088 15764] [16474 16892] [69082 72858]"
vfxScenes = "[4334 4470] [4526 4654] [4706 4838] [13888 14086]"

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

src = core.dgdecodenv.DGSource("D:\\DOCTOR_WHO_CASTROLAVA\\BDMV\\STREAM\\00160.dgi")
src = depth(src, 16)

doubled = ChangeFPS(src, 50)

deint = src.nnedi3cl.NNEDI3CL(3)

finalDeint = core.remap.Rfs(deint, doubled, mappings=filmScenes)
finalDeint = core.remap.Rfs(finalDeint, deint, mappings=vfxScenes)

den = denChroma(finalDeint)

final = depth(den, 8)
final = final.std.Crop(242, 242)

set_output(src)
set_output(finalDeint)
set_output(den)
set_output(final, False)