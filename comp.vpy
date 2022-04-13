import vapoursynth as vs
import lvsfunc as lvf
sauce = lvf.src("Brittas.mkv")
# sauce = sauce[24:-24] # uncomment line if you clipped black frames at the start and end
enc = lvf.src("Out.mkv")
sauce.set_output(0)
enc.set_output(1)