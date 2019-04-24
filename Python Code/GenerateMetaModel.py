'''
Kaden Plewe
04/02/2019
Script used to generate meta model for energy plus building simulations for each of the desired outputs.
This script will read a json input file for a set of energy plus building model inputs and parameters and run a
simulation for each set of input parameters. After obtaining the energy usage and thermal comfort outputs for each
parameter set, it will fit a regression model. Note that since this regression model will not depend on weather data
or simulation horizon, the model will only be represented of the energy plus model for identical simulation periods,
building types and weather input files.
'''

'''import libraries and classes'''
from EPDataModule import epData
import numpy as np
import json
import time
from sklearn.model_selection import GridSearchCV
from joblib import dump, load
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel

'''--------------------------------------------------------------------------------------------------------
Acquire Training Data for Building Model
--------------------------------------------------------------------------------------------------------'''
epFilePath = 'E:\Masters Thesis\Sensativity Analysis\Energy Plus Data\GP Training'

'''JSON parameters'''
with open('jsonOUTPUT_ALL_Train.txt') as jsonParams:
    paramSet = json.load(jsonParams)

'''run a simulation for every value in the randomly generated sample set'''
epTotalElecEnergy = np.array([])    # total electrical energy purchased over run period
epAvePMV = np.array([])         # Average PMV over simulation period for Core Zone

'''run nominal simulation'''
'''add nominal values to the input array that will be used to train the meta model'''
X = np.array([])
for obj in paramSet['input']: X = np.append(X, obj['Nominal Value'])

'''calculate energy plus data files for a range of sample sizes'''
# a = 100; b = len(paramSet['input'][0]['Sample Values']); c = b/a
a = 4000; b = 4000; c = b/a
sampleSize = np.linspace(a, b, c, dtype=int)


for N in sampleSize:
    gpFEEModelName = 'gpFEEMetaModelW%d.joblib' % N
    gpPMVModelName = 'gpPMVMetaModelW%d.joblib' % N
    try:
        # test = load('NA')
        gpElecEnergy = load(gpFEEModelName)
        gpPMV = load(gpPMVModelName)

    except FileNotFoundError:
        # input('press any key to begin \n')
        t0 = time.time()
        energyFile = 'epTotalElecEnergyALLW%d.npy' % N
        PMVFile = 'epAvePMVALLW%d.npy' % N
        ep_load = time.time() - t0
        print("=== energy plus data file loaded in %.3f s ===" % ep_load)

        '''either load data or run simulations for training data set'''
        try:
            t0 = time.time()
            ep = epData(epFilePath, N, N)
            epFEEALLS = np.sum(ep.TotalElecEnergyALLS, 1)
            epPMVALLS = np.mean(ep.AvePMVALLS, 1)

            '''extract X values'''
            X = np.zeros((N, ))
            print(X.shape)
            print(np.asarray(paramSet['input'][0]['Sample Values'][0:N]).T.shape)
            for obj in paramSet['input']: X = np.vstack((X, np.asarray(obj['Sample Values'][0:N]).T))
            X = np.delete(X, 0, 0).T
            print(X.shape)
            x_load = time.time() - t0
            print("=== input data extracted in %.3f s ===" % x_load)
        except FileNotFoundError:
            print('=== Energy Plus Data File Not Found for %s or %s ===' % (energyFile, PMVFile))
            break

        '''--------------------------------------------------------------------------------------------------------
        Build Meta Model With Acquired Training Data
        Two different regression models will be used for validation purposes: kernal ridge regression and support
        vector regression.
        --------------------------------------------------------------------------------------------------------'''

        '''declare the regression models'''
        t0 = time.time()
        kernel = DotProduct() + WhiteKernel()
        gpFEE = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
        gpPMV = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
        gp_init = time.time() - t0
        print("=== Gaussian Process regressor initialized in %.3f s ===" % gp_init)

        '''fit regression models with training data'''
        t0 = time.time()
        gpFEE.fit(X, epFEEALLS)
        gp_fit = time.time() - t0
        print("=== Electric Energy Gaussian Process complexity and bandwidth selected and model fitted in %.3f s ===" % gp_fit)
        print('=== Model saved as svrElecEnergyMetaModel%d.joblib ===' % N)

        t0 = time.time()
        gpPMV.fit(X, epPMVALLS)
        gp_fit = time.time() - t0
        print("=== Core PMV Gaussian Process complexity and bandwidth selected and model fitted in %.3f s ===" % gp_fit)
        print('=== Model saved as gpPMVMetaModel%d.joblib ===' % N)

        '''save models'''
        dump(gpFEE, gpFEEModelName)
        dump(gpPMV, gpPMVModelName)


    '''reset input/output sets'''
    epFEEALLS = np.array([])  # total electrical energy purchased over run period
    epPMVALLS = np.array([])  # Average PMV over simulation period for Core Zone
    X = np.array([])
    for obj in paramSet['input']: X = np.append(X, obj['Nominal Value'])