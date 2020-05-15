/*  Final Project
 *   Kenny Wang & Lukas Griffin
 *   We affirm that we've adhered to the honor code on this assignment.
 *   So far it takes in soil moisture and temperature reading.
*/

#include <LiquidCrystal.h>
#include <dht11.h>
#define DHT11PIN A2

dht11 DHT11;
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

const int AirValue = 580;  // when 0% moisture
const int WaterValue = 310; // when 100% moisture
const int tempPin = A1;
int soilMoistureValue = 0;
int soilMoisturePercent = 0;


void setup() {
  Serial.begin(9600); // open serial port, set the baud rate to 9600 bps
  lcd.begin(16, 2);
}
void loop() {
  int chk = DHT11.read(DHT11PIN);
  int tempMV = analogRead(tempPin);  
  float voltage = tempMV * 5.0; // voltage adjustments for 5v
  voltage /= 1024.0; 
  float tempC = (voltage - 0.5) * 100 ;  // celcius conversion
  
  soilMoistureValue = analogRead(A0);  //put Sensor insert into soil
  //Serial.println(soilMoistureValue);
  soilMoisturePercent = map(soilMoistureValue, AirValue, WaterValue, 0, 100);
  
  // first two cases to adjust to the current environment.
  if(soilMoisturePercent > 100)  // when 100% moisutre
  {
    Serial.println("100 %");
    lcd.setCursor(0, 0);
    lcd.print("Soil Moisture");
    lcd.setCursor(0, 1);
    lcd.print("100 %");
    delay(250);
    lcd.clear();
  }
  else if(soilMoisturePercent < 0)  // means no moisture
  {
    Serial.println("0 %");
    lcd.setCursor(0, 0);
    lcd.print("Soil Moisture");
    lcd.setCursor(0, 1);
    lcd.print("0 %");
    delay(250);
    lcd.clear();
    }
  else if(soilMoisturePercent >0 && soilMoisturePercent < 100)
  {
    //Serial.print(soilMoisturePercent);
    //Serial.println("%");

    float humidity = (float)DHT11.humidity;
    float temperature = (float)DHT11.temperature;
    
    lcd.setCursor(0, 0);
    lcd.print("Soil Moisture");
    lcd.setCursor(0, 1);
    lcd.print(soilMoisturePercent);
    lcd.print("%");
    delay(1000);
    lcd.clear();

    lcd.setCursor(0,0);
    lcd.print("Temperature");
    lcd.setCursor(0,1);
    lcd.print(tempC);
    lcd.print("C");
    
    delay(1000);
    lcd.clear();

    lcd.setCursor(0,0);
    lcd.print("Humidity");
    lcd.setCursor(0,1);
    lcd.print(humidity);
    lcd.print("%");
    Serial.println(String(soilMoisturePercent) + "z" + String(temperature) + "z" + String(humidity));

    delay(1000);
    lcd.clear();
  }  
}
