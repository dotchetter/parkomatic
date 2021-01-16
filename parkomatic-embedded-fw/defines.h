#ifndef _DEFINES_H_
#define _DEFINES_H_

/*
    2021-01-06 Simon Olofsson, Anton Norell
    Parkomatic* firmware defines file
*/


/* Configurations */

#define LCD_RS_PIN             		 12
#define LCD_ENABLE_PIN               11  
#define LCD_D4_PIN            		 5    
#define LCD_D5_PIN 			         4   
#define LCD_D6_PIN                   3
#define LCD_D7_PIN             		 2

#define LCD_COLUMNS                  16
#define LCD_ROWS                     2

#define JSON_BUFSIZE                 1024
#define MQTT_PORT				     8883

/* Intervals and time definitions */

#define SECRET_BROKER                ""
#define SECRET_DEVICE_ID             ""

#define SECOND                       1000UL
#define MINUTE                       60 * SECOND
#define PUBLISH_INTERVAL             30 * SECOND
#define GPS_SEEK_CYCLES              F_CPU / 1000000

/* Development flags */

#define DEVMODE true
#define SENDONCE true

/* Macros */

#define TIME_PASSED(ref, ts) (millis() - ts > ref)

#endif // _DEFINES_H_