import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append(".")
from python.Random import Random 

# porting dr. rogan's c code

random = Random()

Nmeas = 1
Nexp = 1000 # fewer cycles
sigma = 3.0 # wider sigma

histx = []
histy = []
for i in np.linspace(-10, 10, 201):
	mu_true = i

	for e in range(Nexp):
		mu_best = 0.0

		for m in range(Nmeas):
			x = random.Logistic(mu_true, sigma)
			mu_best += x


		mu_best = mu_best / Nmeas
		histx.append(mu_true)
		histy.append(mu_best)

# make neyman plot
fig = plt.figure(figsize=(8,8))
ax = plt.gca()
ax.set_aspect("equal")
H = plt.hist2d(histx, histy, bins=100, density=False)
plt.colorbar()
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_xlabel(r"$\mu$ true")
ax.set_ylabel(r"$\mu$ measured")
plt.show()
fig.savefig("neyman_plot.jpg", dpi=180)

# get bin edges from histogram
xedges = H[1]
yedges = H[2]

# "experimental" mu
test_mu = 0.0

#get bin index of measurement
ind = np.digitize(test_mu, yedges)

# get 2d weights from measurement
exp = H[0][:,ind]

# histogram of measurement
fig1 = plt.figure(figsize=(10,8))
H2 = plt.hist(yedges[:-1], yedges, weights=exp, color="darkgray")
n = H2[0]
bins = H2[1]

# get experiment values
mids = 0.5*(bins[1:] + bins[:-1])
mean = np.average(mids, weights=n)
std = np.sqrt(np.average((mids-mean)**2, weights=n))

plt.axvline(mean, c="C0", ls="--", label=r"$\mu$")
plt.axvline(mean+std, c="tomato", ls="--", label=r"$+\sigma$")
plt.axvline(mean-std, c="tomato", ls="--", label=r"$-\sigma$")
plt.legend()
plt.title(r"PDF for Measurement: $\mu=${:.3f}, $\sigma=${:.3f}".format(mean, std))
plt.show()
fig1.savefig("mu_meas.jpg", dpi=180)