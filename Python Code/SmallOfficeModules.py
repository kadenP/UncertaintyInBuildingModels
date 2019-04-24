'''
this class configures the small office idf file in order to set up the correct outputs and simulation run parameters
'''
class configuresmalloffice:
    def __init__(self, idfdevice, beginMonth, beginDayOfMonth, endMonth, endDayOfMonth):
        '''updates all necessary fields and declares the output variables. Note that the global variable idfdevice
            must exist as the current eppy idf object in the script'''

        '''update the run period fields'''
        for object in idfdevice.idfobjects['RUNPERIOD']:
            object.Begin_Month = beginMonth
            object.Begin_Day_of_Month = beginDayOfMonth
            object.End_Month = endMonth
            object.End_Day_of_Month = endDayOfMonth

        '''update the simulation control variables'''
        for object in idfdevice.idfobjects['SIMULATIONCONTROL']:
            object.Do_Zone_Sizing_Calculation = 'Yes'
            object.Do_System_Sizing_Calculation = 'Yes'
            object.Do_Plant_Sizing_Calculation = 'Yes'
            object.Run_Simulation_for_Sizing_Periods = 'No'
            object.Run_Simulation_for_Weather_File_Run_Periods = 'Yes'
            print('=== Sumulation Control Parameters Changed ===')

        '''add thermal comfort model to people objects'''
        for object in idfdevice.idfobjects['PEOPLE']:
            object.Surface_NameAngle_Factor_List_Name = ''
            object.Work_Efficiency_Schedule_Name = 'WORK_EFF_SCH'
            object.Clothing_Insulation_Schedule_Name = 'CLOTHING_SCH'
            object.Air_Velocity_Schedule_Name = 'AIR_VELO_SCH'
            object.Thermal_Comfort_Model_1_Type = 'Fanger'

        '''Fanger PMV thermal comfort model (Zone Average)'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Zone Thermal Comfort Fanger Model PMV'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Zone Thermal Comfort Fanger Model PMV'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Timestep'

        '''Fanger PPD thermal comfort model (Zone Average)'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Zone Thermal Comfort Fanger Model PPD'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Total Purchase Electric Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Facility Total Purchased Electric Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Total Zone Internal Heating Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Zone Total Internal Total Heating Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Lights Electric Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Lights Electric Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Electric Equipment Electric Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Electric Equipment Electric Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Water Heater Heating Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Water Heater Heating Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Zone Air System Sensible Heating Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Zone Air System Sensible Heating Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Zone Air System Sensible Cooling Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Zone Air System Sensible Cooling Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Hourly cooling temperature setpoint [°C]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Zone Thermostat Cooling Setpoint Temperature'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Hourly heating temperature setpoint [°C]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Zone Thermostat Heating Setpoint Temperature'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Zone thermostat air temperature [°C]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Zone Thermostat Air Temperature'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Fan Electric Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Fan Electric Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Cooling Coil Electric Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Cooling Coil Electric Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Heating Coil Electric Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Heating Coil Electric Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Heating Coil Gas Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Heating Coil Gas Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Pump Electric Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Pump Electric Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Air System Total Cooling Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Air System Total Cooling Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'

        '''Air System Total Heating Energy [J]'''
        idfdevice.newidfobject('OUTPUT:VARIABLE')
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Air System Total Heating Energy'
        idfdevice.idfobjects['OUTPUT:VARIABLE'][-1].Reporting_Frequency = 'Hourly'


'''this class reads the output file for an energy plus simulation and makes them available as scalars and arrays'''
import csv
from collections import defaultdict
import numpy as np

class smallofficeoutputs:
    def __init__(self, output_filename):
        '''Read csv file into new data dictionary and set variable arrays'''
        newEntry = defaultdict(list)
        with open(output_filename, newline='') as newFile:
            newData = csv.DictReader(newFile)
            for row in newData:
                [newEntry[key].append(value) for key, value in row.items()]

        '''raw data'''

        '''Date/Time array'''
        self.DateTime = np.asarray(newEntry['Date/Time'], dtype=str)

        '''PMV values for core zone'''
        self.corePMV = np.asarray(newEntry['CORE_ZN:Zone Thermal Comfort Fanger Model PMV [](Hourly)'],
                                  dtype=np.float32)
        self.corePMV_mean = np.mean(self.corePMV)
        self.corePMV_max = np.max(self.corePMV)
        self.corePMV_min = np.min(self.corePMV)

        '''PMV values for zone 1'''
        self.zn1PMV = np.asarray(newEntry['PERIMETER_ZN_1:Zone Thermal Comfort Fanger Model PMV [](Hourly)'],
                                 dtype=np.float32)
        self.zn1PMV_mean = np.mean(self.zn1PMV)
        self.zn1PMV_max = np.max(self.zn1PMV)
        self.zn1PMV_min = np.min(self.zn1PMV)

        '''PMV values for zone 2'''
        self.zn2PMV = np.asarray(newEntry['PERIMETER_ZN_2:Zone Thermal Comfort Fanger Model PMV [](Hourly)'],
                                 dtype=np.float32)
        self.zn2PMV_mean = np.mean(self.zn2PMV)
        self.zn2PMV_max = np.max(self.zn2PMV)
        self.zn2PMV_min = np.min(self.zn2PMV)


        '''PMV values for zone 3'''
        self.zn3PMV = np.asarray(newEntry['PERIMETER_ZN_3:Zone Thermal Comfort Fanger Model PMV [](Hourly)'],
                                 dtype=np.float32)
        self.zn3PMV_mean = np.mean(self.zn3PMV)
        self.zn3PMV_max = np.max(self.zn3PMV)
        self.zn3PMV_min = np.min(self.zn3PMV)

        '''PMV values for zone 4'''
        self.zn4PMV = np.asarray(newEntry['PERIMETER_ZN_4:Zone Thermal Comfort Fanger Model PMV [](Hourly)'],
                                 dtype=np.float32)
        self.zn4PMV_mean = np.mean(self.zn4PMV)
        self.zn4PMV_max = np.max(self.zn4PMV)
        self.zn4PMV_min = np.min(self.zn4PMV)

        '''PMV values for all zones'''
        self.allPMV = np.asarray([[self.corePMV], [self.zn1PMV], [self.zn2PMV], [self.zn3PMV], [self.zn4PMV]])
        self.allPMV_mean1 = np.mean(self.allPMV, 0)
        self.allPMV_mean2 = np.mean(self.allPMV_mean1)
        self.allPMV_max = np.max(self.allPMV)
        self.allPMV_min = np.min(self.allPMV)

        '''PPD values for core zone'''
        self.corePPD = np.asarray(newEntry['CORE_ZN:Zone Thermal Comfort Fanger Model PPD [%](Hourly)'],
                                  dtype=np.float32)
        self.corePPD_mean = np.mean(self.corePPD)
        self.corePPD_max = np.max(self.corePPD)
        self.corePPD_min = np.min(self.corePPD)

        '''PPD values for zone 1'''
        self.zn1PPD = np.asarray(newEntry['PERIMETER_ZN_1:Zone Thermal Comfort Fanger Model PPD [%](Hourly)'],
                                 dtype=np.float32)
        self.zn1PPD_mean = np.mean(self.zn1PPD)
        self.zn1PPD_max = np.max(self.zn1PPD)
        self.zn1PPD_min = np.min(self.zn1PPD)

        '''PPD values for zone 2'''
        self.zn2PPD = np.asarray(newEntry['PERIMETER_ZN_2:Zone Thermal Comfort Fanger Model PPD [%](Hourly)'],
                                 dtype=np.float32)
        self.zn2PPD_mean = np.mean(self.zn2PPD)
        self.zn2PPD_max = np.max(self.zn2PPD)
        self.zn2PPD_min = np.min(self.zn2PPD)

        '''PPD values for zone 3'''
        self.zn3PPD = np.asarray(newEntry['PERIMETER_ZN_3:Zone Thermal Comfort Fanger Model PPD [%](Hourly)'],
                                 dtype=np.float32)
        self.zn3PPD_mean = np.mean(self.zn3PPD)
        self.zn3PPD_max = np.max(self.zn3PPD)
        self.zn3PPD_min = np.min(self.zn3PPD)

        '''PPD values for zone 4'''
        self.zn4PPD = np.asarray(newEntry['PERIMETER_ZN_4:Zone Thermal Comfort Fanger Model PPD [%](Hourly)'],
                                 dtype=np.float32)
        self.zn4PPD_mean = np.mean(self.zn4PPD)
        self.zn4PPD_max = np.max(self.zn4PPD)
        self.zn4PPD_min = np.min(self.zn4PPD)

        '''PPD values for all zones'''
        self.allPPD = np.asarray([[self.corePPD], [self.zn1PPD], [self.zn2PPD], [self.zn3PPD], [self.zn4PPD]])
        self.allPPD_mean1 = np.mean(self.allPPD, 0)
        self.allPPD_mean2 = np.mean(self.allPPD_mean1)
        self.allPPD_max = np.max(self.allPPD)
        self.allPPD_min = np.min(self.allPPD)

        '''facility electric energy (J)'''
        self.elecEnergy = np.asarray(newEntry['Whole Building:Facility Total Purchased Electric Energy [J](Hourly)'],
                                       dtype=np.float32)
        self.elecEnergy_sum = np.sum(self.elecEnergy)


        '''Core Zone Heating Energy (J)'''
        self.coreHE = np.asarray(newEntry['CORE_ZN:Zone Total Internal Total Heating Energy [J](Hourly)'],
                       dtype=np.float32)
        self.coreHE_sum = np.sum(self.coreHE)

        '''Zone 1 Heating Energy (J)'''
        self.zn1HE = np.asarray(newEntry['PERIMETER_ZN_1:Zone Total Internal Total Heating Energy [J](Hourly)'],
                       dtype=np.float32)
        self.zn1HE_sum = np.sum(self.zn1HE)

        '''Zone 2 Heating Energy (J)'''
        self.zn2HE = np.asarray(newEntry['PERIMETER_ZN_2:Zone Total Internal Total Heating Energy [J](Hourly)'],
                       dtype=np.float32)
        self.zn2HE_sum = np.sum(self.zn2HE)

        '''Zone 3 Heating Energy (J)'''
        self.zn3HE = np.asarray(newEntry['PERIMETER_ZN_3:Zone Total Internal Total Heating Energy [J](Hourly)'],
                       dtype=np.float32)
        self.zn3HE_sum = np.sum(self.zn3HE)

        '''Zone 4 Heating Energy (J)'''
        self.zn4HE = np.asarray(newEntry['PERIMETER_ZN_4:Zone Total Internal Total Heating Energy [J](Hourly)'],
                       dtype=np.float32)
        self.zn4HE_sum = np.sum(self.zn4HE)

        '''All Zones Heating Energy (J)'''
        self.allHE = np.asarray([[self.coreHE], [self.zn1HE],[self.zn2HE], [self.zn3HE], [self.zn4HE]])
        self.allHE_sum1 = np.sum(self.allHE, 0)
        self.allHE_sum2 = np.sum(self.allHE)

        '''Core Zone Lights Electric Energy (J)'''
        self.coreLE = np.asarray(newEntry['CORE_ZN_LIGHTS:Lights Electric Energy [J](Hourly)'],
                       dtype=np.float32)
        self.coreLE_sum = np.sum(self.coreLE)

        '''Zone 1 Lights Electric Energy (J)'''
        self.zn1LE = np.asarray(newEntry['PERIMETER_ZN_1_LIGHTS:Lights Electric Energy [J](Hourly)'],
                                            dtype=np.float32)
        self.zn1LE_sum = np.sum(self.zn1LE)

        '''Zone 2 Lights Electric Energy (J)'''
        self.zn2LE = np.asarray(newEntry['PERIMETER_ZN_2_LIGHTS:Lights Electric Energy [J](Hourly)'],
                                       dtype=np.float32)
        self.zn2LE_sum = np.sum(self.zn2LE)

        '''Zone 3 Lights Electric Energy (J)'''
        self.zn3LE = np.asarray(newEntry['PERIMETER_ZN_3_LIGHTS:Lights Electric Energy [J](Hourly)'],
                                       dtype=np.float32)
        self.zn3LE_sum = np.sum(self.zn3LE)

        '''Zone 4 Lights Electric Energy (J)'''
        self.zn4LE = np.asarray(newEntry['PERIMETER_ZN_4_LIGHTS:Lights Electric Energy [J](Hourly)'],
                                       dtype=np.float32)
        self.zn4LE_sum = np.sum(self.zn4LE)

        '''All Zones Lights Electric Energy (J)'''
        self.allLE = np.asarray([[self.coreLE], [self.zn1LE], [self.zn2LE], [self.zn3LE], [self.zn4LE]])
        self.allLE_sum1 = np.sum(self.allLE, 0)
        self.allLE_sum2 = np.sum(self.allLE)

        '''Core Zone Electric Equipment Energy (J)'''
        self.coreEEE = np.asarray(newEntry['CORE_ZN_MISCPLUG_EQUIP:Electric Equipment Electric Energy [J](Hourly)'],
                                       dtype=np.float32)
        self.coreEEE_sum = np.sum(self.coreEEE)

        '''Zone 1 Electric Equipment Energy (J)'''
        self.zn1EEE = np.asarray(newEntry['PERIMETER_ZN_1_MISCPLUG_EQUIP:Electric Equipment Electric Energy [J](Hourly)'],
                                       dtype=np.float32)
        self.zn1EEE_sum = np.sum(self.zn1EEE)

        '''Zone 2 Electric Equipment Energy (J)'''
        self.zn2EEE = np.asarray(newEntry['PERIMETER_ZN_2_MISCPLUG_EQUIP:Electric Equipment Electric Energy [J](Hourly)'],
                                       dtype=np.float32)
        self.zn2EEE = np.sum(self.zn2EEE)

        '''Zone 3 Electric Equipment Energy (J)'''
        self.zn3EEE = np.asarray(newEntry['PERIMETER_ZN_3_MISCPLUG_EQUIP:Electric Equipment Electric Energy [J](Hourly)'],
                                       dtype=np.float32)
        self.zn3EEE_sum = np.sum(self.zn3EEE)

        '''Zone 4 Electric Equipment Energy (J)'''
        self.zn4EEE = np.asarray(newEntry['PERIMETER_ZN_4_MISCPLUG_EQUIP:Electric Equipment Electric Energy [J](Hourly)'],
                                       dtype=np.float32)
        self.zn4EEE_sum = np.sum(self.zn4EEE)

        '''All Zones Electric Equipment Energy (J)'''
        self.allEEE = np.asarray([[self.coreEEE], [self.zn1EEE], [self.zn2EEE], [self.zn3EEE], [self.zn4EEE]])
        self.allEEE_sum1 = np.sum(self.allEEE, 1)
        self.allEEE_sum2 = np.sum(self.allEEE)

        '''Core Zone Cooling Setpoint (°C)'''
        self.coreCS = np.asarray(newEntry['CORE_ZN:Zone Thermostat Cooling Setpoint Temperature [C](Hourly)'],
                                       dtype=np.float32)
        self.coreCS_mean = np.mean(self.coreCS)
        self.coreCS_max = np.max(self.coreCS)
        self.coreCS_min = np.min(self.coreCS)

        '''Zone 1 Cooling Setpoint (°C)'''
        self.zn1CS = np.asarray(newEntry['PERIMETER_ZN_1:Zone Thermostat Cooling Setpoint Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn1CS_mean = np.mean(self.zn1CS)
        self.zn1CS_max = np.max(self.zn1CS)
        self.zn1CS_min = np.min(self.zn1CS)

        '''Zone 2 Cooling Setpoint (°C)'''
        self.zn2CS = np.asarray(newEntry['PERIMETER_ZN_2:Zone Thermostat Cooling Setpoint Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn2CS_mean = np.mean(self.zn2CS)
        self.zn2CS_max = np.max(self.zn2CS)
        self.zn2CS_min = np.min(self.zn2CS)

        '''Zone 3 Cooling Setpoint (°C)'''
        self.zn3CS = np.asarray(newEntry['PERIMETER_ZN_3:Zone Thermostat Cooling Setpoint Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn3CS_mean = np.mean(self.zn3CS)
        self.zn3CS_max = np.max(self.zn3CS)
        self.zn3CS_min = np.min(self.zn3CS)

        '''Zone 4 Cooling Setpoint (°C)'''
        self.zn4CS = np.asarray(newEntry['PERIMETER_ZN_4:Zone Thermostat Cooling Setpoint Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn4CS_mean = np.mean(self.zn4CS)
        self.zn4CS_max = np.max(self.zn4CS)
        self.zn4CS_min = np.min(self.zn4CS)

        '''All Zones Cooling Setpoint (°C)'''
        self.allCS = np.asarray([[self.coreCS], [self.zn1CS], [self.zn2CS], [self.zn3CS], [self.zn4CS]])
        self.allCS_mean1 = np.mean(self.allCS, 1)
        self.allCS_mean2 = np.mean(self.allCS_mean1)
        self.allCS_max = np.max(self.allCS)
        self.allCS_min = np.min(self.allCS)

        '''Core Zone Heating Setpoint (°C)'''
        self.coreHS = np.asarray(newEntry['CORE_ZN:Zone Thermostat Heating Setpoint Temperature [C](Hourly)'],
                                        dtype=np.float32)
        self.coreHS_mean = np.mean(self.coreHS)
        self.coreHS_max = np.max(self.coreHS)
        self.coreHS_min = np.min(self.coreHS)

        '''Zone 1 Heating Setpoint (°C)'''
        self.zn1HS = np.asarray(newEntry['PERIMETER_ZN_1:Zone Thermostat Heating Setpoint Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn1HS_mean = np.mean(self.zn1HS)
        self.zn1HS_max = np.max(self.zn1HS)
        self.zn1HS_min = np.min(self.zn1HS)

        '''Zone 2 Heating Setpoint (°C)'''
        self.zn2HS = np.asarray(newEntry['PERIMETER_ZN_2:Zone Thermostat Heating Setpoint Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn2HS_mean = np.mean(self.zn2HS)
        self.zn2HS_max = np.max(self.zn2HS)
        self.zn2HS_min = np.min(self.zn2HS)

        '''Zone 3 Heating Setpoint (°C)'''
        self.zn3HS = np.asarray(newEntry['PERIMETER_ZN_3:Zone Thermostat Heating Setpoint Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn3HS_mean = np.mean(self.zn3HS)
        self.zn3HS_max = np.max(self.zn3HS)
        self.zn3HS_min = np.min(self.zn3HS)

        '''Zone 4 Heating Setpoint (°C)'''
        self.zn4HS = np.asarray(newEntry['PERIMETER_ZN_4:Zone Thermostat Heating Setpoint Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn4HS_mean = np.mean(self.zn4HS)
        self.zn4HS_max = np.max(self.zn4HS)
        self.zn4HS_min = np.min(self.zn4HS)

        '''All Zones Heating Setpoint (°C)'''
        self.allHS = np.asarray([[self.coreHS], [self.zn1HS], [self.zn2HS], [self.zn3HS], [self.zn4HS]])
        self.allHS_mean1 = np.mean(self.allHS, 1)
        self.allHS_mean2 = np.mean(self.allHS_mean1)
        self.allHS_max = np.max(self.allHS)
        self.allHS_min = np.min(self.allHS)

        '''Core Zone Thermostat Temperature (°C)'''
        self.coreT = np.asarray(newEntry['CORE_ZN:Zone Thermostat Air Temperature [C](Hourly)'],
                                        dtype=np.float32)
        self.coreT_mean = np.mean(self.coreT)
        self.coreT_max = np.max(self.coreT)
        self.coreT_min = np.min(self.coreT)

        '''Zone 1 Thermostat Temperature (°C)'''
        self.zn1T = np.asarray(newEntry['PERIMETER_ZN_1:Zone Thermostat Air Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn1T_mean = np.mean(self.zn1T)
        self.zn1T_max = np.max(self.zn1T)
        self.zn1T_min = np.min(self.zn1T)

        '''Zone 2 Thermostat Temperature (°C)'''
        self.zn2T = np.asarray(newEntry['PERIMETER_ZN_2:Zone Thermostat Air Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn2T_mean = np.mean(self.zn2T)
        self.zn2T_max = np.max(self.zn2T)
        self.zn2T_min = np.min(self.zn2T)

        '''Zone 3 Thermostat Temperature (°C)'''
        self.zn3T = np.asarray(newEntry['PERIMETER_ZN_3:Zone Thermostat Air Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn3T_mean = np.mean(self.zn3T)
        self.zn3T_max = np.max(self.zn3T)
        self.zn3T_min = np.min(self.zn3T)

        '''Zone 4 Thermostat Temperature (°C)'''
        self.zn4T = np.asarray(newEntry['PERIMETER_ZN_4:Zone Thermostat Air Temperature [C](Hourly)'],
                       dtype=np.float32)
        self.zn4T_mean = np.mean(self.zn4T)
        self.zn4T_max = np.max(self.zn4T)
        self.zn4T_min = np.min(self.zn4T)

        '''All Zones Thermostat Temperature (°C)'''
        self.allT = np.asarray([[self.coreT], [self.zn1T], [self.zn2T], [self.zn3T], [self.zn4T]])
        self.allT_mean1 = np.mean(self.allT, 1)
        self.allT_mean2 = np.mean(self.allT_mean1)
        self.allT_max = np.max(self.allT)
        self.allT_min = np.min(self.allT)

