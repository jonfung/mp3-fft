import ffmpy
import sys

def convert(infile, outfile):
	ff = ffmpy.FFmpeg(
		inputs = {infile :None},
		outputs = {outfile :None}
	)
	ff.run()


print(sys.argv[1])

source = sys.argv[1]
dest = sys.argv[2]

convert(source, dest)
