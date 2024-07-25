import vapoursynth as vs
from vsparsedvd import IsoFile
import vsutil

core = vs.core

eden = IsoFile(r"D:/MANGA UK - EDEN east - D1.ISO")

a = eden.get_title(None, 0)
eden.joined_titles[0].set_output(0)