import vapoursynth as vs
from vsutil import depth
from stgfunc import set_output
from jvsfunc import vinverse
from havsfunc import ChangeFPS

core = vs.core

filmScenes = "[0 1502] [15226 18676] [30086 36910] [38466 40442] [41252 41282] [41432 42732] [49264 53092] [62190 62666] [63104 63214] [67952 73540]"

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

src = core.dgdecodenv.DGSource("D:\\MASQUE_OF_MANDRAGORA\\BDMV\\STREAM\\00021.dgi")
src = depth(src, 16)

doubled = ChangeFPS(src, 50)
deint = src.nnedi3cl.NNEDI3CL(3)

finalDeint = core.remap.Rfs(deint, doubled, mappings=filmScenes).std.SetFieldBased(0)

den = denChroma(finalDeint)

final = depth(den, 8)
final = final.std.Crop(236, 242)

set_output(src)
set_output(finalDeint)
set_output(den)
set_output(final, False)