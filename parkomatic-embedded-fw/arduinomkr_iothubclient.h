#include <Arduino.h>
#include <MKRGSM.h>
#include <ArduinoMqttClient.h>
#include <ArduinoBearSSL.h>
#include <ArduinoECCX08.h>
#include <utility/ECCX08SelfSignedCert.h>

#ifndef _ARDUINOMKR_IOTHUBCLIENT_H
#define _ARDUINOMKR_IOTHUBCLIENT_H

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


class IotHubClient
{
public:
    IotHubClient(MqttClient mqttClient, 
                 char* hostName,
                 char* deviceId,
                 int mqttPort = 8883);
   
    ~IotHubClient();
    int 

private:
    // methods
    unsigned long getTimeFromGsm();

private:
    // properties
    char* hostName;
    char* deviceId;

    GPRS gprsHandle;
    GSM gsmHandle;

    GSMClient gsmClient;
    BearSSLClient sslClient;
    MqttClient mqttClient;
};