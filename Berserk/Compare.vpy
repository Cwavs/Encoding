import vapoursynth as vs
import stgfunc as stg

core = vs.core

source = core.lsmas.LWLibavSource("out.264").std.Trim(9506, 11506)
source.set_output(0)
crf14265 = core.lsmas.LWLibavSource("crf14.265")
stg.set_output(crf14265)
cbqpoffs = core.lsmas.LWLibavSource("cbqpoffs3.265")
stg.set_output(cbqpoffs)
