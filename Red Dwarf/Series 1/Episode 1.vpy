import vapoursynth as vs
from vsutil import depth
from vstools import set_output, change_fps as ChangeFPS
from vsdeband import PlaceboGrain as grain

core = vs.core

intro = "[0 0]"
singleRate = "[0 0]"

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

def denLuma(clip: vs.VideoNode):
    #Import vsutil and vsdenoise
    from vsutil import split, join, get_y
    from vsdenoise import MVTools, MVToolsPresets

    #Create MV instance for first chroma chanel
    denChroma1 = MVTools(split(clip)[1], **MVToolsPresets.CMDE).degrain()

    #Same as above but for the second channel
    denChroma2 = MVTools(split(clip)[2], **MVToolsPresets.CMDE).degrain()

    denLuma = MVTools(split(clip)[0], **MVToolsPresets.CMDE).degrain()

    #Recombine the seperated channels and return the clip
    return join([denLuma, denChroma1, denChroma2])

src = core.dgdecodenv.DGSource("E:\\Red Dwarf S1\\BDMV\\STREAM\\00002.dgi")
src = depth(src, 16)

doubled = ChangeFPS(src, 50)
deint = src.nnedi3cl.NNEDI3CL(3)
intFade = ChangeFPS(src.nnedi3cl.NNEDI3CL(1), 50)

finalDeint = core.remap.Rfs(deint, doubled, mappings=intro)
finalDeint = core.remap.Rfs(finalDeint, intFade, mappings=singleRate).std.SetFieldBased(0)

#den = denChroma(finalDeint)
#denL = denLuma(finalDeint)

#finalDen = core.remap.Rfs(den, denL, mappings=intro)

#noise = grain(finalDen, luma_scaling=0, strength=[100, 0])

#noisedIntro = core.remap.Rfs(finalDen, noise, mappings=intro)

#final = depth(noisedIntro, 8)
#final = final.std.Crop(244, 240, 2, 4)

set_output(src)
set_output(deint)
#set_output(finalDen)
#set_output(noisedIntro)
#set_output(final, False)