void setup() {
  // put your setup code here, to run once:
#include "LiquidCrystal.h"
#include "defines.h"
#include "ArduinoLowPower.h"

LiquidCrystal lcd(LCD_RS_PIN, LCD_ENABLE_PIN, LCD_D4_PIN, LCD_D5_PIN, LCD_D6_PIN, LCD_D7_PIN);

void setup() 
{
	lcd.setCursor(0,0);
	lcd.print("Parkering start:");
	lcd.begin(LCD_COLUMNS, LCD_ROWS);
}

void loop() {
  // put your main code here, to run repeatedly:

}
