
from decoder import AudioDecoder, init_gstreamer
from filter import Filter
from analyse import scms_from_mfcc, SCMS #, symmetric_distance

class Analyser(object):
	SAMPLING_RATE = 22050
	WINDOW_SIZE = 1024
	MEL_COEFFICIENTS = 36
	MFCC_COEFFICIENTS = 20
	SECONDS_TO_ANALYZE = 120
	
	def __init__(self):
		self.mfcc = Filter(self.WINDOW_SIZE, self.SAMPLING_RATE, self.MEL_COEFFICIENTS, self.MFCC_COEFFICIENTS)
		self.ad = AudioDecoder(self.SAMPLING_RATE, self.SECONDS_TO_ANALYZE, self.WINDOW_SIZE)
	
	def cancel_analyze(self):
		self.ad.cancel_decode()
	def analyse(self, filename):
		stftdata = self.ad.decode(filename)
		scms = scms_from_mfcc((self.mfcc * stftdata))
		return scms
	@staticmethod
	def distance(a, b):
		return a.distance(b)
		#return symmetric_distance(a, b)


if __name__ == '__main__':
	import sys
	init_gstreamer()
	#Analyser.MFCC_COEFFICIENTS = 9
	a = Analyser()
	f1 = a.analyse(sys.argv[1])
	#print f1
	f2 = a.analyse(sys.argv[2])
	#print f2
	print f1 - f2
	print f1.distance(f2)


