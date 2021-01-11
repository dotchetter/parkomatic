#include "arduinomkr_iothubclient.h"

/*
    Arduino MKR1400 Azure IOT Hub library 
    
    Developed by Simon Olofsson 2021-01-11
    https://github.com/dotchetter

    This library is designed to work with the Arduino MKR
    series boards, on NB, Wifi or GSM.

    This library is intended for free use, even for commercial
    purposed but WITHOUT ANY WARRANTY; without even the 
    implied warranty of MERCHANTABILITY or FITNESS FOR A 
    PARTICULAR PURPOSE. 
    
    License: MIT
*/


IotHubClient::IotHubClient::(MqttClient mqttClient, 
                             const char* hostName,
                             const char* deviceId,
                             int mqttPort = 8883)
/*
    Main constructor
    Set up MQTT client with properties
*/
{
    ECCX08SelfSignedCert.beginReconstruction(0, 8);
    ECCX08SelfSignedCert.setCommonName(ECCX08.serialNumber());
    ECCX08SelfSignedCert.endReconstruction();


}


IotHubClient::connect()
{

}


unsigned long IotHubClient::getTimeFromGsm()
{

}

