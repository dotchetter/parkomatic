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


/* Global handles used for communícations */
GPRS gprsHandle;
GSM gsmHandle;

GSMClient gsmClient;
BearSSLClient sslClient(gsmClient);
MqttClient mqttClient(sslClient);


/* Helper functions */
uint32_t GetTimeFromGsm()
{
    return gsmHandle.getTime();
}


/* == Public instance methods == */

IotHubClient::IotHubClient(char* hostName,
                           char* deviceId,
                           int mqttPort)
{
    this->hostName = hostName;
    this->deviceId = deviceId;
    this->mqttPort = mqttPort;
}


IotHubClient::~IotHubClient()
{
    gsmClient.stop();
}


void IotHubClient::Begin()
{
    char mqtt_username[128];

    /* Restore and configure SSL certificate and time method callback*/
    ECCX08SelfSignedCert.beginReconstruction(0, 8);
    ECCX08SelfSignedCert.setCommonName(ECCX08.serialNumber());
    ECCX08SelfSignedCert.endReconstruction();
    ArduinoBearSSL.onGetTime(GetTimeFromGsm);

    /* Set the public key to be used with the certificate 
       in the ECCX08 slot */
    sslClient.setEccSlot(NULL,
                         ECCX08SelfSignedCert.bytes(),
                         ECCX08SelfSignedCert.length());

    /* Format string for MQTT username */
    sprintf(mqtt_username, 
            "%s/%s/api-version=2018-06-30", 
            this->hostName, 
            this->deviceId);

    mqttClient.setId(this->deviceId);
    mqttClient.setUsernamePassword(mqtt_username, NONE);

    /* Establish connection with cellular services over GPRS or GSM */
    this->ConnectToCellularNetwork();

    /* Establish connection to the MQTT broker*/
    this->ConnectToMqttBroker();
}


int IotHubClient::Available()
{
    return mqttClient.available();
}


void IotHubClient::Update()
{
    mqttClient.poll();
}


const char IotHubClient::ReadIncoming()
{
    return mqttClient.read();
}


void IotHubClient::Publish(char* message)
{
    char mqtt_topic[1024];

    if (gsmHandle.status() != GSM_READY || gprsHandle.status() != GPRS_READY)
    {
        this->ConnectToCellularNetwork();
    }

    if (!mqttClient.connected())
    {
        this->ConnectToMqttBroker();
    }

    sprintf(mqtt_topic,
            "devices/%s/messages/events/",
            this->deviceId);

    mqttClient.beginMessage(mqtt_topic);
    mqttClient.print(message);
    mqttClient.endMessage();

    Serial.print(F("[DEBUG]: Message successfully published to "));
    Serial.println(this->hostName);
}

/* == Private methods == */

void IotHubClient::ConnectToCellularNetwork()
{
    uint32_t connect_start_ms = millis();
    uint32_t previous_connect_ms;

    while(1)
    {
        if (millis() - connect_start_ms > GSM_RECONNECT_TIMEOUT)
        {
            Serial.println("[DEBUG]: GSM reached timeout for reconnects, aborting");
            break;
        }

        if (millis() - previous_connect_ms > GSM_RECONNECT_INTERVAL)
        {
            Serial.print("[DEBUG]: Attempting to connect to cellular services... ");
            previous_connect_ms = millis();

            if ((gsmHandle.begin(SECRET_PINNUMBER) != GSM_READY) ||
                (gprsHandle.attachGPRS(SECRET_GPRS_APN, 
                                       SECRET_GPRS_LOGIN,
                                       SECRET_GPRS_PASSWORD) != GPRS_READY))
            {
                Serial.println("[ERROR]: connection failed. -> Trying again... ");
            }
            else
            {
                Serial.println("success");
                break;
            }
        }
    }
}


void IotHubClient::ConnectToMqttBroker()
{
    char mqtt_topic[128];
    uint32_t connect_start_ms = millis();
    uint32_t previous_connect_ms;

    /* Format string for MQTT topic subscription for incoming messages */
    sprintf(mqtt_topic,
            "devices/%s/messages/devicebound/#",
            this->deviceId);

    while (1)
    {
        if (millis() - connect_start_ms > MQTT_RECONNECT_TIMEOUT)
        {
            Serial.println("[DEBUG]: MQTT reached timeout for reconnects, aborting");
            break;
        }
        
        if (millis() - previous_connect_ms > MQTT_RECONNECT_INTERVAL)
        {
            Serial.println("[DEBUG]: Attempting to connect to the MQTT broker... ");
            
            previous_connect_ms = millis();
            
            if (!mqttClient.connect(this->hostName, this->mqttPort))
            {
                Serial.print("[ERROR]: MQTT ran in to a problem. Error code: ");
                Serial.println(mqttClient.connectError());
            }
            else
            {
                Serial.println("[DEBUG]: Connection to MQTT broker successful.");
                mqttClient.subscribe(mqtt_topic);
                break;
            }
        }
    }
} 


void IotHubClient::SetIncomingMessageCallback(void(*callback)(int))
{
    mqttClient.onMessage(callback);
}