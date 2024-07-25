import vapoursynth as vs
from stgfunc import set_output
from vsutil import depth
from awsmfunc import bbmod
from vsdenoise import MVTools, MVToolsPresets, BM3DCuda, bm3d

core = vs.core

def denoiseMV(clip: vs.VideoNode):
    #Import vsutil and vsdenoise
    from vsutil import split, join, get_y

    #Create MV instance for first chroma chanel
    denChroma1 = MVTools(split(clip)[1], **MVToolsPresets.CMDE).degrain()

    #Same as above but for the second channel
    denChroma2 = MVTools(split(clip)[2], **MVToolsPresets.CMDE).degrain()

    denLuma = MVTools(get_y(clip), **MVToolsPresets.CMDE).degrain()

    #Recombine the seperated channels and return the clip
    return join([get_y(clip), denChroma1, denChroma2])


#Load in the source file and the english credits to be appended to the end.
src = core.dgdecodenv.DGSource("D://ELHAZARDOVABD1//BDMV//STREAM//00001.dgi")
credits = core.dgdecodenv.DGSource("D://ELHAZARDOVABD1//BDMV//STREAM//00005.dgi")

#Dither to 16 bits, crop and fix the dirty lines on both credits and source
src = depth(src, 16).std.Crop(238, 238, 0, 0)
src = bbmod(src, left=3, right=3)

credits = depth(credits, 16).std.Crop(238, 238, 0, 0)
credits = bbmod(credits, left=3, right=3)

#Denoise the chroma using MVTools to  obliterate chroma noise
denRef = denoiseMV(src)
den = BM3DCuda(src, sigma=[0, 3], ref=denRef, profile=bm3d.Profile.HIGH).clip

set_output(src)
set_output(denRef)
set_output(den)