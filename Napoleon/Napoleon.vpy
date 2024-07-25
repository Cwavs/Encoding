import vapoursynth as vs
import rvsfunc as rvf
from lvsfunc import source as src
import vsutil

core = vs.core

actFrames = [[0, 163758], [163759, 255367], [255368, 409657], [409658, 479606]] 

#Act Clips
acts = src("D:/NAPOLEON DISC 1/BDMV/STREAM/00000.dgi")

#Finale Segments
left = src("D:/NAPOLEON DISC 1/BDMV/STREAM/00001.dgi")
center = src("D:/NAPOLEON DISC 2/BDMV/STREAM/00002.dgi").std.Crop(214, 216, 0, 0)
right = src("D:/NAPOLEON DISC 3/BDMV/STREAM/00006.dgi")

#Credits
credits = src("D:/NAPOLEON DISC 3/BDMV/STREAM/00008.dgi")

finale = core.std.StackHorizontal([left, center, right]).resize.Bicubic(format=vs.RGBS).std.Crop(431, 431, 0, 0).resize.Bicubic(format=vs.YUV420P8, matrix=1)

acts = rvf.utils.pad_to(acts.std.Crop(242, 242, 0, 0), finale.width)
credits = rvf.utils.pad_to(credits, finale.width)

movie = acts + finale + credits

#chunk = 1
chunk = int(chunk) - 1
final = movie[actFrames[chunk][0]:actFrames[chunk][1]]
final.set_output(0)