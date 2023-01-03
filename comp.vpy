import vapoursynth as vs
import lvsfunc as lvf
sauce = lvf.src("Doctor Who\Classic\The Five Doctors\VTS_02_1.dgi")
# sauce = sauce[24:-24] # uncomment line if you clipped black frames at the start and end
enc = lvf.src("Doctor Who\Classic\The Five Doctors/remaster.dgi")
sauce.set_output(0)
enc.set_output(1)