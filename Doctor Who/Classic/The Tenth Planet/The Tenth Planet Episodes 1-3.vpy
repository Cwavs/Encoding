import vapoursynth as vs
import lvsfunc as lvf
import fvsfunc as fvf
import havsfunc as haf
import EoEfunc as eoe
import kagefunc as kgf
import awsmfunc as awf
import vsutil
from vsmlrt import DPIR, DPIRModel, Backend

def trimAudioFromVideoFrames(clip, videoClip, f, l):
    fps = videoClip.fps.numerator/videoClip.fps.denominator
    fLength = f/fps
    lLength = l/fps-1
    fSample = clip.sample_rate*fLength
    lSample = clip.sample_rate*lLength
    return core.std.AudioTrim(clip, fSample, lSample)

core = vs.core

#Episode 1 Frames
# (0, 34792),
#Episode 2 Frames
# (34793, 69638),
#Episode 3 Frames
# (69639, 105000),


src_file = "VTS_02_1.d2v"
src = lvf.src(src_file)
audioFile = "VTS_02_1 T80 2_0ch 192Kbps.ac3"
audioCommentaryFile = "VTS_02_1 T81 2_0ch 192Kbps.ac3"
audio = core.bas.Source(audioFile, track=-1)
audioCommentary = core.bas.Source(audioCommentaryFile, track=-1)

audio = trimAudioFromVideoFrames(audio, src, 34793, 69638)
audioCommentary = trimAudioFromVideoFrames(audioCommentary, src, 34793, 69638)

trim = core.std.Trim(src, 34793, 69638)

deint = haf.QTGMC(trim, "Placebo")

dep = vsutil.depth(deint, 16)

#denoised = DPIR(gray, strength=5, model=DPIRModel.drunet_gray, backend=Backend.TRT())
#yuv = core.resize.Bicubic(dec, format=vs.YUV420P8, matrix=5, transfer=5, primaries=5, range=0).std.Limiter()

#mask = kgf.adaptive_grain(deint, strength=10000, static=True, show_mask=True)
#denoisedRef = haf.KNLMeansCL(deint, d=5, a=10, s=8, h=2)
denoised = eoe.denoise.BM3D(deint, sigma=20)

#denoisedFinal = core.std.MaskedMerge(denoised, denoisedRef, mask)

deband = fvf.GradFun3(denoised)

gray = core.resize.Bicubic(deband, format=vs.GRAYS, matrix_in=5, transfer_in=5, primaries_in=5, range=0).std.Limiter()

crop = core.std.Crop(gray, left=9, right=10, top=3, bottom=1)
#crop = core.fb.FillBorders(crop, left=1, top=1, bottom=1)

edge = awf.bbmod(crop, left=2, right=2, bottom=1, blur=200)

final = vsutil.depth(edge, 8)
final = kgf.adaptive_grain(final, static=True)



final.set_output(0)
audio.set_output(1)
audioCommentary.set_output(2)

#denoised.set_output(1)
#denoisedRef.set_output(2)
#deint.set_output(3)
#src.set_output(4)
#mask.set_output(5)