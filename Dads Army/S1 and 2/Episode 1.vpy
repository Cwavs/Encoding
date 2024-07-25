import vapoursynth as vs
from vsparsedvd import IsoFile
import vsutil

core = vs.core

dad = IsoFile(r"D:/BBCDVD1368.ISO")

src = dad.get_title()
src.set_output(0)