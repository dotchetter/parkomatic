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
#define SECRET_BROKER                ""
#define SECRET_DEVICE_ID             ""
#define MQTT_PORT				     8883

/* Intervals and time definitions */

#define SECOND                       1000UL
#define MINUTE                       60 * SECOND
#define INTERVAL                     1 * SECOND

#define DEVMODE                      1

#endif // _DEFINES_H_#define POLL_TIME_LIMIT				 5 * MINUTE
