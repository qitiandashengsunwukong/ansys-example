import numpy as np

wave = np.genfromtxt('ELCENTRO.DAT', delimiter='  ',
    missing_values='NaN', names=None, skip_header=6, skip_footer=1)

wave2 = np.reshape(wave, (np.product(wave.shape), 1))
wave2 = wave2[~np.isnan(wave2)]
np.savetxt("wave.csv", wave2, fmt='%8.5f', delimiter=' ', newline='\n')
