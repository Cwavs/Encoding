import vapoursynth as vs
import lvsfunc as lvf
sauce = lvf.src("Gankutsuou/00002.m2ts")
# sauce = sauce[24:-24] # uncomment line if you clipped black frames at the start and end
enc = lvf.src("Gankutsuou/out.265")
sauce.set_output(0)
enc.set_output(1)