// include the library code:
#include <LiquidCrystal.h>

// General defines
#define PIN_BACKLIGHT 		10
#define CLK_LINE      		0  
#define LCD_NUM_LINES 		2
#define LCD_LINE_LENGTH		16


// general CMD op code
#define CMD_OP 				0xFF

// Low level op codes
#define CMD_CLEAR 			0x0A
#define CMD_BACKLIGHT_OFF  	0x0B
#define CMD_BACKLIGHT_ON  	0x0C
#define CMD_SET_CURSOR  	0x0D
#define CMD_BACKLIGHT_BLINK         0x0E

// High level op codes
#define CMD_CLOCK_START		0x20
#define CMD_CLOCK_END		0x21

#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   5
int lcd_key     = 0;
int adc_key_in  = 0;

int read_LCD_buttons()
{
 adc_key_in = analogRead(0);   
 if (adc_key_in > 1000) return btnNONE; 
 if (adc_key_in < 50)   return btnRIGHT;  
 if (adc_key_in < 195)  return btnUP; 
 if (adc_key_in < 380)  return btnDOWN; 
 if (adc_key_in < 555)  return btnLEFT; 
 if (adc_key_in < 790)  return btnSELECT;    
 
 return btnNONE; 
}


  


// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
void setup()
{
	// set up the LCD's number of columns and rows: 
	lcd.begin(LCD_LINE_LENGTH, LCD_NUM_LINES);
	// initialize the serial communications:
	Serial.begin(9600);
	pinMode(PIN_BACKLIGHT,  OUTPUT);
	digitalWrite(PIN_BACKLIGHT, HIGH);
	// Write welcome messege
	lcd.print("Waiting...");
}






void loop()
{
	int in_byte;
	int cmd;
	int col;
	int row;
	
	// when characters arrive over the serial port...
	if (Serial.available()) 
	{
		// wait a bit for the entire message to arrive
		delay(100);
		// read all the available characters
		while (Serial.available() > 0) 
		{
			// display each character to the LCD
			in_byte = Serial.read();
			if (in_byte == CMD_OP) // Op Code
			{
				cmd = Serial.read();
				switch (cmd)
				{
				// ------ OP Codes
				case CMD_CLEAR:
					lcd.clear();
					break;
				case CMD_BACKLIGHT_OFF:
					digitalWrite(PIN_BACKLIGHT, LOW);
					break;
				case CMD_BACKLIGHT_ON:
					digitalWrite(PIN_BACKLIGHT, HIGH);
					break;
				case CMD_SET_CURSOR:
					col = Serial.read();
					row = Serial.read();
					lcd.setCursor(col,row);
					break;
                                case CMD_BACKLIGHT_BLINK:
                                        int d = Serial.read();;
                                        BackLightBlink(d * 1000);
                                        break;
					
				}        
				
			}
			else // Regular Char, just print
			{
				lcd.write(in_byte);
			}
		}
	}
}

void BackLightBlink(int dismissTimeOutMs)
{
  int Tic = millis();
  int Toc;
  
  while (true)
  {
    Toc = millis();
    if ((Toc - Tic) > dismissTimeOutMs) break;
    if (read_LCD_buttons() != btnNONE) break;    
    digitalWrite(PIN_BACKLIGHT, LOW);
    if (read_LCD_buttons() != btnNONE) break;
    delay(500);
    if (read_LCD_buttons() != btnNONE) break;
    digitalWrite(PIN_BACKLIGHT, HIGH);
    if (read_LCD_buttons() != btnNONE) break;
    delay(500);
    if (read_LCD_buttons() != btnNONE) break;
    
  }
  
  digitalWrite(PIN_BACKLIGHT, HIGH);
  lcd.clear();
  Serial.write("Dismissed\n");
  
}
  
  
  
  

