import vapoursynth as vs
from vsparsedvd import IsoFile
import vsutil

core = vs.core

apple = IsoFile(r"D:/Appleseed Disc1.ISO")

a = apple.get_title()
apple.joined_titles[0].set_output(0)