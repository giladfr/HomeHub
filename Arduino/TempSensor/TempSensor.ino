#include "DHT.h"


DHT dht;


#define DHT11_PIN    7
#define GET_TEMP_HUMID  't'


void setup()
{
  Serial.begin(9600);
  dht.setup(DHT11_PIN); // data pin 2
}

void loop()
{
  byte in_byte;
  if (Serial.available()) 
  {
      in_byte = Serial.read();
      switch (in_byte)
      {
        case GET_TEMP_HUMID:
          return_temp_humid();
          break;
        default:
          break;    
      }
  }
	
}

void return_temp_humid()
{
    float humidity = dht.getHumidity();
    float temperature = dht.getTemperature();

    Serial.print(dht.getStatusString());
    Serial.print(",");
    Serial.print(humidity, 1);
    Serial.print(",");
    Serial.println(temperature, 1);
}

