#include <SdFat.h>

SdFat sd;
SdFile myFile;
const int chipSelect = 27;
int zaehler = 0;

void setup() {
  Serial.begin(9600);
}

void loop(){
  float temperatur;
  float druck;
  temperatur = get_temperatur_Messung();
  druck = get_druck_Messung();
  Serial.println(zaehler);
  zaehler ++;
  Serial.println(temperatur);
  Serial.println(druck);
  save_to_Sd(druck, temperatur, zaehler);
  Serial.println();
  delay(1000);
}

float get_temperatur_Messung() {
 float volt;
 float temperatur;
 volt=5.0/1023.0*analogRead(A1);
 temperatur = 100*volt;
 return temperatur;
}

float get_druck_Messung() {
 float volt;
 float druck;
 volt=5.0/1023.0*analogRead(A0);
 druck = 10*(volt/(0.009*5.0)+(0.095/0.009));
 return druck;
}

void save_to_Sd(float druck, float temperatur, int zaehlernummer){
  if (!sd.begin(chipSelect, SPI_HALF_SPEED)) {
    Serial.println("Fehler beim Speichern. ERROR 1");
   }
  else if (!myFile.open("log.txt", O_RDWR | O_CREAT | O_AT_END))  {
    Serial.println("Fehler beim erstellen der Protokolldatei. ERROR 2");
   }
  else {
    Serial.print("Writing to log.txt...");
    myFile.println(zaehlernummer);
    myFile.println(druck);
    myFile.println(temperatur);
    myFile.println();
    myFile.close();
    Serial.println("done.");
   }
}
