import vapoursynth as vs
from vsutil import depth
from stgfunc import set_output
from jvsfunc import vinverse
from havsfunc import ChangeFPS

core = vs.core

filmScenes = "[0 1480] [70730 73088]"
#My dumbass spent forever trying to work out what these were (called them confusing frames in Episode 5), and I only just fucking realised they're just PAL telecine where the film has been shot at 25fps. For anyone else who encoutners this content, I've figured the best course of action is single rate deint, double ate isn't needed as all you'll end up with is the same frame with a differnt grain pattern. Note to self: Some of the combing looks much less notable in some scenes, not sure if it is just genuinley not as noticeable, I am blind or the film for some segments survived and was rescanned for this release, not sure if this information exists,r I suspect I'd have to speak to the restoration team about this, but not sure if they'd know or be able to share it.
telecine = "[14014 14706] [14892 16004] [16230 17378] [17582 17656] [17794 19972] [23750 27932] [54810 55072] [60514 60844]"

def denChroma(clip: vs.VideoNode):
    #Import vsutil and vsdenoise
    from vsutil import split, join, get_y
    from vsdenoise import MVTools, MVToolsPresets

    #Create MV instance for first chroma chanel
    denChroma1 = MVTools(split(clip)[1], **MVToolsPresets.CMDE).degrain()

    #Same as above but for the second channel
    denChroma2 = MVTools(split(clip)[2], **MVToolsPresets.CMDE).degrain()

    #Recombine the seperated channels and return the clip
    return join([get_y(clip), denChroma1, denChroma2])\

src = core.dgdecodenv.DGSource("E:\\THE_HAND_OF_FEAR\\BDMV\\STREAM\\00023.dgi")
src = depth(src, 16)

doubled = ChangeFPS(src, 50)
deint = src.nnedi3cl.NNEDI3CL(3)
intFade = ChangeFPS(src.nnedi3cl.NNEDI3CL(1), 50)

finalDeint = core.remap.Rfs(deint, doubled, mappings=filmScenes)
finalDeint = core.remap.Rfs(finalDeint, intFade, mappings=telecine).std.SetFieldBased(0)

den = denChroma(finalDeint)

final = depth(den, 8)
final = final.std.Crop(236, 236)

set_output(src)
set_output(finalDeint)
set_output(den)
set_output(final, False)