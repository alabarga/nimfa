"""
    #####################
    Smf (``models.smf``)
    #####################
"""

import nimfa.utils.utils as utils
from nimfa.utils.linalg import *


class Smf(object):

    """
    This class defines a common interface / model to handle standard MF models in
    a generic way.
    
    It contains definitions of the minimum set of generic methods that are used in 
    common computations and matrix factorizations. Besides it contains some quality
    and performance measures about factorizations.
    """

    def __init__(self, params):
        self.__dict__.update(params)
        # do not copy target and factor matrices into the program
        if sp.isspmatrix(self.V):
            self.V = self.V.tocsr().astype('d')
        else:
            self.V = np.asmatrix(self.V) if self.V.dtype == np.dtype(
                float) else np.asmatrix(self.V, dtype='d')
        if self.W != None or self.H != None or self.H1 != None:
            raise MFError(
                "Passing fixed initialized factors is not supported in SMF model.")
        self.model_name = "smf"

    def run(self):
        """Run the specified MF algorithm."""
        return self.factorize()

    def basis(self):
        """Return the matrix of basis vectors (factor 1 matrix)."""
        return self.W

    def target(self, idx=None):
        """
        Return the target matrix to estimate.
        
        :param idx: Used in the multiple MF model. In standard MF ``idx`` is always None.
        :type idx: None
        """
        return self.V

    def coef(self, idx=None):
        """
        Return the matrix of mixture coefficients (factor 2 matrix).
        
        :param idx: Used in the multiple MF model. In standard MF ``idx`` is always None.
        :type idx: None
        """
        return self.H

    def fitted(self, idx=None):
        """
        Compute the estimated target matrix according to the MF algorithm model.
        
        :param idx: Used in the multiple MF model. In standard MF ``idx`` is always None.
        :type idx: None
        """
        return dot(self.W, self.H)

    def distance(self, metric='euclidean', idx=None):
        """
        Return the loss function value.
        
        :param distance: Specify distance metric to be used. Possible are Euclidean and
           Kullback-Leibler (KL) divergence. Strictly, KL is not a metric.
        :type distance: `str` with values 'euclidean' or 'kl'

        :param idx: Used in the multiple MF model. In standard MF ``idx`` is always None.
        :type idx: None
        """
        if metric.lower() == 'euclidean':
            R = self.V - dot(self.W, self.H)
            return power(R, 2).sum()
        elif metric.lower() == 'kl':
            Va = dot(self.W, self.H)
            return (multiply(self.V, sop(elop(self.V, Va, div), op=log)) - self.V + Va).sum()
        else:
            raise utils.MFError("Unknown distance metric.")

    def residuals(self, idx=None):
        """
        Return residuals matrix between the target matrix and its MF estimate.
        
        :param idx: Used in the multiple MF model. In standard MF ``idx`` is always None.
        :type idx: None
        """
        return self.V - dot(self.W, self.H)