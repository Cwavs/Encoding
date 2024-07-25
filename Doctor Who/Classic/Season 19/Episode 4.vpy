import vapoursynth as vs
from vsutil import depth
from stgfunc import set_output
from jvsfunc import vinverse
from havsfunc import ChangeFPS

core = vs.core

filmScenes = "[0 1272] [1414 1462] [1602 1644] [1798 1798] [63340 68952]"

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

src = core.dgdecodenv.DGSource("D:\\DOCTOR_WHO_CASTROLAVA\\BDMV\\STREAM\\00226.dgi")
src = depth(src, 16)

doubled = ChangeFPS(src, 50)
deint = src.nnedi3cl.NNEDI3CL(3)

finalDeint = core.remap.Rfs(deint, doubled, mappings=filmScenes).std.SetFieldBased(0)

den = denChroma(finalDeint)

final = depth(den, 8)
final = final.std.Crop(242, 242)

set_output(src)
set_output(finalDeint)
set_output(den)
set_output(final, False)