'''
Kaden Plewe
04/03/2019
This script will generate energy plus model data with different sample sizes to use in PCA and convergence analysis.
'''

'''import libraries and classes'''
from SmallOfficeModules import configuresmalloffice
from SmallOfficeModules import smallofficeoutputs
from eppy.modeleditor import IDF
import eppy.json_functions as json_functions
import json
import os
import numpy as np
from joblib import load
import scipy.stats as stats
import matplotlib.pyplot as plt

'''JSON parameters'''
with open('jsonOUTPUT_ALL.txt') as jsonParams:
    paramSet = json.load(jsonParams)


'''--------------------------------------------------------------------------------------------------------
Generate Energy Plus Data
--------------------------------------------------------------------------------------------------------'''
'''files used for energy plus simulation'''
iddfile = "C:\EnergyPlusV8-5-0\Energy+.idd"
fname = "SmallOffice.idf"
weatherfile = "USA_MI_Lansing-Capital.City.AP.725390_TMY3.epw"

'''initialize idf file'''
IDF.setiddname(iddfile)
idfdevice = IDF(fname, weatherfile)

'''declare simulation run period'''
Begin_Month = '7'
Begin_Day_of_Month = '16'
End_Month = '7'
End_Day_of_Month = '29'

'''configure the idf file that will be used for simulations'''
configuresmalloffice(idfdevice, Begin_Month, Begin_Day_of_Month, End_Month, End_Day_of_Month)

'''run nominal simulation'''
'''run IDF and the associated batch file to export the custom csv output'''
idfdevice.run(verbose='q')
os.system(r'CD C:\Users\Owner\OneDrive\Research\Masters Thesis\Cosimulation\SmallOffice')
os.system('CustomCSV SO OUTPUT')

'''extract nominal output data'''
nomOutputSet = smallofficeoutputs('SO_OUTPUT_hourly.csv')
epElecEnergyNom = nomOutputSet.elecEnergy
epPMVNom = nomOutputSet.allPMV_mean1
epHeatEnergyNom = nomOutputSet.allHE_sum1
epLightsEnergyNom = nomOutputSet.allLE_sum1
epEquipEnergyNom = nomOutputSet.allEEE_sum1
DateTime = nomOutputSet.DateTime

'''data used for comparison'''
epElecEnergy = epElecEnergyNom
epPMV = epPMVNom
epHeatEnergy = epHeatEnergyNom
epLightsEnergy = epLightsEnergyNom
epEquipEnergy = epEquipEnergyNom

'''Number of samples to run'''
N = 100

print('====== ready to evaluate energy plus model for %d samples ======' % N)
# input('press any key to begin \n')
DateTimeFile = 'epDateTimeS.npy'
elecEnergyFile = 'epTotalElecEnergySET3S%d.npy' % N
PMVFile = 'epAvePMVSET3S%d.npy' % N
heatEnergyFile = 'epHeatEnergySET3S%d.npy' % N
lightsEnergyFile = 'epLightsEnergySET3S%d.npy' % N
equipEnergyFile = 'epEquipEnergySET3S%d.npy' % N

'''try to load energy plus data files, else generate data by running energy plus simulations'''
try:
    epElecEnergy = np.load('NA.npy')  # total electrical energy purchased over run period
    epElecEnergy = np.load(elecEnergyFile)  # total electrical energy purchased over run period
    epPMV = np.load(PMVFile)  # Average PMV over simulation period for Core Zone
    epHeatEnergy = np.load(heatEnergyFile)  # total heating energy used over run period
    epLightsEnergy = np.load(lightsEnergyFile)  # total lighting energy used over run period
    epEquipEnergy = np.load(equipEnergyFile)  # total equipment electric energy used over run period

    print('=== all requested files already exist ===')

except FileNotFoundError:
    '''run parametric simulations'''
    for i in range(N):
        '''update JSON file'''
        runJSON = {}
        for object in paramSet['input']: runJSON[object['eppy json string']] = object['Sample Values'][i]
        json_functions.updateidf(idfdevice, runJSON)

        '''run IDF and the associated batch file to export the custom csv output'''
        idfdevice.run(verbose='q')
        os.system(r'CD C:\Users\Owner\OneDrive\Research\Masters Thesis\Cosimulation\SmallOffice')
        os.system('CustomCSV SO OUTPUT')

        '''record output data points'''
        outputSet = smallofficeoutputs('SO_OUTPUT_hourly.csv')
        epElecEnergy = np.vstack((epElecEnergy, outputSet.elecEnergy))
        epPMV = np.vstack((epPMV, outputSet.allPMV_mean1))
        epHeatEnergy = np.vstack((epHeatEnergy, outputSet.allHE_sum1))
        epLightsEnergy = np.vstack((epLightsEnergy, outputSet.allLE_sum1))
        epEquipEnergy = np.vstack((epEquipEnergy, outputSet.allEEE_sum1))
        print('=== epElecEnergy Shape is (%d, %d)' % (epElecEnergy.shape[0], epElecEnergy.shape[1]))
        print('=== epPMV Shape is (%d, %d)' % (epPMV.shape[0], epPMV.shape[1]))
        print('=== epHeatEnergy Shape is (%d, %d)' % (epHeatEnergy.shape[0], epHeatEnergy.shape[1]))
        print('=== epLightsEnergy Shape is (%d, %d)' % (epLightsEnergy.shape[0], epLightsEnergy.shape[1]))
        print('=== epEquipEnergy Shape is (%d, %d)' % (epEquipEnergy.shape[0], epElecEnergy.shape[1]))

    '''save energy plus output arrays'''
    print(DateTime)
    np.save(DateTimeFile, DateTime)
    np.save(elecEnergyFile, epElecEnergy)
    np.save(PMVFile, epPMV)
    np.save(heatEnergyFile, epHeatEnergy)
    np.save(lightsEnergyFile, epLightsEnergy)
    np.save(equipEnergyFile, epEquipEnergy)

    '''print size as check'''
    print('====== all energy output arays (shape = (%d, %d)) saved successfully ======' % (epPMV.shape[0], epPMV.shape[1]))