
import ctypes
from ctypes import cdll, c_int, c_void_p, c_float, create_string_buffer, byref, cast, POINTER
lib = cdll.LoadLibrary('libmirageaudio.so')
lib.mirageaudio_decode.restype = ctypes.POINTER(ctypes.c_float)
import numpy
#import numpy.ndarray.ctypes

def init_gstreamer(argc = 0, argv = 0):
	return lib.gst_init(argc, argv)

class AudioDecoder(object):
	def __init__(self, rate, seconds, winsize):
		self.ptr = lib.mirageaudio_initialize(c_int(rate), c_int(seconds), c_int(winsize))
		#print 'init done'
	
	def to_array(self, data, frames, size):
		# TODO: direct access would be faster, but this does not work yet
		#       following advice from https://stackoverflow.com/questions/4355524/getting-data-from-ctypes-array-into-numpy
		#buffer = numpy.core.multiarray.int_asbuffer(
		#	ctypes.addressof(data.contents),
		#	numpy.dtype(float).itemsize * (size * frames))
		#print 'itemsize:', numpy.dtype(float).itemsize, size, frames
		#buffer_from_memory = ctypes.pythonapi.PyBuffer_FromMemory
		#buffer_from_memory.restype = ctypes.py_object
		#buffer = buffer_from_memory(data, numpy.dtype(float).itemsize * size * frames)
		
		arr = numpy.array([[data[i * frames + j] for i in range(size)] for j in range(frames)])
		#print arr2.shape
		#arr = numpy.ctypeslib.as_array((c_float * size * frames).from_address(ctypes.addressof(data)))
		#arr = numpy.frombuffer(buffer, float)
		#print arr.shape
		#arr = numpy.array([[arr[i * frames + j] for i in range(size)] for j in range(frames)])
		#arr = numpy.array(cast(data, c_float * (size * frames)))
		#numpy.testing.assert_almost_equal(arr, arr2)
		return arr
	def decode(self, filename):
		frames = c_int(0)
		size = c_int(0)
		ret = c_int(0)
		
		data = lib.mirageaudio_decode(self.ptr, create_string_buffer(filename), byref(frames), byref(size), byref(ret))
		
		if ret.value == -1:
			raise Exception("Decoding failed")
		elif ret.value == -2:
			raise Exception("Decoding cancelled")
		elif frames <= 2 or size <= 0:
			raise Exception("No data found")
		
		#print 'mirage decoded {} frames of size {}. Return value {}'.format(frames.value, size.value, ret.value)
		
		frames = frames.value
		size = size.value
		# Sort the frames by total energy (frame selection)
		# data is (size, frames) big, floats
		# sum across to get total energy in frame
		arr = self.to_array(data, frames, size)
		sums = arr.sum(axis=1)
		pos = numpy.argsort(sums)
		copyframes = frames / 2
		stft = numpy.matrix(arr[pos[:copyframes],:]).transpose()
		return stft
	
	def cancel_decode(self):
		lib.mirageaudio_canceldecode(self.ptr)
	
	def __del__(self):
		#print 'destroying!'
		lib.mirageaudio_destroy(self.ptr)
		self.ptr = None

if __name__ == '__main__':
	import sys
	init_gstreamer()
	# make sure we have input
	if len(sys.argv) < 2:
		print 'Usage: %s <filename>' % sys.argv[1]
		sys.exit(-1)
	filename = sys.argv[1]
	dec = AudioDecoder(11025, 135, 512)
	dec.decode(filename)
	 

