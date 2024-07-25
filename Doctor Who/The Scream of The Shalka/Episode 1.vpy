from gettext import dgettext
import vapoursynth as vs
from vsparsedvd import IsoFile, DGIndexNV
import vsutil

core = vs.core

Shalka = IsoFile(r"D:/SCREAM_OF_THE_SHALKA.ISO", DGIndexNV())


src = Shalka.get_title(0)
src.set_output(0)