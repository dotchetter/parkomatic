#ifndef _DEFINES_H_
#define _DEFINES_H_

/*
    2021-01-06 Simon Olofsson, Anton Norell
    Parkomatic* firmware defines file
*/


/* Configurations */
#define SECRET_PINNUMBER             ""
#define SECRET_GPRS_APN              ""  
#define SECRET_GPRS_LOGIN            ""    
#define SECRET_GPRS_PASSWORD         ""   
#define MQTT_PORT				     8883

/* Intervals and time definitions */
#define SECOND                       1000UL
#define MINUTE                       60 * SECOND
#define PUBLISH_INTERVAL             10 * SECOND

/* 
Devmode alters the device behavior in the following aspects:
 - Runtime is blocking until UART is initiated on the terminal side
 - Serial debug messages are ON 
*/

#define DEVMODE true
#define RUNONCE false
#define SENDONCE true

#endif // _DEFINES_H_