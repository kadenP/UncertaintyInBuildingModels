'''
Kaden Plewe
04/03/2019
This script will compare the output distributions for the energy plus model simulations and the gaussian process
regression fit for the same data sets for a range of sample sets. In order to compare the distributions, a
bhattacharyya distance is calculated for each model that was calculated with a different sample set size. The
objective here is to find the sufficient sample size that allows the gaussian process model and the energy plus model
distrubutions to match.
'''

'''import libraries and classes'''
from EPDataModule import epData
import json
import os
import numpy as np
from joblib import load
import scipy.stats as stats
import matplotlib.pyplot as plt

'''functions'''
def bhattacharyya(H1, H2):
    mu1 = np.mean(H1)               # mean of distribution 1
    sig1 = np.sqrt(np.var(H1))      # std of distribution 1
    mu2 = np.mean(H2)               # mean of distribution 2
    sig2 = np.sqrt(np.var(H2))      # std of distribution 2

    return 0.25*np.log(0.25*(sig1/sig2 + sig2/sig1 + 2)) + 0.25*((mu1 - mu2)**2/(sig1 + sig2))

def roundup(x):
    return int(np.ceil(x / 100.0)) * 100

'''JSON parameters'''
with open('jsonOUTPUT_ALL_Train.txt') as jsonParams:
    paramSet = json.load(jsonParams)

'''--------------------------------------------------------------------------------------------------------
Generate Energy Plus Data
--------------------------------------------------------------------------------------------------------'''

'''energy plus test folder'''
epFilePath = 'E:\Masters Thesis\Sensativity Analysis\Energy Plus Data\GP Training'

'''calculate energy plus data files for a range of sample sizes'''
# a = 100; b = len(paramSet['input'][0]['Sample Values']); c = b/a
a = 100; b = 5000; c = b/a
sampleSize = np.linspace(a, b, c, dtype=int)

'''define roundup function to be used later for results output'''
base = b/c
def roundup(x, base):
    return int(np.ceil(x / float(base))) * base

'''data used for comparison'''
epMeanFEE = np.array([])
epStdFEE = np.array([])
epMeanPMV = np.array([])
epStdPMV = np.array([])
gpMeanFEE = np.array([])
gpStdFEE = np.array([])
gpMeanPMV = np.array([])
gpStdPMV = np.array([])

'''comparison metrics'''
R2FEE = np.array([])
R2PMV = np.array([])
bdFEE = np.array([])
bdPMV = np.array([])
meanErrorFEE = np.array([])
meanErrorPMV = np.array([])
stdErrorFEE = np.array([])
stdErrorPMV = np.array([])

for N in [4000]:
    print('====== ready to process evaluate models for %d samples ======' % N)
    # input('press any key to begin \n')
    energyFile = 'epTotalElecEnergy%d.npy' % 5000
    PMVFile = 'epAvePMV%d.npy' % 5000
    '''try to load energy plus data files, else generate data by running energy plus simulations'''
    try:
        ep = epData(epFilePath, 5000, 5000)
        epFEEALLS = np.sum(ep.TotalElecEnergyALLS, 1)   # total electrical energy purchased over run period
        epPMVALLS = np.mean(ep.AvePMVALLS, 1)   # Average PMV over simulation period for Core Zone
    except FileNotFoundError:
        print('=== Energy Plus Data File Not Found for %s or %s ===' % (energyFile, PMVFile))
        break

    '''calculate statistics for generating the probability density function for electric energy and PMV values'''
    epMeanFEE = np.append(epMeanFEE, np.mean(epFEEALLS))
    epStdFEE = np.append(epStdFEE, np.sqrt(np.var(epFEEALLS)))
    epMeanPMV = np.append(epMeanPMV, np.mean(epPMVALLS))
    epStdPMV = np.append(epStdPMV, np.sqrt(np.var(epPMVALLS)))

    print(epMeanFEE)

    '''--------------------------------------------------------------------------------------------------------
    Generate Gaussian Process Regression Meta Model Data
    --------------------------------------------------------------------------------------------------------'''
    gpFEEModelName = 'gpFEEMetaModel%d.joblib' % N
    gpPMVModelName = 'gpPMVMetaModel%d.joblib' % N

    gpFEE = load(gpFEEModelName)
    gpPMV = load(gpPMVModelName)

    '''generate set of nominal input parameters'''
    nomX = np.array([])
    for obj in paramSet['input']: nomX = np.append(nomX, obj['Nominal Value'])

    '''generate set of nominal outputs for nominal input values'''
    gpFEENom = gpFEE.predict(nomX.reshape(1, -1))
    gpPMVNom = gpPMV.predict(nomX.reshape(1, -1))

    print('Nominal Electric Energy for Gaussian Process Model = %1.3f [J]' % gpFEENom)
    print('Nominal PMV for Gaussian Process Model = %1.3f [J]' % gpPMVNom)

    '''extract all of the samples for each parameter'''
    X = np.zeros((len(paramSet['input'][0]['Sample Values'][0:5000]), 1))
    for obj in paramSet['input']: X = np.hstack((X, np.asarray([obj['Sample Values'][0:5000]]).T))
    X = np.delete(X, 0, 1)

    '''generate set of outputs for current input values'''
    gpFEEVal = gpFEE.predict(X)
    gpPMVVal = gpPMV.predict(X)

    '''calculate statistics for generating the probability density function for electric energy and PMV values'''
    gpMeanFEE = np.append(gpMeanFEE, np.mean(gpFEEVal))
    gpStdFEE = np.append(gpStdFEE, np.sqrt(np.var(gpFEEVal)))
    gpMeanPMV = np.append(gpMeanPMV, np.mean(gpPMVVal))
    gpStdPMV = np.append(gpStdPMV, np.sqrt(np.var(gpPMVVal)))

    '''calculate the comparisson measures for this sample set'''

    # print('size of gpElecEnergyVal: %d' % len(gpElecEnergyVal))
    # print('size of epElecEnergy: %d' % len(epElecEnergy))
    # print('size of gpPMV: %d' % len(gpPMVVal))
    # print('size of epPMV: %d' % len(epPMV))
    R2FEE = np.append(R2FEE, gpFEE.score(X, epFEEALLS))
    R2PMV = np.append(R2PMV, gpPMV.score(X, epPMVALLS))
    bdFEE = np.append(bdFEE, bhattacharyya(gpFEEVal, epFEEALLS))
    bdPMV = np.append(bdPMV, bhattacharyya(gpPMVVal, epPMVALLS))
    meanErrorFEE = np.append(meanErrorFEE, abs((gpMeanFEE[-1] - epMeanFEE[-1])/epMeanFEE[-1]))
    meanErrorPMV = np.append(meanErrorPMV, abs((gpMeanPMV[-1] - epMeanPMV[-1])/epMeanPMV[-1]))
    stdErrorFEE = np.append(stdErrorFEE, abs((gpStdFEE[-1] - epStdFEE[-1])/epStdFEE[-1]))
    stdErrorPMV = np.append(stdErrorPMV, abs((gpStdPMV[-1] - epStdPMV[-1])/epStdPMV[-1]))
    print('Mean Error for Elec Energy GP Model = %1.3f [J]' % meanErrorFEE[-1])
    print('STD Error for Elec Energy GP Model = %1.3f [J]' % stdErrorFEE[-1])
    print('Mean Error for PMV GP Model = %1.3f [J]' % meanErrorPMV[-1])
    print('STD Error for PMV GP Model = %1.3f [J]' % stdErrorPMV[-1])

    print('ep FEE mean:', epMeanFEE)
    print('ep PMV mean:', epMeanPMV)
    print('ep FEE std:', epStdFEE)
    print('ep PMV std:', epStdPMV)
    print('gp FEE mean:', gpMeanFEE)
    print('gp PMV mean:', gpMeanPMV)
    print('gp FEE std:', gpStdFEE)
    print('gp PMV std:', gpStdPMV)
    print('FEE mean err:', (gpMeanFEE-epMeanFEE)/epMeanFEE)
    print('PMV mean err:', (gpMeanPMV - epMeanPMV) / epMeanPMV)
    print('FEE std err:', (gpStdFEE - epStdFEE) / epStdFEE)
    print('PMV std err:', (gpStdPMV - epStdPMV) / epStdPMV)

    np.save('meanFEE.npy', epMeanFEE)
    np.save('meanPMV.npy', epMeanPMV)
    np.save('stdFEE.npy', epStdFEE)
    np.save('stdPMV.npy', epStdPMV)
    np.save('bhattacharyyaFEE.npy', bdFEE)
    np.save('bhattacharyyaPMV.npy', bdPMV)
    np.save('meanErrorFEE.npy', meanErrorFEE)
    np.save('meanErrorPMV.npy', meanErrorPMV)
    np.save('stdErrorFEE.npy', stdErrorFEE)
    np.save('stdErrorPMV.npy', stdErrorPMV)

bdFEE = np.load('bhattacharyyaFEE.npy')
bdPMV = np.load('bhattacharyyaPMV.npy')
meanErrorFEE = np.load('meanErrorFEE.npy')
meanErrorPMV = np.load('meanErrorPMV.npy')
stdErrorFEE = np.load('stdErrorFEE.npy')
stdErrorPMV = np.load('stdErrorPMV.npy')

'''ploting'''
# import seaborn as sns
#
# # plt.style.use('seaborn-darkgrid')
# colors = sns.hls_palette(10, l=.55, s=.6)
# externality_colors = ["#be0119", "#7a6a4f", "#94ac02", "#0e87cc", "#887191"]
# ccolors = ['orangered', 'olivedrab']
# # sns.palplot(externality_colors)
# plt.rcParams['font.serif'] = 'DejaVu Serif'
# plt.rcParams['figure.figsize'] = 8, 6.5
# plt.rcParams['figure.constrained_layout.use'] = True
# plt.rcParams['figure.titlesize'] = 20
# plt.rcParams['figure.titleweight'] = 'heavy'
# plt.rcParams['axes.titlepad'] = 20
# plt.rcParams['axes.labelpad'] = 20
# plt.rcParams['legend.loc'] = 'upper left'
# plt.rcParams['legend.fontsize'] = 14
#
# axfont = {'family': 'serif',
#         'color':  'black',
#         'weight': 'normal',
#         'size': 16,
#         }
# axfontsm = {'family': 'serif',
#         'color':  'black',
#         'weight': 'normal',
#         'size': 12,
#         }
# legendfont = {'family': 'serif',
#         'weight': 'light',
#         'size': 14,
#         }
# legendfontsm = {'family': 'serif',
#         'weight': 'light',
#         'size': 10,
#         }
# titlefont = {'family': 'serif',
#         'color':  'black',
#         'weight': 'heavy',
#         'size': 20,
#         }
# tickfont = {'family': 'serif',
#         'color':  'black',
#         'weight': 'normal',
#         'size': 12,
#         }
#
# figname = 'SummerConvergence.jpeg'
# fig1, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
# ax1.plot(sampleSize, bdFEE, '-ok')
# ax1.plot([4000, 4000], ax1.get_ylim(), '-r')
# # ax1.set_title('Convergence Analysis for GPR', fontsize=14)
# ax1.set_ylabel('Electric Energy \nBhattacharyya Distance', fontdict=axfont)
# ax1.set_yscale('log')
# ax2.plot(sampleSize, bdPMV, '-ok')
# ax2.plot([4000, 4000], ax2.get_ylim(), '-r')
# ax2.set_xlabel('Number of Samples', fontdict=axfont)
# ax2.set_ylabel('PMV \nBhattacharyya Distance', fontdict=axfont)
# ax2.set_yscale('log')
#
# for tick in ax1.get_xticklabels():
#     tick.set_fontname("serif")
# for tick in ax1.get_yticklabels():
#     tick.set_fontname("serif")
# for tick in ax2.get_xticklabels():
#     tick.set_fontname("serif")
# for tick in ax2.get_yticklabels():
#     tick.set_fontname("serif")
#
# ax2.set_xlim(0, 5000)
#
# fig1.savefig(figname)

# '''plot for N = 4000'''
# '''load energy plus data'''
# ep = epData(epFilePath, 5000, 5000)
# epFEENomS = np.sum(ep.TotalElecEnergyNomS)
# epPMVNomS = np.mean(ep.AvePMVNomS)
# epFEEALLS = np.sum(ep.TotalElecEnergyALLS, 1)  # total electrical energy purchased over run period
# epPMVALLS = np.mean(ep.AvePMVALLS, 1)  # Average PMV over simulation period for Core Zone
#
# '''calculate statistics for generating the probability density function for electric energy and PMV values'''
# epMeanFEEALLS = np.mean(epFEEALLS)
# epStdFEEALLS = np.sqrt(np.var(epFEEALLS))
# epMeanPMVALLS = np.mean(epPMVALLS)
# epStdPMVALLS = np.sqrt(np.var(epPMVALLS))
#
# '''bin size based on Sturge's Rule'''
# nbins = int(1 + 3.322 * np.log10(len(epFEEALLS))) * 2
#
# '''probability density function for total electric energy and PMV values'''
# epxFEE = np.linspace(min(epFEEALLS), max(epFEEALLS), nbins + 1)
# epxPMV = np.linspace(min(epPMVALLS), max(epPMVALLS), nbins + 1)
# eppdfFEE = stats.norm.pdf(epxFEE, epMeanFEEALLS, epStdFEEALLS)
# eppdfPMV = stats.norm.pdf(epxPMV, epMeanPMVALLS, epStdPMVALLS)
#
# '''load gaussian process model'''
# gpFEE = load('gpFEEMetaModel%d.joblib' % 4000)
# gpPMV = load('gpPMVMetaModel%d.joblib' % 4000)
#
# '''extract random data to use in gp model'''
# for i in range(5000):
#     # for i in range(50):
#     '''update JSON file and input parameter array for training meta model'''
#     xTemp = np.array([])
#     for obj in paramSet['input']: xTemp = np.append(xTemp, obj['Sample Values'][i])
#     X = np.vstack((X, xTemp)) if i != 0 else xTemp
#
# print(X.shape)
# '''compute gaussian process model data'''
# gpFEEVal = gpFEE.predict(X)
# gpPMVVal = gpPMV.predict(X)
#
# '''calculate statistics for generating the probability density function for electric energy and PMV values'''
# gpMeanFEE = np.mean(gpFEEVal)
# gpStdFEE = np.sqrt(np.var(gpFEEVal))
# gpMeanPMV = np.mean(gpPMVVal)
# gpStdPMV = np.sqrt(np.var(gpPMVVal))
#
# '''probability density function for total electric energy and PMV values'''
# gpxFEE = np.linspace(min(gpFEEVal), max(gpFEEVal), nbins + 1)
# gpxPMV = np.linspace(min(gpPMVVal), max(gpPMVVal), nbins + 1)
# gppdfFEE = stats.norm.pdf(gpxFEE, gpMeanFEE, gpStdFEE)
# gppdfPMV = stats.norm.pdf(gpxPMV, gpMeanPMV, gpStdPMV)
#
# '''plot histogram'''
# ax1stats = '\n'.join((
#     r'$\mu_{ep}=%.2f$' % (epMeanFEEALLS, ),
#     r'$\sigma_{ep}=%.2f$' % (epStdFEEALLS, ),
#     r'$\mu_{gp}=%.2f$' % (gpMeanFEE, ),
#     r'$\sigma_{gp}=%.2f$' % (gpStdFEE, ),
# ))
#
# ax2stats = '\n'.join((
#     r'$\mu_{ep}=%.2f$' % (epMeanPMVALLS, ),
#     r'$\sigma_{ep}=%.2f$' % (epStdPMVALLS, ),
#     r'$\mu_{gp}=%.2f$' % (gpMeanPMV, ),
#     r'$\sigma_{gp}=%.2f$' % (gpStdPMV, ),
# ))
#
# props = dict(boxstyle='round', facecolor='white')
#
# figname = 'metamodelcomparison4000.jpeg'
# histFig, (ax1, ax2) = plt.subplots(nrows=2)
# gpFEEweights = np.ones_like(gpFEEVal) / len(gpFEEVal)
# epFEEweights = np.ones_like(epFEEALLS) / len(epFEEALLS)
# ax1.hist(gpFEEVal, bins=nbins, histtype='step', align='mid', weights=gpFEEweights, color=ccolors[0], label='GP Model')
# ax1.hist(epFEEALLS, bins=nbins, histtype='step', align='mid', weights=gpFEEweights, color=ccolors[1], label='EP Model')
# ax1.set_ylabel('Probability Density', fontdict=axfont)
# ax1.set_xlabel('Electric Energy [MJ]', fontdict=axfont)
# ax1.plot([epFEENomS, epFEENomS], ax1.get_ylim(), '--r', label='Nominal')
# ax1.text(0.05, 0.95, ax1stats, transform=ax1.transAxes, fontsize=14,
#         verticalalignment='top', bbox=props)
# ax1.legend(prop=legendfont, loc=1)
#
# gpPMVweights = np.ones_like(gpPMVVal) / len(gpPMVVal)
# epPMVweights = np.ones_like(epPMVALLS) / len(epPMVALLS)
#
# ax2.hist(gpPMVVal, bins=nbins, histtype='step', align='mid', weights=gpPMVweights, color=ccolors[0], label='GP Model')
# ax2.hist(epPMVALLS, bins=nbins, histtype='step', align='mid', weights=epPMVweights, color=ccolors[1], label='EP Model')
# ax2.plot([epPMVNomS, epPMVNomS], ax2.get_ylim(), '--r', label='Nominal')
# ax2.set_ylabel('Probability Density', fontdict=axfont)
# ax2.set_xlabel('Predicted Mean Vote', fontdict=axfont)
# ax2.text(0.05, 0.95, ax2stats, transform=ax2.transAxes, fontsize=14,
#         verticalalignment='top', bbox=props)
#
# histFig.savefig(figname)

# '''collect set of points to show distributions for'''
# testDistributions = fig1.ginput(-1, timeout=15, show_clicks=True)
#
# j = 2
# # for point in testDistributions:
# for point in testDistributions:
#     N = int(roundup(point[0], base))
#     testSize = int(roundup(N/10, base))
#     print(testSize)
#     print(N)
#
#     # N = point
#
#     '''load energy plus data'''
#     ep = epData(epFilePath, N, N)
#     epFEEALLS = np.sum(ep.TotalElecEnergyALLS, 1)  # total electrical energy purchased over run period
#     epPMVALLS = np.mean(ep.AvePMVALLS, 1)  # Average PMV over simulation period for Core Zone
#     epFEEALLS = epFEEALLS[N-testSize:N]
#     epPMVALLS = epPMVALLS[N-testSize:N]
#
#     '''calculate statistics for generating the probability density function for electric energy and PMV values'''
#     epMeanFEEALLS = np.mean(epFEEALLS)
#     epStdFEEALLS = np.sqrt(np.var(epFEEALLS))
#     epMeanPMVALLS = np.mean(epPMVALLS)
#     epStdPMVALLS = np.sqrt(np.var(epPMVALLS))
#
#     '''bin size based on Sturge's Rule'''
#     nbins = int(1 + 3.322*np.log10(len(epFEEALLS)))*2
#
#     '''probability density function for total electric energy and PMV values'''
#     epxFEE = np.linspace(min(epFEEALLS), max(epFEEALLS), nbins+1)
#     epxPMV = np.linspace(min(epPMVALLS), max(epPMVALLS), nbins+1)
#     eppdfFEE = stats.norm.pdf(epxFEE, epMeanFEEALLS, epStdFEEALLS)
#     eppdfPMV = stats.norm.pdf(epxPMV, epMeanPMVALLS, epStdPMVALLS)
#
#     '''load gaussian process model'''
#     gpFEE = load('gpFEEMetaModel%d.joblib' % N)
#     gpPMV = load('gpPMVMetaModel%d.joblib' % N)
#
#     '''extract random data to use in gp model'''
#     for i in range(100):
#     # for i in range(50):
#         '''update JSON file and input parameter array for training meta model'''
#         xTemp = np.array([])
#         for obj in paramSet['input']: xTemp = np.append(xTemp, obj['Sample Values'][i])
#         X = np.vstack((X, xTemp)) if i != 0 else xTemp
#
#     print(X.shape)
#     '''compute gaussian process model data'''
#     gpFEEVal = gpFEE.predict(X)
#     gpPMVVal = gpPMV.predict(X)
#
#     '''calculate statistics for generating the probability density function for electric energy and PMV values'''
#     gpMeanFEE = np.mean(gpFEEVal)
#     gpStdFEE = np.sqrt(np.var(gpFEEVal))
#     gpMeanPMV = np.mean(gpPMVVal)
#     gpStdPMV = np.sqrt(np.var(gpPMVVal))
#
#     '''probability density function for total electric energy and PMV values'''
#     gpxFEE = np.linspace(min(gpFEEVal), max(gpFEEVal), nbins+1)
#     gpxPMV = np.linspace(min(gpPMVVal), max(gpPMVVal), nbins+1)
#     gppdfFEE = stats.norm.pdf(gpxFEE, gpMeanFEE, gpStdFEE)
#     gppdfPMV = stats.norm.pdf(gpxPMV, gpMeanPMV, gpStdPMV)
#
#     '''plot probability density functions and statistics for ep and gp model'''
#     plt.figure(j)
#     plt.subplot(2, 1, 1)
#     gpE, = plt.plot(gpxFEE, gppdfFEE, label='gp model', color='orange')
#     epE, = plt.plot(epxFEE, eppdfFEE, label='ep model', color='blue')
#     plt.ylabel('Probability Density', fontsize=16)
#     plt.xlabel('Total Electric Energy [MJ]', fontsize=16)
#     plt.title('%d Samples' % N, fontsize=16)
#
#     plt.subplot(2, 1, 2)
#     gpPMV, = plt.plot(gpxPMV, gppdfPMV, label='gp model', color='orange')
#     epPMV, = plt.plot(epxPMV, eppdfPMV, label='ep model', color='blue')
#     plt.ylabel('Probability Density', fontsize=16)
#     plt.xlabel('PMV', fontsize=16)
#
#     plt.legend()
#
#     j += 1

# fig2, ((ax3, ax4), (ax5, ax6)) = plt.subplots(nrows=2, ncols=2)
# ax3.plot(sampleSize, meanErrorElecEnergy)
# ax4.plot(sampleSize, stdErrorElecEnergy)
# ax5.plot(sampleSize, meanErrorPMV)
# ax6.plot(sampleSize, stdErrorPMV)

plt.show()
