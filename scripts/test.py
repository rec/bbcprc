"""
Merges many .WAV files into one great big one and keeps track of the sample
offset for each one.
"""

import wave

FILE = '/Volumes/bbcbbc/bbcprc/source/00008000.wav'

with open(FILE, 'rb') as fp1:
    with wave.open(fp1) as fp2:
        print(fp1.tell(), fp2.tell())
        print(fp2.readframes(1))
        print(fp1.tell(), fp2.tell())
        print(fp2.readframes(2))
        print(fp1.tell(), fp2.tell())
        print(fp2.readframes(100))
        print(fp1.tell(), fp2.tell())
