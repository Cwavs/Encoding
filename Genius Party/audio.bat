ffmpeg -i 00000.m2ts -c:a libopus -b:a 256k -ac 6 -af channelmap=channel_layout=5.1 -apply_phase_inv 0 out.opus