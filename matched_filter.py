"""Matched filter and threshold detector for a single target."""

import numpy as np


def matched_filter(r, s):
    """Correlate the receive window with the pulse for every delay.

    Parameters
    ----------
    r : ndarray of complex
        Receive window, length M.
    s : ndarray of complex
        Transmit pulse, length N <= M.

    Returns
    -------
    y : ndarray of complex
        y[d] = sum_n r[n + d] * conj(s[n]), d = 0, ..., M - N.
    """
    M = len(r)
    N = len(s)
    return np.array([np.vdot(s, r[d:d + N]) for d in range(M - N + 1)])


def detect(y, sigma, p_fa):
    """One decision per receive window: is the maximum of |y|^2 above the threshold?

    Parameters
    ----------
    y : ndarray of complex
        Matched-filter output.
    sigma : float
        Noise standard deviation.
    p_fa : float
        False-alarm probability per receive window (upper bound).

    Returns
    -------
    detected : bool
        True if max |y[d]|^2 exceeds the threshold.
    d_hat : int
        Delay of the maximum in samples.
    """
    K = len(y)
    gamma = -sigma**2 * np.log(p_fa / K)    
    y2 = np.abs(y)**2
    d_hat = int(np.argmax(y2))
    return y2[d_hat] > gamma, d_hat