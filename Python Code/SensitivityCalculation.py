'''
Kaden Plewe
04/03/2019
This script will use the gaussian process regression models generated for the energy plus simulations in order to
pwerform a sensitivity analysis on all of the input parameters by calculating sobol indices.
'''

import json
import os
import numpy as np
from joblib import load
import time
import scipy.stats as stats
import matplotlib.pyplot as plt
from SALib.sample import finite_diff
from SALib.analyze import dgsm
from SALib.test_functions import Ishigami
import seaborn as sns

'''JSON parameters'''
with open('jsonOUTPUT_ALL_Train.txt') as jsonParams:
    paramSet = json.load(jsonParams)

'''SALib test'''

# # Define the model inputs
# problem = {
#     'num_vars': 3,
#     'names': ['x1', 'x2', 'x3'],
#     'bounds': [[-3.14159265359, 3.14159265359],
#                [-3.14159265359, 3.14159265359],
#                [-3.14159265359, 3.14159265359]]
# }
#
# # Generate samples
# param_values = saltelli.sample(problem, 1000)
#
# # Run model (example)
# Y = Ishigami.evaluate(param_values)
#
# # Perform analysis
# Si = sobol.analyze(problem, Y, print_to_console=True)
#
# # Print the first-order sensitivity indices
# print(Si['S1'])

'''generate problem domain with the json parameter set'''
problem = {
    'num_vars': 0,
    'names': [],
    'bounds': []
}
t0 = time.time()
for obj in paramSet['input']:
    problem['names'].append(str(obj['ID']))
    if min(obj['Sample Values']) == 1e-8 and max(obj['Sample Values']) == 1e-8:
        problem['bounds'].append([0, 0.1])
    else:
        problem['bounds'].append([min(obj['Sample Values']), max(obj['Sample Values'])])
    problem['num_vars'] += 1
problem_load = time.time() - t0
print('=== problem formulated in %d seconds ===' % problem_load)

'''Generate samples'''
N = 5
t0 = time.time()
param_values = finite_diff.sample(problem, N)
param_calc = time.time() - t0
print('=== parameters generated in %d seconds ===' % param_calc)
print(param_values.shape)
'''load gaussian process models'''
gpFEE = load('gpFEEMetaModel4000.joblib')
gpPMV = load('gpPMVMetaModel4000.joblib')

'''run snalysis for both models'''
try:
    # test = np.load('NA')
    outFEE = np.load('outFEE%d.npy' % N)
    outPMV = np.load('outPMV%d.npy' % N)
    print('=== saved outputs loaded ===')
except FileNotFoundError:
    outFEE = np.zeros([param_values.shape[0]])
    outPMV = np.zeros([param_values.shape[0]])
    t0 = time.time()
    for i, X in enumerate(param_values):
        outFEE[i] = gpFEE.predict(X.reshape(1, -1))
        outPMV[i] = gpPMV.predict(X.reshape(1, -1))
    out_calc = time.time() - t0
    print('=== outputs generated in %d seconds ===' % out_calc)

    np.save('outFEE%d'%N, outFEE)
    np.save('outPMV%d'%N, outPMV)

'''Perform analysis'''
try:
    # test = np.load('NA')
    SiFEE = np.load('SiFEE%d.npy' % N)
    SiPMV = np.load('SiPMV%d.npy' % N)
    print('=== saved results loaded ===')
except FileNotFoundError:
    t0 = time.time()
    SiFEE = dgsm.analyze(problem, param_values, outFEE, print_to_console=False)
    SiPMV = dgsm.analyze(problem, param_values, outPMV, print_to_console=False)
    analyze = time.time() - t0
    print('=== sensitivity analyzed in %d seconds ===' % analyze)

    np.save('SiFEE%d'%N, SiFEE)
    np.save('SiPMV%d'%N, SiPMV)

print(SiPMV.item().get('vi'))

colors = sns.hls_palette(10, l=.55, s=.6)
externality_colors = ["#be0119", "#7a6a4f", "#94ac02", "#0e87cc", "#887191"]
# sns.palplot(externality_colors)
plt.rcParams['font.serif'] = 'DejaVu Serif'
plt.rcParams['figure.figsize'] = 10, 6.5
plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams['figure.titlesize'] = 20
plt.rcParams['figure.titleweight'] = 'heavy'
plt.rcParams['axes.titlepad'] = 20
plt.rcParams['axes.labelpad'] = 20
plt.rcParams['legend.loc'] = 'upper left'
plt.rcParams['legend.fontsize'] = 14

axfont = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 16,
        }
axfontsm = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 12,
        }
legendfont = {'family': 'serif',
        'weight': 'light',
        'size': 14,
        }
legendfontsm = {'family': 'serif',
        'weight': 'light',
        'size': 10,
        }
titlefont = {'family': 'serif',
        'color':  'black',
        'weight': 'heavy',
        'size': 20,
        }
titlefontsm = {'family': 'serif',
        'color':  'black',
        'weight': 'heavy',
        'size': 12,
        }
tickfont = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 12,
        }


'''sort and color the indices'''
names = []
[names.append(int(problem['names'][i])) for i in range(len(problem['names']))]

orderedNamesFEE = [x for _,x in sorted(zip(SiFEE.item().get('dgsm'), names))]
orderedNamesPMV = [x for _,x in sorted(zip(SiPMV.item().get('dgsm'), names))]
optFEE = SiFEE.item().get('dgsm')[orderedNamesFEE[-10:]]
optPMV = SiPMV.item().get('dgsm')[orderedNamesPMV[-10:]]

print(orderedNamesFEE[-10:])
print(optFEE)
print(orderedNamesPMV[-10:])
print(optPMV)

schNames = names[:220]
matNames = names[221:221+576]
eqNames = names[221+576:]
schDGSMFEE = SiFEE.item().get('dgsm')[:220]
matDGSMFEE = SiFEE.item().get('dgsm')[221:221+576]
eqDGSMFEE = SiFEE.item().get('dgsm')[221+576:]
schDGSMPMV = SiPMV.item().get('dgsm')[:220]
matDGSMPMV = SiPMV.item().get('dgsm')[221:221+576]
eqDGSMPMV = SiPMV.item().get('dgsm')[221+576:]


'''sensativity figure'''
figname = 'DGSMSensitivitySummer.jpg'
fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex='col', sharey='row')

schML, schSL, schBL = ax1.stem(schNames, schDGSMFEE, markerfmt='^')
matML, matSL, matBL = ax1.stem(matNames, matDGSMFEE, markerfmt='o')
eqML, eqSL, eqBL = ax1.stem(eqNames, eqDGSMFEE, markerfmt='s')

plt.setp(schML, color=colors[0])
plt.setp(schSL, color=colors[0])
plt.setp(matML, color=colors[2])
plt.setp(matSL, color=colors[2])
plt.setp(eqML, color=colors[5])
plt.setp(eqSL, color=colors[5])

schML, schSL, schBL = ax3.stem(schNames, schDGSMPMV, markerfmt='^')
matML, matSL, matBL = ax3.stem(matNames, matDGSMPMV, markerfmt='o')
eqML, eqSL, eqBL = ax3.stem(eqNames, eqDGSMPMV, markerfmt='s')

plt.setp(schML, color=colors[0])
plt.setp(schSL, color=colors[0])
plt.setp(matML, color=colors[2])
plt.setp(matSL, color=colors[2])
plt.setp(eqML, color=colors[5])
plt.setp(eqSL, color=colors[5])

optML, optSL, optBL = ax2.stem(orderedNamesFEE[-10:], optFEE, markerfmt='*')
plt.setp(optML, color='k')
plt.setp(optSL, color='k')

optML, optSL, optBL = ax4.stem(orderedNamesPMV[-10:], optPMV, markerfmt='*')
plt.setp(optML, color='k')
plt.setp(optSL, color='k')

ax1.set_ylabel('Electric Energy DGSM', fontdict=axfont)
ax1.set_yscale('log')
ax3.set_xlabel('Parameter Number', fontdict=axfont)
ax3.set_ylabel('PMV DGSM', fontdict=axfont)
ax3.set_yscale('log')
ax4.set_xlabel('Parameter Number', fontdict=axfont)

for tick in ax1.get_xticklabels():
    tick.set_fontname("serif")
for tick in ax1.get_yticklabels():
    tick.set_fontname("serif")
for tick in ax2.get_xticklabels():
    tick.set_fontname("serif")
for tick in ax2.get_yticklabels():
    tick.set_fontname("serif")
for tick in ax3.get_xticklabels():
    tick.set_fontname("serif")
for tick in ax3.get_yticklabels():
    tick.set_fontname("serif")
for tick in ax4.get_xticklabels():
    tick.set_fontname("serif")
for tick in ax4.get_yticklabels():
    tick.set_fontname("serif")

ax3.set_xlim(0, 907)
ax4.set_xlim(0, 907)

sch = 'Setpoints/\nSchedules'
mat = 'Materials'
eq = 'Equipment'

props = dict(boxstyle='round', facecolor='white')
ax1.text(0.022, 0.25, sch, transform=ax1.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)
ax1.text(0.44, 0.22, mat, transform=ax1.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)
ax1.text(0.83, 0.22, eq, transform=ax1.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)
ax3.text(0.022, 0.25, sch, transform=ax3.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)
ax3.text(0.44, 0.22, mat, transform=ax3.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)
ax3.text(0.83, 0.22, eq, transform=ax3.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)
fig1.savefig(figname)

# ax1.set_yscale('log')
# ax2.set_yscale('log')
plt.show()