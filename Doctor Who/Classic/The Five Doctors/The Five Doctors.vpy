import vapoursynth as vs
import lvsfunc as lvf
from lvsfunc.types import Position, Size
from typing import Tuple, List
import fvsfunc as fvf
import havsfunc as haf
import EoEfunc as eoe
import kagefunc as kgf
import awsmfunc as awf
import vardefunc as var
import rvsfunc as rvf
import vsutil
from vsmlrt import DPIR, DPIRModel, Backend

rainbowed_frames: List[Tuple[int, int, Position, Size]] = [
    (100, -1, (500, 500), (8, 8)),
    (200, 1, (300, 160), (16, 16)),
    (200, 1, (800, 300), (16, 16)),
    ]

def sqmask_rainbows(clip: vs.VideoNode, frame: int, rel_clean: int = -1,
                pos: Position = (0, 0), size: Size = (2, 2), **kwargs
                ) -> vs.VideoNode:
    """
    Simple sqmasking function for fixing rainbowing.
    Allows you to pass a relative frame using ``rel_clean`` to square mask an area.
    Follows ``BoundingBox`` logic, so check the docs for more info.
    :param clip:        Clip to process.
    :param frame:       Frame number.
    :param rel_clean:   Relative clean frame position. Relative to ``frame``.
                        For example, `rel_clean=-1` will grab the frame before it.
    :param pos:         Mask position. See ``BoundingBox``.
    :param size:        Mask size. See ``BoundingBox``.
    :param kwargs:      Additional args to pass to replace_ranges.    
    :return:            Masked clip.
    """
    from lvsfunc import replace_ranges, BoundingBox
    sqmask = BoundingBox(pos, size).get_mask(clip)
    clean = core.std.MaskedMerge(clip[frame], clip[frame+rel_clean], sqmask)
    clean = clean * clip.num_frames  # If `replace_ranges` errors, try adding `-1` behind `num_length` here.
    return replace_ranges(clip, clean, [frame], **kwargs)

def RainbowSmooth(clip, radius=3, lthresh=0, hthresh=220, mask="original"):
    core = vs.core
    
    if isinstance(mask, str):
        if mask == "original":
            mask = core.std.Expr(clips=[clip.std.Maximum(planes=0), clip.std.Minimum(planes=0)], expr=["x y - 90 > 255 x y - 255 90 / * ?", "", ""])
        elif mask == "prewitt":
            mask = core.std.Prewitt(clip=clip, planes=0)
        elif mask == "sobel":
            mask = core.std.Sobel(clip=clip, planes=0)
        elif mask == "tcanny":
            mask = core.tcanny.TCanny(clip)
        elif mask == "fast_sobel":
            import kagefunc as kage

            mask = kage.fast_sobel(clip)
        elif mask == "kirsch":
            import kagefunc as kage

            mask = kage.kirsch(clip)
        elif mask == "retinex_edgemask":
            import kagefunc as kage

            mask = kage.retinex_edgemask(clip)

    lderain = clip

    if lthresh > 0:
        lderain = clip.smoothuv.SmoothUV(radius=radius, threshold=lthresh, interlaced=False)

    hderain = clip.smoothuv.SmoothUV(radius=radius, threshold=hthresh, interlaced=False)

    if hthresh > lthresh:
        return core.std.MaskedMerge(clipa=lderain, clipb=hderain, mask=mask, planes=[1, 2], first_plane=True)
    else:
        return lderain

core = vs.core

src_file = "VTS_02_1.d2v"
src = lvf.src(src_file)

deint = haf.QTGMC(src, "Placebo")

print(deint.num_frames)

dep = vsutil.depth(deint, 16)

denoisedRef = core.knlm.KNLMeansCL(dep, d=10, a=10, s=8, h=3)
denoised = eoe.denoise.BM3D(dep, ref=denoisedRef, sigma=1)
denoised2 = eoe.denoise.BM3D(dep, ref=denoisedRef, sigma=20, profile='vn')

mask = kgf.adaptive_grain(denoised2, static=True, show_mask=True, luma_scaling=100)

denoisedFinal = core.std.MaskedMerge(denoised, denoised2, mask)

aa = lvf.aa.upscaled_sraa(denoisedFinal)

derainbow = aa

#for f in rainbowed_frames:
    #derainbow = sqmask_rainbows(aa, f[0], f[1], f[2], f[3])

crop = core.std.Crop(aa, left=10, right=8, bottom=2)

final = vsutil.depth(crop, 8)
final = kgf.adaptive_grain(final, static=True)

#fragment = 1
frag_size = 2713
fs = (int(fragment) - 1) * frag_size
fe = fs + frag_size
chunk = final[fs:fe]

chunk.set_output(0)


aa.set_output(1)
denoisedFinal.set_output(2)
dep.set_output(3)
deint.set_output(4)
src.set_output(5)
mask.set_output(6)

