from os import stat
import vapoursynth as vs
import lvsfunc as lvf
import stgfunc as stg
import vsutil

core = vs.core

src = lvf.src("00000.m2ts")
src = vsutil.depth(src, 10)

final = stg.adaptive_grain(src, luma_scaling=0.9, strength=1)

#The encode is very fast because only like two filters, so I'm only splitting it into two fragments. Uncomment the fragment definition variable if you don't wanna set the var through vspipe
#fragment=1
frag_size = 73421 #or 18339
fs = (int(fragment) - 1) * frag_size
fe = fs + frag_size
chunk = final[fs:fe]
chunk.set_output(0)

#Source looks clean, and again this is just for my personal viewing, so I'm not gonna both filtering other than grain