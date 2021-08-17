import numpy as np
import pywt

#################
# real wavelets #
#################

# gets a scaling function
def scale_function(N, wavelet, scale, pos):
    Lmax = pywt.dwt_max_level(N, pywt.Wavelet(wavelet).dec_len)
    L = min(scale, Lmax)
    Ne = int(np.floor(N/2**L))
    k = int(np.floor(Ne*pos))
    temp = np.zeros(N)
    transform = pywt.wavedecn(temp, wavelet, mode='periodization', level=L)
    _, coeff_slices = pywt.coeffs_to_array(transform)
    temp[k]=1
    coeffs_from_arr = pywt.array_to_coeffs(temp, coeff_slices)
    phi = pywt.waverecn(coeffs_from_arr, wavelet, mode='periodization')
    return phi

# gets a wavelet function
def wavelet_function(N, wavelet, scale, pos):
    Lmax = pywt.dwt_max_level(N, pywt.Wavelet(wavelet).dec_len)
    L = min(scale,Lmax)
    Ne = int(np.floor(N/2**L))
    k = int(np.floor(Ne*pos))
    temp = np.zeros(N)
    transform = pywt.wavedecn(temp, wavelet, mode='periodization', level=L)
    _, coeff_slices = pywt.coeffs_to_array(transform)
    temp[k+Ne] = 1
    coeffs_from_arr = pywt.array_to_coeffs(temp, coeff_slices)
    psi = pywt.waverecn(coeffs_from_arr, wavelet, mode='periodization')
    return psi

####################
# complex wavelets #
####################

# computes coefficients in the approximation space
def V_coeffs(signal, hn):
    N = len(hn)
    coeffs = []
    for i in range(0, len(signal), 2):
        c = np.dot(hn, np.roll(signal, -i)[:N])
        coeffs.append(c)
    return np.array(coeffs)

# computes coefficients in the detail space
def W_coeffs(signal, hn):
    N = len(hn)
    gn = [(-1) ** n * np.conj(hn[N - 1 - n]) for n in range(N)]
    return V_coeffs(signal, gn)

# computes a wavelet transform knowing hn (level L)
# /!\ returns an array of arrays
# [np.array(V0...), np.array(W0...), np.array(W1), ...]
def wvt(signal, hn, L=1):
    if L == 0 or len(signal) < len(hn):
        return [signal]
    else:
        Vn = V_coeffs(signal, hn)
        Wn = W_coeffs(signal, hn)
        return wvt(Vn, hn, L - 1) + [Wn]

# computes an inverse transform
def iwvt(coefs, hn):
    if len(coefs) > 2:
        Vn = iwvt(coefs[:-1], hn)
    else:
        Vn = coefs[0]
    Wn = coefs[-1]
    N = len(hn)
    M = len(Vn)
    gn = [(-1) ** n * np.conj(hn[N - 1 - n]) for n in range(N)]
    Vn2 = np.zeros(2 * M, dtype=type(hn[0]))
    Wn2 = np.zeros(2 * M, dtype=type(hn[0]))
    for i in range(0, M):
        for j in range(N):
            index_in_rec = 2 * i + j
            Vn2[index_in_rec % (2 * M)] += Vn[i] * hn[j]
            Wn2[index_in_rec % (2 * M)] += Wn[i] * gn[j]
    return Vn2 + Wn2

# concatenates lists returned from the wavelet transform into one big array
# returns also the shape of each original list
def coefs_to_array(w):
    return np.array([i for a in w for i in a]), list(map(len, w))

# get back the array of arrays from the big array and the shapes obtained with the previous function
def array_to_coefs(arr, shapes):
    coefs = []
    start = 0
    for s in shapes:
        coefs.append(np.array(arr[start:start + s]))
        start += s
    return coefs

# gets a complex scaling function
def scale_function_complex(hn, N, scale, pos):
    L = min(scale, pywt.dwt_max_level(N, len(hn)))
    Ne = int(np.floor(N / 2 ** L))
    k = int(np.floor(Ne * pos))
    temp = np.zeros(N)
    WT = wvt(temp, hn, L)
    arr, coeff_slices = coefs_to_array(WT)
    temp[k] = 1
    coeffs_from_arr = array_to_coefs(temp, coeff_slices)
    phi = iwvt(coeffs_from_arr, hn)
    return phi

# gets a complex wavelet function
def wavelet_function_complex(hn, N, scale, pos):
    L = min(scale, pywt.dwt_max_level(N, len(hn)))
    Ne = int(np.floor(N / 2 ** L))
    k = int(np.floor(Ne * pos))
    temp = np.zeros(N)
    WT = wvt(temp, hn, L)
    arr, coeff_slices = coefs_to_array(WT)
    temp[Ne + k] = 1
    coeffs_from_arr = array_to_coefs(temp, coeff_slices)
    psi = iwvt(coeffs_from_arr, hn)
    return psi
