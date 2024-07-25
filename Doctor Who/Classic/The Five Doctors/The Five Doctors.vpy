import vapoursynth as vs
import lvsfunc as lvf
import havsfunc as haf
from vsmlrt import DPIR, DPIRModel, Backend
import EoEfunc as eoe
import vsutil

core = vs.core

src_file = "remaster.dgi"
src = lvf.src(src_file)
src = vsutil.depth(src, 16)

interlacedScenes = "[3364 4773] [6112 9117] [12248 13295] [14656 15887] [26778 27643] [31036 31707] [42542 44059] [45088 73201] [82250 83945] [86064 95747] [99772 101903] [111594 112529] [113090 114695] [118218 120285] [121958 123583] [133836 133971] [135640 136651] [137984 145961] [150552 151879] [159528 160309] [161470 169283] [177844 178941] [185928 188077] [194088 213555] [213744 220345] [220548 223025] [223174 244449] [245652 255701] [256544 281443] [281754 298153]"

hartnellScene = "[0 1063]"

specialEffects = "[14142 14219] [14300 14359] [14410 14643] [25446 25999] [26412 26467] [26566 26773] [29454 29525] [30062 30161] [30738 31031] [42266 42501] [44856 45063] [111266 111275] [111340 111353] [111424 111435] [281444 281609]"

interlaced = core.nnedi3.nnedi3(src, 3)
specialEffect = haf.ChangeFPS(core.nnedi3.nnedi3(src, 1), 50)
prog = haf.ChangeFPS(src, 50)
hartnell = core.nnedi3.nnedi3(src, 3)

deint = core.remap.Rfs(prog, interlaced, mappings=interlacedScenes)
deint = core.remap.Rfs(deint, specialEffect, mappings=specialEffects)

deblock = DPIR(deint.resize.Bicubic(format=vs.RGBS, matrix_in=5, transfer_in=5, primaries_in=5, range=0).std.Limiter(), strength=50, model=DPIRModel.drunet_deblocking_color, backend=Backend.ORT_CUDA()).resize.Bicubic(format=vs.YUV420P16, matrix=5, transfer=5, primaries=5, range=0).std.Limiter()

denRef = core.knlm.KNLMeansCL(deblock, d=10, a=10, s=8)
den = eoe.denoise.BM3D(deblock, ref=denRef, sigma=3, profile="vn").remap.Rfs(hartnell, mappings=hartnellScene)

src.set_output(0)
deint.set_output(1)
den.set_output(2)