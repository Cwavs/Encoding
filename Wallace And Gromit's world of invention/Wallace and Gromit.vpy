import vapoursynth as vs
import lvsfunc as lvf
import havsfunc as haf
import fvsfunc as fvf
core = vs.core

#Load Source file
src_file = "VTS_01_1.d2v"
src = lvf.src(src_file)

#Deinterlace
deint = haf.QTGMC(src, "Placebo", TFF=True)

deint = fvf.Depth(deint, 16)

#Set outputs
src.set_output(0)
deint.set_output(1)