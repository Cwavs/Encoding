from vstools import vs, core, set_output
from vsmuxtools import Setup, src_file

setup = Setup("01", bdmv_dir="E:\\Parasyte BD-1\\BDMV", show_name="Parasyte: The Maxim")

sBD = src_file("E:\\Parasyte BD-1\\BDMV\\STREAM\\00006.dgi")

src = sBD.init()
aSrc = sBD.get_audio()

set_output(src)