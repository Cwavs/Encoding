import vapoursynth as vs
from stgfunc import set_output

core = vs.core

src = core.dgdecodenv.DGSource("out.dgi")
src2 = core.dgdecodenv.DGSource("outb.dgi")
q60 = core.dgdecodenv.DGSource("out60.dgi")
q65 = core.dgdecodenv.DGSource("out65.dgi")
q70 = core.dgdecodenv.DGSource("out70.dgi")
q75 = core.dgdecodenv.DGSource("out75.dgi")
q80 = core.dgdecodenv.DGSource("out80.dgi")

set_output(src)
set_output(src2)
set_output(q60)
set_output(q65)
set_output(q70)
set_output(q75)
set_output(q80)