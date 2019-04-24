'''
Kaden Plewe
04/15/2019
This class loads the energy plus simulation data that will be used for the uncertainty analysis
'''

import numpy as np
import pandas as pd
from functools import reduce

class epData:
    def __init__(self, epFilePath, pectFilePath, fileSampleN, N=100):
        '''calculates basic output parameters'''
        '''Emissions and Water Usage Calculation'''
        summerEx = pd.read_excel(pectFilePath[0], sheetname='Results')
        winterEx = pd.read_excel(pectFilePath[1], sheetname='Results')

        '''winter'''
        self.winterCoalGrid = winterEx['Coal Production [MWh]']
        self.winterNatgasGrid = winterEx['Natural Gas Production [MWh]']
        self.winterNuclearGrid = winterEx['Nuclear Production [MWh]']
        self.winterSolarpvGrid = winterEx['Solar PV Production [MWh]']
        self.winterSolarthGrid = winterEx['Solar Thermal Production [MWh]']
        self.winterWindGrid = winterEx['Wind Production [MWh]']
        self.winterGeoGrid = winterEx['Geothermal Production [MWh]']
        self.winterBiomassGrid = winterEx['Bio-Mass Production [MWh]']
        self.winterBiogasGrid = winterEx['Bio-Gas Production [MWh]']
        self.winterCO2Grid = winterEx['CO2 [lbs]']
        self.winterNOxGrid = winterEx['NOx [lbs]']
        self.winterSO2Grid = winterEx['SO2 [lbs]']
        self.winterWithdrawalGrid = winterEx['Water Withdrawal [gal]']
        self.winterConsumptionGrid = winterEx['Water Consumption [gal]']
        self.winterTotalGen = self.winterCoalGrid + self.winterNatgasGrid + self.winterNuclearGrid + self.winterSolarpvGrid\
                              + self.winterSolarthGrid + self.winterWindGrid + self.winterGeoGrid + self.winterBiomassGrid\
                              + self.winterBiogasGrid
        self.winterCO2EF = np.divide(self.winterCO2Grid, self.winterTotalGen)
        self.winterNOxEF = np.divide(self.winterNOxGrid, self.winterTotalGen)
        self.winterSO2EF = np.divide(self.winterSO2Grid, self.winterTotalGen)
        self.winterWWF = np.divide(self.winterWithdrawalGrid, self.winterTotalGen)
        self.winterWCF = np.divide(self.winterConsumptionGrid, self.winterTotalGen)

        '''summer'''
        self.summerCoalGrid = summerEx['Coal Production [MWh]']
        self.summerNatgasGrid = summerEx['Natural Gas Production [MWh]']
        self.summerNuclearGrid = summerEx['Nuclear Production [MWh]']
        self.summerSolarpvGrid = summerEx['Solar PV Production [MWh]']
        self.summerSolarthGrid = summerEx['Solar Thermal Production [MWh]']
        self.summerWindGrid = summerEx['Wind Production [MWh]']
        self.summerGeoGrid = summerEx['Geothermal Production [MWh]']
        self.summerBiomassGrid = summerEx['Bio-Mass Production [MWh]']
        self.summerBiogasGrid = summerEx['Bio-Gas Production [MWh]']
        self.summerCO2Grid = summerEx['CO2 [lbs]']
        self.summerNOxGrid = summerEx['NOx [lbs]']
        self.summerSO2Grid = summerEx['SO2 [lbs]']
        self.summerWithdrawalGrid = summerEx['Water Withdrawal [gal]']
        self.summerConsumptionGrid = summerEx['Water Consumption [gal]']
        self.summerTotalGen = self.summerCoalGrid + self.summerNatgasGrid + self.summerNuclearGrid + self.summerSolarpvGrid\
                              + self.summerSolarthGrid + self.summerWindGrid + self.summerGeoGrid + self.summerBiomassGrid\
                              + self.summerBiogasGrid
        self.summerCO2EF = np.divide(self.summerCO2Grid, self.summerTotalGen)
        self.summerNOxEF = np.divide(self.summerNOxGrid, self.summerTotalGen)
        self.summerSO2EF = np.divide(self.summerSO2Grid, self.summerTotalGen)
        self.summerWWF = np.divide(self.summerWithdrawalGrid, self.summerTotalGen)
        self.summerWCF = np.divide(self.summerConsumptionGrid, self.summerTotalGen)


        '''loads data from the specified file location'''

        '''date time array for summer and winter'''
        self.DateTimeS = np.load('%s\epDateTimeS.npy' % epFilePath)
        self.DateTimeW = np.load('%s\epDateTimeW.npy' % epFilePath)

        '''total electric energy for winter and summer [MJ]'''
        self.TotalElecEnergyNomW = np.load('%s\epTotalElecEnergyAllW%d.npy' % (epFilePath, fileSampleN))[0, :]/1000000
        self.TotalElecEnergyALLW = np.load('%s\epTotalElecEnergyAllW%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]/1000000
        self.TotalElecEnergySET1W = np.load('%s\epTotalElecEnergySET1W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]/1000000
        self.TotalElecEnergySET2W = np.load('%s\epTotalElecEnergySET2W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]/1000000
        self.TotalElecEnergySET3W = np.load('%s\epTotalElecEnergySET3W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]/1000000

        self.TotalElecEnergyNomS = np.load('%s\epTotalElecEnergyAllS%d.npy' % (epFilePath, fileSampleN))[0, :]/1000000
        self.TotalElecEnergyALLS = np.load('%s\epTotalElecEnergyAllS%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]/1000000
        self.TotalElecEnergySET1S = np.load('%s\epTotalElecEnergySET1S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]/1000000
        self.TotalElecEnergySET2S = np.load('%s\epTotalElecEnergySET2S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]/1000000
        self.TotalElecEnergySET3S = np.load('%s\epTotalElecEnergySET3S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]/1000000

        '''hourly co2 emissions calculations'''
        self.CO2NomW = self.TotalElecEnergyNomW*np.asarray([self.winterCO2EF])/3600
        self.CO2ALLW = self.TotalElecEnergyALLW*np.asarray([self.winterCO2EF])/3600
        self.CO2SET1W = self.TotalElecEnergySET1W*np.asarray([self.winterCO2EF])/3600
        self.CO2SET2W = self.TotalElecEnergySET2W*np.asarray([self.winterCO2EF])/3600
        self.CO2SET3W = self.TotalElecEnergySET3W*np.asarray([self.winterCO2EF])/3600

        self.CO2NomS = self.TotalElecEnergyNomS*np.asarray([self.summerCO2EF])/3600
        self.CO2ALLS = self.TotalElecEnergyALLS*np.asarray([self.summerCO2EF])/3600
        self.CO2SET1S = self.TotalElecEnergySET1S*np.asarray([self.summerCO2EF])/3600
        self.CO2SET2S = self.TotalElecEnergySET2S*np.asarray([self.summerCO2EF])/3600
        self.CO2SET3S = self.TotalElecEnergySET3S*np.asarray([self.summerCO2EF])/3600

        '''hourly nox emissions calculations'''
        self.NOxNomW = self.TotalElecEnergyNomW*np.asarray([self.winterNOxEF])/3600
        self.NOxALLW = self.TotalElecEnergyALLW*np.asarray([self.winterNOxEF])/3600
        self.NOxSET1W = self.TotalElecEnergySET1W*np.asarray([self.winterNOxEF])/3600
        self.NOxSET2W = self.TotalElecEnergySET2W*np.asarray([self.winterNOxEF])/3600
        self.NOxSET3W = self.TotalElecEnergySET3W*np.asarray([self.winterNOxEF])/3600

        self.NOxNomS = self.TotalElecEnergyNomS*np.asarray([self.summerNOxEF])/3600
        self.NOxALLS = self.TotalElecEnergyALLS*np.asarray([self.summerNOxEF])/3600
        self.NOxSET1S = self.TotalElecEnergySET1S*np.asarray([self.summerNOxEF])/3600
        self.NOxSET2S = self.TotalElecEnergySET2S*np.asarray([self.summerNOxEF])/3600
        self.NOxSET3S = self.TotalElecEnergySET3S*np.asarray([self.summerNOxEF])/3600

        '''hourly so2 emissions calculations'''
        self.SO2NomW = self.TotalElecEnergyNomW*np.asarray([self.winterSO2EF])/3600
        self.SO2ALLW = self.TotalElecEnergyALLW*np.asarray([self.winterSO2EF])/3600
        self.SO2SET1W = self.TotalElecEnergySET1W*np.asarray([self.winterSO2EF])/3600
        self.SO2SET2W = self.TotalElecEnergySET2W*np.asarray([self.winterSO2EF])/3600
        self.SO2SET3W = self.TotalElecEnergySET3W*np.asarray([self.winterSO2EF])/3600

        self.SO2NomS = self.TotalElecEnergyNomS*np.asarray([self.summerSO2EF])/3600
        self.SO2ALLS = self.TotalElecEnergyALLS*np.asarray([self.summerSO2EF])/3600
        self.SO2SET1S = self.TotalElecEnergySET1S*np.asarray([self.summerSO2EF])/3600
        self.SO2SET2S = self.TotalElecEnergySET2S*np.asarray([self.summerSO2EF])/3600
        self.SO2SET3S = self.TotalElecEnergySET3S*np.asarray([self.summerSO2EF])/3600

        '''hourly water consumption calculations'''
        self.WCNomW = self.TotalElecEnergyNomW*np.asarray([self.winterWCF])/3600
        self.WCALLW = self.TotalElecEnergyALLW*np.asarray([self.winterWCF])/3600
        self.WCSET1W = self.TotalElecEnergySET1W*np.asarray([self.winterWCF])/3600
        self.WCSET2W = self.TotalElecEnergySET2W*np.asarray([self.winterWCF])/3600
        self.WCSET3W = self.TotalElecEnergySET3W*np.asarray([self.winterWCF])/3600

        self.WCNomS = self.TotalElecEnergyNomS*np.asarray([self.summerWCF])/3600
        self.WCALLS = self.TotalElecEnergyALLS*np.asarray([self.summerWCF])/3600
        self.WCSET1S = self.TotalElecEnergySET1S*np.asarray([self.summerWCF])/3600
        self.WCSET2S = self.TotalElecEnergySET2S*np.asarray([self.summerWCF])/3600
        self.WCSET3S = self.TotalElecEnergySET3S*np.asarray([self.summerWCF])/3600

        '''hourly water withdrawal calculations'''
        self.WWNomW = self.TotalElecEnergyNomW*np.asarray([self.winterWWF])/3600
        self.WWALLW = self.TotalElecEnergyALLW*np.asarray([self.winterWWF])/3600
        self.WWSET1W = self.TotalElecEnergySET1W*np.asarray([self.winterWWF])/3600
        self.WWSET2W = self.TotalElecEnergySET2W*np.asarray([self.winterWWF])/3600
        self.WWSET3W = self.TotalElecEnergySET3W*np.asarray([self.winterWWF])/3600

        self.WWNomS = self.TotalElecEnergyNomS*np.asarray([self.summerWWF])/3600
        self.WWALLS = self.TotalElecEnergyALLS*np.asarray([self.summerWWF])/3600
        self.WWSET1S = self.TotalElecEnergySET1S*np.asarray([self.summerWWF])/3600
        self.WWSET2S = self.TotalElecEnergySET2S*np.asarray([self.summerWWF])/3600
        self.WWSET3S = self.TotalElecEnergySET3S*np.asarray([self.summerWWF])/3600


        '''total elec energy (PACKED)'''
        self.pdTotalElecEnergyALLW1 = pd.DataFrame([i for i in np.ndenumerate(self.TotalElecEnergyALLW)],
                                                  columns=('idx', 'allw val'))
        self.pdTotalElecEnergyALLW = pd.DataFrame([self.pdTotalElecEnergyALLW1['idx'][i][1] for i in
                                                   range(len(self.pdTotalElecEnergyALLW1['idx']))], columns=('hour',)).join(self.pdTotalElecEnergyALLW1)
        self.pdTotalElecEnergySET1W = pd.DataFrame([i for i in np.ndenumerate(self.TotalElecEnergySET1W)],
                                                  columns=('idx', 'set1w val'))
        self.pdTotalElecEnergySET2W = pd.DataFrame([i for i in np.ndenumerate(self.TotalElecEnergySET2W)],
                                                  columns=('idx', 'set2w val'))
        self.pdTotalElecEnergySET3W = pd.DataFrame([i for i in np.ndenumerate(self.TotalElecEnergySET3W)],
                                                  columns=('idx', 'set3w val'))
        self.pdTotalElecEnergyALLS = pd.DataFrame([i for i in np.ndenumerate(self.TotalElecEnergyALLS)],
                                                  columns=('idx', 'alls val'))
        self.pdTotalElecEnergySET1S = pd.DataFrame([i for i in np.ndenumerate(self.TotalElecEnergySET1S)],
                                                  columns=('idx', 'set1s val'))
        self.pdTotalElecEnergySET2S = pd.DataFrame([i for i in np.ndenumerate(self.TotalElecEnergySET2S)],
                                                  columns=('idx', 'set2s val'))
        self.pdTotalElecEnergySET3S = pd.DataFrame([i for i in np.ndenumerate(self.TotalElecEnergySET3S)],
                                                  columns=('idx','set3s val'))
        self.pdTotalElecEnergy = reduce(lambda left,right: pd.merge(left, right, on='idx'),
                                        [self.pdTotalElecEnergyALLW, self.pdTotalElecEnergySET1W,
                                         self.pdTotalElecEnergySET2W, self.pdTotalElecEnergySET3W,
                                         self.pdTotalElecEnergyALLS, self.pdTotalElecEnergySET1S,
                                         self.pdTotalElecEnergySET2S, self.pdTotalElecEnergySET3S])

        '''CO2 (PACKED)'''
        self.pdCO2ALLW1 = pd.DataFrame([i for i in np.ndenumerate(self.CO2ALLW)],
                                                  columns=('idx', 'allw val'))
        self.pdCO2ALLW = pd.DataFrame([self.pdCO2ALLW1['idx'][i][1] for i in range(len(self.pdCO2ALLW1['idx']))],
                                                  columns=('hour',)).join(self.pdCO2ALLW1)
        self.pdCO2SET1W = pd.DataFrame([i for i in np.ndenumerate(self.CO2SET1W)], columns=('idx', 'set1w val'))
        self.pdCO2SET2W = pd.DataFrame([i for i in np.ndenumerate(self.CO2SET2W)], columns=('idx', 'set2w val'))
        self.pdCO2SET3W = pd.DataFrame([i for i in np.ndenumerate(self.CO2SET3W)], columns=('idx', 'set3w val'))
        self.pdCO2ALLS = pd.DataFrame([i for i in np.ndenumerate(self.CO2ALLS)], columns=('idx', 'alls val'))
        self.pdCO2SET1S = pd.DataFrame([i for i in np.ndenumerate(self.CO2SET1S)], columns=('idx', 'set1s val'))
        self.pdCO2SET2S = pd.DataFrame([i for i in np.ndenumerate(self.CO2SET2S)], columns=('idx', 'set2s val'))
        self.pdCO2SET3S = pd.DataFrame([i for i in np.ndenumerate(self.CO2SET3S)], columns=('idx', 'set3s val'))
        self.pdCO2 = reduce(lambda left, right: pd.merge(left, right, on='idx'),
                                        [self.pdCO2ALLW, self.pdCO2SET1W, self.pdCO2SET2W, self.pdCO2SET3W,
                                         self.pdCO2ALLS, self.pdCO2SET1S, self.pdCO2SET2S, self.pdCO2SET3S])



        '''all zone average pmv for winter and summer'''
        self.AvePMVNomW = np.load('%s\epAvePMVAllW%d.npy' % (epFilePath, fileSampleN))[0, :]
        self.AvePMVALLW = np.load('%s\epAvePMVAllW%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.AvePMVSET1W = np.load('%s\epAvePMVSET1W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.AvePMVSET2W = np.load('%s\epAvePMVSET2W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.AvePMVSET3W = np.load('%s\epAvePMVSET3W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]

        self.AvePMVNomS = np.load('%s\epAvePMVAllS%d.npy' % (epFilePath, fileSampleN))[0, :]
        self.AvePMVALLS = np.load('%s\epAvePMVAllS%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.AvePMVSET1S = np.load('%s\epAvePMVSET1S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.AvePMVSET2S = np.load('%s\epAvePMVSET2S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.AvePMVSET3S = np.load('%s\epAvePMVSET3S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]

        '''(PACKED)'''
        self.pdAvePMVALLW1 = pd.DataFrame([i for i in np.ndenumerate(self.AvePMVALLW)],
                                                  columns=('idx', 'allw val'))
        self.pdAvePMVALLW = pd.DataFrame([self.pdAvePMVALLW1['idx'][i][1] for i in
                                                   range(len(self.pdAvePMVALLW1['idx']))], columns=('hour',)).join(self.pdAvePMVALLW1)
        self.pdAvePMVSET1W = pd.DataFrame([i for i in np.ndenumerate(self.AvePMVSET1W)],
                                                  columns=('idx', 'set1w val'))
        self.pdAvePMVSET2W = pd.DataFrame([i for i in np.ndenumerate(self.AvePMVSET2W)],
                                                  columns=('idx', 'set2w val'))
        self.pdAvePMVSET3W = pd.DataFrame([i for i in np.ndenumerate(self.AvePMVSET3W)],
                                                  columns=('idx', 'set3w val'))
        self.pdAvePMVALLS = pd.DataFrame([i for i in np.ndenumerate(self.AvePMVALLS)],
                                                  columns=('idx', 'alls val'))
        self.pdAvePMVSET1S = pd.DataFrame([i for i in np.ndenumerate(self.AvePMVSET1S)],
                                                  columns=('idx', 'set1s val'))
        self.pdAvePMVSET2S = pd.DataFrame([i for i in np.ndenumerate(self.AvePMVSET2S)],
                                                  columns=('idx', 'set2s val'))
        self.pdAvePMVSET3S = pd.DataFrame([i for i in np.ndenumerate(self.AvePMVSET3S)],
                                                  columns=('idx','set3s val'))
        self.pdAvePMV = reduce(lambda left,right: pd.merge(left, right, on='idx'),
                                        [self.pdAvePMVALLW, self.pdAvePMVSET1W,
                                         self.pdAvePMVSET2W, self.pdAvePMVSET3W,
                                         self.pdAvePMVALLS, self.pdAvePMVSET1S,
                                         self.pdAvePMVSET2S, self.pdAvePMVSET3S])

        '''all zone sum heating energy for winter and summer'''
        self.HeatEnergyNomW = np.load('%s\epHeatEnergyAllW%d.npy' % (epFilePath, fileSampleN))[0, :]
        self.HeatEnergyALLW = np.load('%s\epHeatEnergyAllW%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.HeatEnergySET1W = np.load('%s\epHeatEnergySET1W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.HeatEnergySET2W = np.load('%s\epHeatEnergySET2W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.HeatEnergySET3W = np.load('%s\epHeatEnergySET3W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]

        self.HeatEnergyNomS = np.load('%s\epHeatEnergyAllS%d.npy' % (epFilePath, fileSampleN))[0, :]
        self.HeatEnergyALLS = np.load('%s\epHeatEnergyAllS%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.HeatEnergySET1S = np.load('%s\epHeatEnergySET1S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.HeatEnergySET2S = np.load('%s\epHeatEnergySET2S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.HeatEnergySET3S = np.load('%s\epHeatEnergySET3S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]

        '''(PACKED)'''
        self.pdHeatEnergyALLW1 = pd.DataFrame([i for i in np.ndenumerate(self.HeatEnergyALLW)],
                                                  columns=('idx', 'allw val'))
        self.pdHeatEnergyALLW = pd.DataFrame([self.pdHeatEnergyALLW1['idx'][i][1] for i in
                                                   range(len(self.pdHeatEnergyALLW1['idx']))], columns=('hour',)).join(self.pdHeatEnergyALLW1)
        self.pdHeatEnergySET1W = pd.DataFrame([i for i in np.ndenumerate(self.HeatEnergySET1W)],
                                                  columns=('idx', 'set1w val'))
        self.pdHeatEnergySET2W = pd.DataFrame([i for i in np.ndenumerate(self.HeatEnergySET2W)],
                                                  columns=('idx', 'set2w val'))
        self.pdHeatEnergySET3W = pd.DataFrame([i for i in np.ndenumerate(self.HeatEnergySET3W)],
                                                  columns=('idx', 'set3w val'))
        self.pdHeatEnergyALLS = pd.DataFrame([i for i in np.ndenumerate(self.HeatEnergyALLS)],
                                                  columns=('idx', 'alls val'))
        self.pdHeatEnergySET1S = pd.DataFrame([i for i in np.ndenumerate(self.HeatEnergySET1S)],
                                                  columns=('idx', 'set1s val'))
        self.pdHeatEnergySET2S = pd.DataFrame([i for i in np.ndenumerate(self.HeatEnergySET2S)],
                                                  columns=('idx', 'set2s val'))
        self.pdHeatEnergySET3S = pd.DataFrame([i for i in np.ndenumerate(self.HeatEnergySET3S)],
                                                  columns=('idx','set3s val'))
        self.pdHeatEnergy = reduce(lambda left,right: pd.merge(left, right, on='idx'),
                                        [self.pdHeatEnergyALLW, self.pdHeatEnergySET1W,
                                         self.pdHeatEnergySET2W, self.pdHeatEnergySET3W,
                                         self.pdHeatEnergyALLS, self.pdHeatEnergySET1S,
                                         self.pdHeatEnergySET2S, self.pdHeatEnergySET3S])

        '''all zone sum equipment energy for winter and summer'''
        self.EquipEnergyNomW = np.load('%s\epEquipEnergyAllW%d.npy' % (epFilePath, fileSampleN))[0, :]
        self.EquipEnergyALLW = np.load('%s\epEquipEnergyAllW%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.EquipEnergySET1W = np.load('%s\epEquipEnergySET1W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.EquipEnergySET2W = np.load('%s\epEquipEnergySET2W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.EquipEnergySET3W = np.load('%s\epEquipEnergySET3W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]

        self.EquipEnergyNomS = np.load('%s\epEquipEnergyAllS%d.npy' % (epFilePath, fileSampleN))[0, :]
        self.EquipEnergyALLS = np.load('%s\epEquipEnergyAllS%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.EquipEnergySET1S = np.load('%s\epEquipEnergySET1S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.EquipEnergySET2S = np.load('%s\epEquipEnergySET2S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.EquipEnergySET3S = np.load('%s\epEquipEnergySET3S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]

        '''(PACKED)'''
        self.pdEquipEnergyALLW1 = pd.DataFrame([i for i in np.ndenumerate(self.EquipEnergyALLW)],
                                                  columns=('idx', 'allw val'))
        self.pdEquipEnergyALLW = pd.DataFrame([self.pdEquipEnergyALLW1['idx'][i][1] for i in
                                                   range(len(self.pdEquipEnergyALLW1['idx']))], columns=('hour',)).join(self.pdEquipEnergyALLW1)
        self.pdEquipEnergySET1W = pd.DataFrame([i for i in np.ndenumerate(self.EquipEnergySET1W)],
                                                  columns=('idx', 'set1w val'))
        self.pdEquipEnergySET2W = pd.DataFrame([i for i in np.ndenumerate(self.EquipEnergySET2W)],
                                                  columns=('idx', 'set2w val'))
        self.pdEquipEnergySET3W = pd.DataFrame([i for i in np.ndenumerate(self.EquipEnergySET3W)],
                                                  columns=('idx', 'set3w val'))
        self.pdEquipEnergyALLS = pd.DataFrame([i for i in np.ndenumerate(self.EquipEnergyALLS)],
                                                  columns=('idx', 'alls val'))
        self.pdEquipEnergySET1S = pd.DataFrame([i for i in np.ndenumerate(self.EquipEnergySET1S)],
                                                  columns=('idx', 'set1s val'))
        self.pdEquipEnergySET2S = pd.DataFrame([i for i in np.ndenumerate(self.EquipEnergySET2S)],
                                                  columns=('idx', 'set2s val'))
        self.pdEquipEnergySET3S = pd.DataFrame([i for i in np.ndenumerate(self.EquipEnergySET3S)],
                                                  columns=('idx','set3s val'))
        self.pdEquipEnergy = reduce(lambda left,right: pd.merge(left, right, on='idx'),
                                        [self.pdEquipEnergyALLW, self.pdEquipEnergySET1W,
                                         self.pdEquipEnergySET2W, self.pdEquipEnergySET3W,
                                         self.pdEquipEnergyALLS, self.pdEquipEnergySET1S,
                                         self.pdEquipEnergySET2S, self.pdEquipEnergySET3S])

        '''all zone sum lights energy for winter and summer'''
        self.LightsEnergyNomW = np.load('%s\epLightsEnergyAllW%d.npy' % (epFilePath, fileSampleN))[0, :]
        self.LightsEnergyALLW = np.load('%s\epLightsEnergyAllW%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.LightsEnergySET1W = np.load('%s\epLightsEnergySET1W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.LightsEnergySET2W = np.load('%s\epLightsEnergySET2W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.LightsEnergySET3W = np.load('%s\epLightsEnergySET3W%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]

        self.LightsEnergyNomS = np.load('%s\epLightsEnergyAllS%d.npy' % (epFilePath, fileSampleN))[0, :]
        self.LightsEnergyALLS = np.load('%s\epLightsEnergyAllS%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.LightsEnergySET1S = np.load('%s\epLightsEnergySET1S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.LightsEnergySET2S = np.load('%s\epLightsEnergySET2S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]
        self.LightsEnergySET3S = np.load('%s\epLightsEnergySET3S%d.npy' % (epFilePath, fileSampleN))[1:N+1, :]

        '''(PACKED)'''
        self.pdLightsEnergyALLW1 = pd.DataFrame([i for i in np.ndenumerate(self.LightsEnergyALLW)],
                                                  columns=('idx', 'allw val'))
        self.pdLightsEnergyALLW = pd.DataFrame([self.pdLightsEnergyALLW1['idx'][i][1] for i in
                                                   range(len(self.pdLightsEnergyALLW1['idx']))], columns=('hour',)).join(self.pdLightsEnergyALLW1)
        self.pdLightsEnergySET1W = pd.DataFrame([i for i in np.ndenumerate(self.LightsEnergySET1W)],
                                                  columns=('idx', 'set1w val'))
        self.pdLightsEnergySET2W = pd.DataFrame([i for i in np.ndenumerate(self.LightsEnergySET2W)],
                                                  columns=('idx', 'set2w val'))
        self.pdLightsEnergySET3W = pd.DataFrame([i for i in np.ndenumerate(self.LightsEnergySET3W)],
                                                  columns=('idx', 'set3w val'))
        self.pdLightsEnergyALLS = pd.DataFrame([i for i in np.ndenumerate(self.LightsEnergyALLS)],
                                                  columns=('idx', 'alls val'))
        self.pdLightsEnergySET1S = pd.DataFrame([i for i in np.ndenumerate(self.LightsEnergySET1S)],
                                                  columns=('idx', 'set1s val'))
        self.pdLightsEnergySET2S = pd.DataFrame([i for i in np.ndenumerate(self.LightsEnergySET2S)],
                                                  columns=('idx', 'set2s val'))
        self.pdLightsEnergySET3S = pd.DataFrame([i for i in np.ndenumerate(self.LightsEnergySET3S)],
                                                  columns=('idx','set3s val'))
        self.pdLightsEnergy = reduce(lambda left,right: pd.merge(left, right, on='idx'),
                                        [self.pdLightsEnergyALLW, self.pdLightsEnergySET1W,
                                         self.pdLightsEnergySET2W, self.pdLightsEnergySET3W,
                                         self.pdLightsEnergyALLS, self.pdLightsEnergySET1S,
                                         self.pdLightsEnergySET2S, self.pdLightsEnergySET3S])


    def stats(self, Data):
        '''extracts the mean and standard deviation at each time step for each data set should be 2
            rows and the number of columns corresponding to the time steps'''
        return np.vstack((np.mean(Data, 0), np.std(Data, 0)))

