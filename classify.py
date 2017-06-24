import numpy as np
import sys
import scipy.fftpack as fftpack
import scipy.integrate as integrate
from scipy.io import wavfile
from scipy import signal

#loads the data
def loadData (str):
	rate, data = wavfile.read(str)
	#if the song is dual channel, take left ear only.
	if (len(data.T) > 1):
		data = data.T[0]
	return rate, data

def welch (data, sampling_freq, nfft):
	frequencies, pxx_den = signal.welch(data, sampling_freq, nperseg = nfft)
	return frequencies, pxx_den

def analogFreqConversion(index, sampling_freq, n):
	return index * sampling_freq / n

def findCutoffIndices(array_length, sampling_freq, n):
	realfreqs = [analogFreqConversion(index, sampling_freq, n) for index in range(0, array_length)]
	basscutoff = 0
	while realfreqs[basscutoff] < 300:
		basscutoff += 1
	midcutoff = basscutoff
	while realfreqs[midcutoff] < 2000:
		midcutoff += 1
	highcutoff = array_length
	return basscutoff, midcutoff, highcutoff

def integratePxx(data, cut1, cut2, cut3):
	bass = integrate.trapz(data[0:cut1])
	mid = integrate.trapz(data[cut1:cut2])
	treble = integrate.trapz(data[cut2:cut3])
	return bass, mid, treble

def percent(b, m, h):
	total = b + m + h
	return (b / total * 100), (m / total * 100), (h / total * 100)

def classify(b, m, h):
	if h > 9.0:
		return "v shaped"
	if np.absolute(b - m) < 10:
		return "neutral"
	if m > 50.0:
		return "mid forward"
	if b > 60.0:
		return "bass"
	return "neutral"

#USE BY:
#python3 classify.py [yoursong].wav
if __name__ == '__main__':
	assert len(sys.argv) == 2
	_, inputname = sys.argv

	assert inputname.find('.wav') > -1
	sampling_freq, data = loadData(inputname)

	NFFT = 4096
	freq_arr, pxx_den = welch(data, sampling_freq, NFFT)
	cut1, cut2, cut3 = findCutoffIndices(len(pxx_den), sampling_freq, NFFT)
	
	bass, mid, treble = integratePxx(pxx_den, cut1, cut2, cut3)
	bpercent, mpercent, tpercent = percent(bass, mid, treble)
	
	result = classify(bpercent, mpercent, tpercent)

	print(result)


	

