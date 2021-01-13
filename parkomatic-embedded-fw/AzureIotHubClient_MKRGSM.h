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

#ifndef SECOND
#define SECOND                       1000UL
#endif

#ifndef MINUTE
#define MINUTE                       60 * SECOND
#endif
    
/* Timeouts and intervals */

#define NONE ""
#define GSM_RECONNECT_TIMEOUT        1 * MINUTE
#define GSM_RECONNECT_INTERVAL       5 * SECOND
#define MQTT_RECONNECT_INTERVAL      5 * SECOND
#define MQTT_RECONNECT_TIMEOUT       1 * MINUTE
#define GSM_RECONNECT_INTERVAL       5 * SECOND


class IotHubClient
{
public:
    IotHubClient(char* hostName,
                 char* deviceId,
                 int mqttPort=8883);
    ~IotHubClient();
    void Begin();
    int Available();
    void Update();
    const char ReadIncoming();
    void Publish(char* message);
    void SetIncomingMessageCallback(void(*callback)(int));

private: // Methods
    void ConnectToCellularNetwork();
    void ConnectToMqttBroker();

private: // Fields
    char* hostName;
    char* deviceId;
    int mqttPort;
    char incomingMessageAvailable;
    uint32_t(*callback_f_ptr)(void);
};

/* Helper function in global scope */
uint32_t GetTimeFromGsm();

#endif // _ARDUINOMKR_IOTHUBCLIENT_H