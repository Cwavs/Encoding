import vapoursynth as vs
import vssource as vss
from vstools import set_output
from vsutil import depth
from vsdeband import PlaceboGrain


core = vs.core

src = depth(vss.BestSource.source("E:\\fkp8nx.ogv"), 16)

def denLuma(clip: vs.VideoNode):
    #Import vsutil and vsdenoise
    from vsdenoise import BM3DCuda, Profile

    denLuma = BM3DCuda(clip).denoise(clip, sigma=100, profile=Profile.HIGH)

    #Recombine the seperated channels and return the clip
    return denLuma

deb = src.deblock.Deblock(quant=60)
den = denLuma(deb)

grn = PlaceboGrain.grain(den, strength=(5, 0))
set_output(src)
set_output(deb)
set_output(den)
set_output(grn)