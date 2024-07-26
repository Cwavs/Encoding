import vapoursynth as vs
from vssource import DGIndexNV
import itertools
from vstools import set_output

core = vs.core

src = DGIndexNV(bin_path="DGIndexNV.exe").source("E:\\Red Dwarf S1\\BDMV\\STREAM\\00002.m2ts")

def ranges(i):
    for a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]

def createDiff(clip: vs.VideoNode, cLeft: int = 0, cRight: int = 0, cTop: int = 0, cBottom: int = 0, hradius: int = 10, vradius: int = 10):
    clip = clip.std.Crop(cLeft, cRight, cTop, cBottom)

    sep = clip.std.SeparateFields().std.BoxBlur(hradius=hradius, vradius=vradius)

    f1 = sep[0::2]
    f2 = sep[1::2]

    diff = core.std.MakeDiff(f1, f2)
    diff = core.std.PlaneStats(diff, plane=0, prop="prop")
    return diff

def searchForTeleRecordedScenes(clip: vs.VideoNode, threshold: int, multiPass: bool):
    i=0
    range = []
    while i < clip.num_frames:
        frameProps = clip.get_frame(i).props
        if(float(frameProps["propMax"]) > threshold):
            print(str(i) + " might be telercorded")
            range.append(i)
        print(i)
        i=i+1
    if not multiPass:
        return list(ranges(range))
    else:
        return range

def searchForTeleRecordedScenesPass2(clip: vs.VideoNode, frames: list, threshold: int):
    range = []
    for i in frames:
        frameProps = clip.get_frame(frames[i]).props
        if(float(frameProps["propMax"]) > threshold):
            print(str(i) + " might be telercorded")
            range.append(i)
        print(i)
        i=i+1
    return list(ranges(range))

diff = createDiff(src, cLeft=238, cRight=238, hradius=5, vradius=5)
range = searchForTeleRecordedScenes(diff, 39000, True)
diff = createDiff(src, cLeft=238, cRight=238, hradius=10, vradius=10)
range = searchForTeleRecordedScenesPass2(diff, range, 40000)
print(range)
set_output(diff)