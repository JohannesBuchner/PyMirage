import numpy
from numpy import linspace, arange, log, zeros, cos, transpose, pi, logical_and, log10
import scipy.sparse
import tempfile

def gen_mfcc_filters(samplingrate, winsize, numfilters, nummfccs):
	# Precompute the MFCC filterweights and DCT.
	# Adopted from Malcolm Slaneys mfcc.m, August 1993
	# Mirage uses filters computed by the following command in octave 3.0
	#     as of August 26th, 2008
	#     writefilters(22050, 1024, 36, 20, 'dct.filter', 'filterweights.filter');
	#
	# see http://www.ee.columbia.edu/~dpwe/muscontent/practical/mfcc.m

	fft_freq = linspace(0, samplingrate/2, winsize/2 + 1)
	f = arange(20, samplingrate/2 + 1)
	mel = log(1 + f/700.) * 1127.01048
	m_idx = linspace(1, mel.max(), numfilters+2)
	f_idx = numpy.array([numpy.abs(mel - m_idx[i]).argmin() for i in range(numfilters+2)])

	freqs = f[f_idx]
	lo = freqs[:numfilters]
	ce = freqs[1:numfilters+1]
	up = freqs[2:numfilters+2]

	# filters outside of spectrum
	idx = numpy.arange(numfilters)[ce <= samplingrate/2][-1]
	numfilters = min(idx + 1, numfilters)
	
	mfcc_filterweights = zeros((numfilters, winsize/2 + 1))
	triangleh = 2. / (up - lo)

	for i in range(1, numfilters):
		lovals = triangleh[i] * (fft_freq - lo[i]) / (ce[i] - lo[i])
		mfcc_filterweights[i,:] += numpy.where(logical_and(fft_freq > lo[i], fft_freq <= ce[i]), lovals, 0)
		upvals = triangleh[i] * (up[i] - fft_freq) / (up[i] - ce[i])
		mfcc_filterweights[i,:] += numpy.where(logical_and(fft_freq > ce[i], fft_freq <  up[i]), upvals, 0)
	
	dct = 1/(numfilters/2)**0.5 * cos(arange(nummfccs).reshape((-1, 1))) * (2*(arange(numfilters).reshape((1, -1))+1) * pi/2/numfilters)
	dct[0,:] *= 2**0.5 / 2
	return dct, mfcc_filterweights

class Filter(object):
	def __init__(self, winsize, srate, filters, cc):
		dct, filterWeights = gen_mfcc_filters(srate, winsize, filters, cc)
		self.filterWeights = scipy.sparse.csr_matrix(filterWeights)
		self.dct = dct
	def __mul__(self, m):
		#print 'multiplying:', m.shape, 'with', self.filterWeights.shape
		a = self.filterWeights * m
		#print 'multiplying:', a.shape
		#mel = numpy.zeros_like(a)
		#mel[a >= 1] = 10 * log10(a[a >= 1])
		mel = numpy.where(a < 1, 0, 10 * log10(a))
		#print 'multiplying:', mel.shape, self.dct.shape
		return self.dct * mel

if __name__ == '__main__':
	a, b = gen_mfcc_filters(22050, 1024, 36, 20)
	print a, b
	print b.shape, b.size, (b == 0).sum()
	indices = [(i, j) for i in range(b.shape[0]) for j in range(b.shape[1]) if b[i,j] != 0]
	print indices, len(indices), b.size
	#import matplotlib.pyplot as plt
	#plt.imshow(b, aspect='auto', interpolation='none')
	#plt.show()
	#print indices[b == 0]
	print numpy.diag(b), (numpy.diag(b) == 0).sum()





