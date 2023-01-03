import vapoursynth as vs
from stgfunc import set_output, adptvgrnMod
from vsutil import depth
from vsdenoise import MVTools, MVToolsPresets
from fvsfunc import GradFun3mod
from vsaa import upscaled_sraa
from kagefunc import retinex_edgemask

core = vs.core

src = core.dgdecodenv.DGSource(r"D://PROMARE//BDMV//STREAM//00011.dgi")
src = depth(src, 16)

den = MVTools(src, **MVToolsPresets.CMDE).degrain()

deband = GradFun3mod(den)

aa = upscaled_sraa(deband, rfactor=2)
aaMask = retinex_edgemask(deband)
aaFinal = core.std.MaskedMerge(deband, aa, aaMask)

final = adptvgrnMod(depth(aaFinal[0:785] + src[785:6150] + aaFinal[6150:153267], 10), strength=[5, 0])

testSeg = final[44808:46291]

set_output(src)
set_output(den)
set_output(deband)
set_output(aaFinal)
set_output(final, text=False)
set_output(testSeg, text=False)