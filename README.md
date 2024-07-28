# cbpi4-inkbird-plugin

This plugin connects to inkbird temperature control devices, specifically the ITC-308 WIFI model (This was the only device tested, others may work, but use at your own risk) to craftbeerpi4. Tuya's home automation API service is used to read and write values to the device. A devlopment account must be created on the Tuya development website and setup instructions must completed to utilize the API service and obtain the device ID. The device ID and/or IP can be used to read the device's temperatue value, setpoint, and heating/cooling status and write setup parameters to the device. 

# Setup API service
To setup the Tuya API service, complete the following for all inkbird devices to connect the CBPI:



## Hardware setup

# Sensor Setup in CBPI:
In the hardware setup tab, an "Inkbird Sensor" can setup with the following parameters:
Device ID - This is the inkbird device ID obtained from the Tuya home automattion developer websites
IP Address - This is the inkbird device IP address, this can also be obtained from the Tuya home automation developer website. THis can be helpful to identify the device, but is not a neccesary parameter
Refresh Rate - This is the time (in seconds) the data from the device will be refreshed in CBPI. default value is 60 (s)
Data - This is the sensor data requested from the device, it can be "Temperature" - Existing temperature reading (PV), "Setpoint" - Desired temperture control loop setpoint (SV), or "State" - "Heating or "Cooling" Control on device. Value of 1 = Heating, Value of 2 = Cooling


# Fermenter Setup in CBPI:
In the hardware setup tab, an "Inkbird Fermenter" can be setup under "FermenterLogic". The CBPI fermenter will set the setpoint on the inkbird device based on the user entered data or fermentation step automation.
The following parameters are required for setup:
Fermenter_Dev_ID - This is the inkbird device ID obtained from the Tuya home automattion developer websites
Fermenter_Dev_IP_address - This is the inkbird device IP address, this can also be obtained from the Tuya home automation developer website. This can be helpful to identify the device, but is not a neccesary parameter
Temp_Unit - Temperature Unit of the fermenter device, In celsius (C) or fahrenheit (F). This will change the setting on the inkbird device.
Temperature_Calibration - Temperature calibartion is used to correct the temperature reading. This will change the setting on the inkbird device.
Fridge_Delay - Delay is used before starting cooling. if temperature value is less than the setpoint minus cooling hystersis, then cooling will start after this amount of time (in minutes). This will change the setting on the inkbird device.
Hi_Temp - This value is the high temperature alarm. An audible buzzer in the device will sound if this is exceeded. 
Lo_Temp - This value is the low temperature alarm. An audible buzzer in the device will sound if the temperature is less than this alarm
Cool_Hys - This is the temperature difference below the setpoint the device will allow cooling before starting heating. This will change the setting on the inkbird device.
Heat_Hys - This is the temperature difference above the setpoint the device will allow heating before waiting for the refridgeration delay or entering cooling. This will change the setting on the inkbird device.
Change_SP - If this is Y - Yes, then the devices temperature setpoint can be changed externally via the app or locally at the controller. If this is N - No, then the devices temperature setpoint can only be changed on the craftebeerpi application.

# Fermenter with Chiller Setup in CBPI:
In the hardware setup tab, an "Inkbird Fermenter with Chiller" can be setup under "FermenterLogic". This is used when two seperate inkbirds are used to control the temperature of a fermenter and glycol chiller. The CBPI fermenter will set the setpoint on the inkbird fermetenter device based on the user entered data or fermentation step automation and also set the setpoint in the inkbird glycol chiller based on the "offset" parameter
The following parameters are required for setup:
Fermenter_Dev_ID - This is the inkbird device ID for the fermenter inkbird controller. This can obtained from the Tuya home automattion developer websites
Fermenter_Dev_IP_address - This is the fermenter inkbird device IP address, this can also be obtained from the Tuya home automation developer website. This can be helpful to identify the device, but is not a neccesary parameter
Fermenter Temp_Unit - Temperature Unit of the fermenter device, In celsius (C) or fahrenheit (F). This will change the setting on the inkbird device.
Fermenter Temperature_Calibration - Fermenter device temperature calibartion is used to correct the temperature reading. This will change the setting on the inkbird device.
Fermenter Fridge_Delay - Fermenter device delay is used before starting cooling. if temperature value is less than the setpoint minus cooling hystersis, then cooling will start after this amount of time (in minutes). This will change the setting on the inkbird device.
Fermenter Hi_Temp - This value is the high temperature alarm for the fermenter device. An audible buzzer in the device will sound if this is exceeded. 
Fermenter Lo_Temp - This value is the low temperature alarm for the fermenter device. An audible buzzer in the device will sound if the temperature is less than this alarm
Fermenter Cool_Hys - This is the fermenter temperature difference below the setpoint the device will allow cooling before starting heating. This will change the setting on the inkbird device.
Fermenter Heat_Hys - This is the fermenter temperature difference above the setpoint the device will allow heating before waiting for the refridgeration delay or entering cooling. This will change the setting on the inkbird device.
Chiller_Dev_ID - This is the inkbird device ID for the Chiller inkbird controller. This can obtained from the Tuya home automattion developer websites
Chiller_Dev_IP_address - This is the inkbird chiller device IP address, this can also be obtained from the Tuya home automation developer website. This can be helpful to identify the device, but is not a neccesary parameter
Chiller Temp_Unit - Temperature Unit of the chiller device, In celsius (C) or fahrenheit (F). This will change the setting on the inkbird device.
Chiller Temperature_Calibration - Chiller device temperature calibartion is used to correct the temperature reading. This will change the setting on the inkbird device.
Chiller Fridge_Delay - Chiller device delay is used before starting cooling. if temperature value is less than the setpoint minus cooling hystersis, then cooling will start after this amount of time (in minutes). This will change the setting on the inkbird device.
Chiller Hi_Temp - This value is the high temperature alarm for the chiller device. An audible buzzer in the device will sound if this is exceeded. 
Chiller Lo_Temp - This value is the low temperature alarm for the chiller device. An audible buzzer in the device will sound if the temperature is less than this alarm
Chiller Cool_Hys - This is the chiller temperature difference below the setpoint the device will allow cooling before starting heating. This will change the setting on the inkbird device.
Chiller Heat_Hys - This is the chiller temperature difference above the setpoint the device will allow heating before waiting for the refridgeration delay or entering cooling. This will change the setting on the inkbird device.
Chiller Offset - This is the temperature difference between the fermenter setpoint and chiller setpoint. The chiller will be set lower than the fermenter based on the value input. When the fermenter setpoint changes, so will the chiller setpoint
Change_SP - If this is Y - Yes, then the fermtner devices temperature setpoint can be changed externally via the app or locally at the controller. If this is N - No, then the devices temperature setpoint can only be changed on the craftebeerpi application.






