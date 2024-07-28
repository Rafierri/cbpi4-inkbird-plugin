
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
from cbpi.api import *
import tinytuya

logger = logging.getLogger(__name__)

@parameters([Property.Text(label="dev_id", description="Device ID from the Tuya Developer Website"),
    Property.Text(label='IP_address',description ='IP Address for the device used. Default is None',default_value='None'),
    Property.Number(label="refresh_rate",configurable = True, default_value = 60, description = "Refresh rate for when device will be downloaded from inkbird (sec). Default value is 60"),
    Property.Select(label="Data", options=["Temperature", "Setpiont", "State"], description="Type of data to pull from the inkbird device")])

class InkbirdSensor(CBPiSensor):
    
    def __init__(self, cbpi, id, props):
        super(InkbirdSensor, self).__init__(cbpi, id, props)
        self.value = 0 
        self.device = tinytuya.OutletDevice(dev_id = self.props.get("dev_id"), address = self.props.get('IP_address'))

    async def run(self):
        
        while self.running is True:

            if self.props.get('Data') == "Temperature":

                self.value = float(self.device.status()['dps']['116']/10)

            elif self.props.get('Data') == "Setpiont":

                self.value = float(self.device.status()['dps']['106']/10)
            
            elif self.props.get('Data') == "State":

                if self.device.status()['dps']['115'] =='3':
                    self.value = 1
                    #Device is calling for heat
                elif self.device.status()['dps']['115'] =='1':
                    self.value = 2
                    #Device is calling for cooling
            
            self.push_update(self.value)
            await asyncio.sleep(int(self.props.get('refresh_rate')))
    

@parameters([Property.Text(label="Fermenter_Dev_ID", configurable=True,
                             description="Inkbird Device ID for Fermenter temperature controller"),
            Property.Text(label='Ferment_Dev_IP_address',configurable=True, description ='Fermenter inkbird device IP Address for the device used. Default is None',default_value='None'),
            Property.Select(label='Fermenter Temp_Unit',options=["C","F"], description='Fermenter Temperature Units (C/F)'),
            Property.Number(label="Fermenter Temperature_Calibration", description='Fermenter Temperature Correction for device',default_value=0),
            Property.Number(label="Fermenter Fridge_Delay", description = "Fermenter Refridgeration delay, Time controller will delay once cooling condition is met",default_value = 0),
            Property.Number(label="Fermenter Hi_Temp", description = "Fermenter High Temperature alarm, buzzer will sound above this temperature.", default_value = 212),
            Property.Number(label="Fermenter Lo_Temp", description = "Fermenter Lo Temperature alarm, buzzer will sound below this temperature.", default_value = -40),
            Property.Number(label="Fermenter Cool_Hys", description='Fermenter Cooling Hystersis Temperature',default_value=0.5),
            Property.Number(label="Fermenter Heat_Hys", description='Fermenter Heating Hystersis Temperature',default_value=0.5),
            Property.Text(label="Chiller_Dev_ID", configurable=True,
                             description="Inkbird Device ID for Glycol Chiller temperature controller"),
            Property.Text(label='Chiller_Dev_IP_address',configurable=True, description ='Chiller inkbird device IP Address for the device used. Default is None',default_value='None'),
            Property.Select(label='Chiller Temp_Unit',options=["C","F"], description='Chiller Temperature Units (C/F)'),
            Property.Number(label="Chiller Temperature_Calibration", description='Chiller Temperature Correction for device',default_value=0),
            Property.Number(label="Chiller Fridge_Delay", description = "Chiller Refridgeration delay, Time controller will delay once cooling condition is met",default_value = 10),
            Property.Number(label="Chiller Hi_Temp", description = "Chiller High Temperature alarm, buzzer will sound above this temperature.", default_value = 212),
            Property.Number(label="Chiller Lo_Temp", description = "Chiller Lo Temperature alarm, buzzer will sound below this temperature.", default_value = 10),
            Property.Number(label="Chiller Cool_Hys", description='Chiller Cooling Hystersis Temperature',default_value=10),
            Property.Number(label="Chiller Heat_Hys", description='Chiller Heating Hystersis Temperature',default_value=5),
            Property.Number(label='Chiller Offset',description='Chiller SP offset from fermenter SP',default_value=10),
            Property.Select(label="Change_SP", options=['Y','N'],description='Allow the setpiont to be changed externally using another app or change the device while running')])


class InkbirdFermenterWithChiller(CBPiFermenterLogic):

    def __init__(self, cbpi, id, props):
        super(InkbirdFermenterWithChiller, self).__init__(cbpi, id, props)
        self.FermenterDevice = tinytuya.OutletDevice(dev_id = self.props.get("Fermenter_Dev_ID"), address = self.props.get('Ferment_Dev_IP_address'))
        self.ChillerDevice = tinytuya.OutletDevice(dev_id = self.props.get("Chiller_Dev_ID"), address = self.props.get('Chiller_Dev_IP_address'))
        
        if self.props.get('Change_SP') == "Y":
            self.allowSPchange = True
        else:
            self.allowSPchange = False
        


    async def run(self):
        
        try:
            self.fermenter = self.get_fermenter(self.id)
            self.FermenterDevice.set_value('102',int(self.props.get("Fermenter Temperature_Calibration", 0))*10)
            self.FermenterDevice.set_value('108',int(self.props.get('Fermenter Fridge_Delay',0)))
            self.FermenterDevice.set_value('109',int(self.props.get("Fermenter Hi_Temp",0))*10)
            self.FermenterDevice.set_value('110',int(self.props.get("Fermenter Lo_Temp",0))*10)
            self.FermenterDevice.set_value('118',int(self.props.get("Fermenter Cool_Hys",0))*10)
            self.FermenterDevice.set_value('117',int(self.props.get("Fermenter Heat_Hys",0))*10)
            self.FermenterDevice.set_value('101',str(self.props.get('Fermenter Temp_Unit',0)))

            self.ChillerDevice.set_value('102',int(self.props.get("Chiller Temperature_Calibration", 0))*10)
            self.ChillerDevice.set_value('108',int(self.props.get('Chiller Fridge_Delay',0)))
            self.ChillerDevice.set_value('109',int(self.props.get("Chiller Hi_Temp",0))*10)
            self.ChillerDevice.set_value('110',int(self.props.get("Chiller Lo_Temp",0))*10)
            self.ChillerDevice.set_value('118',int(self.props.get("Chiller Cool_Hys",0))*10)
            self.ChillerDevice.set_value('117',int(self.props.get("Chiller Heat_Hys",0))*10)
            self.ChillerDevice.set_value('101',str(self.props.get('Chiller Temp_Unit',0)))
            
            while self.running == True:

                if self.allowSPchange == False:
                    
                    target_temp = int(self.get_fermenter_target_temp(self.id))
                    offset = int(self.props.get('Chiller Offset'))
                    
                    if target_temp != self.FermenterDevice.status()['dps']['106']/10:
                        self.FermenterDevice.set_value('106',target_temp*10)
                        self.ChillerDevice.set_value('106',target_temp*10 - offset)
                    await asyncio.sleep(1)

                elif self.allowSPchange == True:
        
                    target_temp = self.get_fermenter_target_temp(self.id)
                    offset = int(self.props.get('Chiller Offset'))

                    self.FermenterDevice.set_value('106',target_temp*10)
                    self.ChillerDevice.set_value('106',target_temp*10 - offset)

                    while self.get_fermenter_target_temp(self.id) == int(self.FermenterDevice.status()['dps']['106']/10) :
                        await asyncio.sleep(5)

                    while self.get_fermenter_target_temp(self.id) != target_temp:                                
                        target_temp = self.get_fermenter_target_temp(self.id)
                        self.FermenterDevice.set_value('106',target_temp*10)
                        self.ChillerDevice.set_value('106',target_temp*10 - offset)

                    await self.set_fermenter_target_temp(self.id,int(self.FermenterDevice.status()['dps']['106']/10))
                    self.ChillerDevice.set_value('106',self.get_fermenter_target_temp(self.id) - offset)

                    
        except asyncio.CancelledError as e:
            pass
        except Exception as e:
            logging.error("Inkbird Fermenter Error {}".format(e))
        finally:
            self.running = False

@parameters([Property.Text(label="Fermenter_Dev_ID", configurable=True,
                             description="Inkbird Device ID for Fermenter temperature controller"),
            Property.Text(label='Fermenter_Dev_IP_address',configurable=True, description ='Fermenter inkbird device IP Address for the device used. Default is None',default_value='None'),
            Property.Select(label='Temp_Unit',options=["C","F"], description='Temperature Units (C/F)'),
            Property.Number(label="Temperature_Calibration", description='Temperature Correction for device',default_value=0),
            Property.Number(label="Fridge_Delay", description = "Refridgeration delay, Time controller will delay once cooling condition is met",default_value = 0),
            Property.Number(label="Hi_Temp", description = "High Temperature alarm, buzzer will sound above this temperature.", default_value = 212),
            Property.Number(label="Lo_Temp", description = "Lo Temperature alarm, buzzer will sound below this temperature.", default_value = -40),
            Property.Number(label="Cool_Hys", description='Cooling Hystersis Temperature',default_value=3),
            Property.Number(label="Heat_Hys", description='Heating Hystersis Temperature',default_value=3),
            Property.Select(label="Change_SP", options=['Y','N'],description='Allow the setpiont to be changed externally using another app or change the device while running')])

class InkbirdFermenter(CBPiFermenterLogic):

    def __init__(self, cbpi, id, props):
        super(InkbirdFermenter, self).__init__(cbpi, id, props)
        self.FermenterDevice = tinytuya.OutletDevice(dev_id = self.props.get("Fermenter_Dev_ID"), address = self.props.get('Ferment_Dev_IP_address'))
        if self.props.get('Change_SP') == "Y":
            self.allowSPchange = True
        else:
            self.allowSPchange = False
        

    async def run(self):
                
        try:
            self.fermenter = self.get_fermenter(self.id)
            self.FermenterDevice.set_value('102',int(self.props.get("Temperature_Calibration", 0))*10)
            self.FermenterDevice.set_value('108',int(self.props.get('Fridge_Delay',0)))
            self.FermenterDevice.set_value('109',int(self.props.get("Hi_Temp",0))*10)
            self.FermenterDevice.set_value('110',int(self.props.get("Lo_Temp",0))*10)
            self.FermenterDevice.set_value('118',int(self.props.get("Cool_Hys",0))*10)
            self.FermenterDevice.set_value('117',int(self.props.get("Heat_Hys",0))*10)
            self.FermenterDevice.set_value('101',str(self.props.get('Temp_Unit',0)))
            
            while self.running == True:

                if self.allowSPchange == False:
                    
                    target_temp = int(self.get_fermenter_target_temp(self.id))
                
                    if target_temp != self.FermenterDevice.status()['dps']['106']/10:
                        self.FermenterDevice.set_value('106',target_temp*10)
                    await asyncio.sleep(1)

                elif self.allowSPchange == True:
        
                        target_temp = self.get_fermenter_target_temp(self.id)
                        self.FermenterDevice.set_value('106',target_temp*10)
                        
                        while self.get_fermenter_target_temp(self.id) == int(self.FermenterDevice.status()['dps']['106']/10) :
                            await asyncio.sleep(5)
  
                        while self.get_fermenter_target_temp(self.id) != target_temp:
                                target_temp = self.get_fermenter_target_temp(self.id)
                                self.FermenterDevice.set_value('106',target_temp*10)

                        await self.set_fermenter_target_temp(self.id,int(self.FermenterDevice.status()['dps']['106']/10))

                    
        except asyncio.CancelledError as e:
            pass
        except Exception as e:
            logging.error("Inkbird Fermenter Error {}".format(e))
        finally:
            self.running = False


def setup(cbpi):
    cbpi.plugin.register("Inkbird Sensor", InkbirdSensor)
    cbpi.plugin.register("Inkbird Fermenter with Chiller", InkbirdFermenterWithChiller)
    cbpi.plugin.register('Inkbird Fermenter', InkbirdFermenter)
    pass
