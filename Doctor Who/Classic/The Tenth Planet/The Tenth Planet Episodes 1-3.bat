vspipe "The Tenth Planet Episodes 1-3.vpy" -c y4m - | x264 --preset slow --crf 13 --tune grain --demuxer y4m --output-csp i444 -o out.264 -
vspipe "The Tenth Planet Episodes 1-3.vpy" -o 1 -c wav - | opusenc --bitrate 256 - audio.opus
vspipe "The Tenth Planet Episodes 1-3.vpy" -o 2 -c wav - | opusenc --bitrate 256 - commentary.opus