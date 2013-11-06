"""
Statistical Cluster Model Similarity class. A Gaussian representation
  of a song. The distance between two models is computed with the
  symmetrized Kullback Leibler Divergence.
"""
import numpy
from numpy import log
from decoder import AudioDecoder, init_gstreamer
from filter import Filter
import scipy.sparse

class SCMS(object):
	def __init__(self, mfcc):
		self.dim = len(mfcc)
		#print 'DIM:', self.dim, mfcc.shape
		self.mean = mfcc.mean(axis=1)
		#self.cov = numpy.cov(mfcc)
		stdev = numpy.asarray(mfcc).std(axis=1)
		self.cov = numpy.diag(stdev)
		#self.cov = scipy.sparse.dia_matrix((stdev, [0]), shape=(self.dim, self.dim)).todense()
		assert self.mean.shape == (self.dim, 1), self.mean.shape
		assert self.cov.shape == (self.dim, self.dim), self.cov.shape
	
	def __sub__(self, b):
		"""
		Kullback Leibler Divergence.
		"""
		meandiff = numpy.matrix(b.mean - self.mean)
		#print '  mean-diff:', meandiff
		#print '  dets', numpy.linalg.det(self.cov), numpy.linalg.det(b.cov)
		#print 'covariance-product:', b.invcov * self.cov
		
		#second = b.invcov * self.cov
		second = numpy.linalg.solve(b.cov, self.cov)
		#first = meandiff.T * b.invcov * meandiff
		#print b.cov.shape, meandiff.shape
		#print 'linalg.solve:', b.cov.shape, meandiff.shape
		first = numpy.linalg.solve(b.cov, meandiff)
		#print '  second', second
		#print '  first', first
		
		kl = 0.5 * (numpy.trace(second) + \
			meandiff.T * first - \
			self.dim - log(numpy.linalg.det(self.cov) / numpy.linalg.det(b.cov)))

		#print '  X', numpy.trace(second), meandiff.T * first
		#print '  X', self.dim, - log(numpy.linalg.det(self.cov) / numpy.linalg.det(b.cov))
		
		# some tolerance for rounding problems
		if kl < 0 and kl > -0.1 * self.dim: 
			kl = 0
		assert kl >= 0, kl
		return kl
	def distance(self, b):
		"""
		symmetrized Kullback Leibler Divergence
		"""
		meandiff = numpy.matrix(b.mean - self.mean)
		second = numpy.linalg.solve(b.cov, self.cov)
		first = numpy.linalg.solve(b.cov, meandiff)
		kl = (numpy.trace(second) + meandiff.T * first - self.dim) / 2.
		meandiff = numpy.matrix(self.mean - b.mean)
		second = numpy.linalg.solve(self.cov, b.cov)
		first = numpy.linalg.solve(self.cov, meandiff)
		kl += (numpy.trace(second) + meandiff.T * first - self.dim) / 2.
		if kl < 0 and kl > -0.1 * self.dim: 
			kl = 0
		assert kl >= 0, kl
		return kl
		
	def __repr__(self):
		return """SCMS(dim=%d, means=%s, cov=%s)""" % (self.dim, self.mean, repr(self.cov))

#def symmetric_distance(a, b):
#	return ((a - b) + (b - a)) / 2.


if __name__ == '__main__':
	numpy.random.seed(0)
	adata = numpy.random.multivariate_normal([0., 0], [[1., 0], [0, 1]], size=1000)
	#print 'adata:', adata
	a = SCMS(adata.T)
	#a.mean[:] = [0, 0]
	#a.cov[:,:] = [[1., 0], [0, 1]]
	print 'A:', a.mean, a.cov
	print a - a
	bdata = numpy.random.multivariate_normal([1., 1.], [[1., 0.1], [0.1, 1]], size=1000)
	b = SCMS(bdata.T)
	#b.mean[:] = [1., 1.]
	#b.cov[:,:] = [[2., 0.1], [0.1, 2]]
	print 'B:', b.mean, b.cov
	
	print b - a
	
	
