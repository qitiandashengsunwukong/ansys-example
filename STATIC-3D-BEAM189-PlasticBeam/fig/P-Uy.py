import numpy as np
from matplotlib.backends.backend_pdf import FigureCanvasPdf as FigureCanvas
from matplotlib.figure import Figure

data = np.loadtxt('../fea/disp.dat')

fig = Figure()
canvas = FigureCanvas(fig)
ax1 = fig.add_subplot(1, 1, 1)
line_P_Uy, = ax1.plot(data[:, 1], data[:, 0], label=r'Uy vs P')
ax1.set_xlabel(r'Deflection $UY (\mathrm{mm})$')
ax1.set_ylabel(r'Load $P (\mathrm{kN})$')
fig.savefig('P-Uy.pdf')
