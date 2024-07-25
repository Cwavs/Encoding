from vstools import vs, core, set_output
from vsmuxtools import Setup, src_file
from vsdenoise import MVTools, MVToolsPresets, dpir
from vsdeband import PlaceboGrain

setup = Setup("01", bdmv_dir="E:\\LE COMTE DE MONTE CRISTO VOL1\\BDMV", show_name="Gankutsuou")

sBD = src_file("E:\\LE COMTE DE MONTE CRISTO VOL1\\BDMV\\STREAM\\00000.dgi")

src = sBD.init()

deblock = dpir(src)
#denoise = MVTools(src, **MVToolsPresets.CMDE).degrain()

grain = PlaceboGrain().grain(deblock, (2, 0))

set_output(src)
set_output(deblock)
set_output(grain)