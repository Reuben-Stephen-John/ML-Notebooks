#include <Servo.h>
Servo myservo;
Servo myservo1;
String my_data;
String my_intensity;
#define LED_PIN 11
int brightness;

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}
void setup() {
  Serial.begin(115200);
  myservo.attach(9);
  myservo1.attach(10);
}

void loop() {
  while (Serial.available()==0){
    
  }
  my_data = Serial.readStringUntil('\r');
  String xval = getValue(my_data, ',', 0);
  String yval = getValue(my_data, ',', 2);
  int xvalue = xval.toInt();
  int yvalue = yval.toInt();
  brightness = my_data.toInt();
  int num = map(xvalue, 0, 255, 20, 90);
  int num1 = map(yvalue, 0, 500, 30, 90);
  myservo.write(num);
  myservo1.write(num1);
}
