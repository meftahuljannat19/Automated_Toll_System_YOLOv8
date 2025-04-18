#include<cvzone.h>
#include <LiquidCrystal_I2C.h>
#include<Servo.h>
Servo myservo;
LiquidCrystal_I2C lcd(0x27, 16, 2);
SerialData serialData(1, 1);
#define reset_pin 7
int valsRec[1];
int pos = 150;
void setup() {
  serialData.begin(9600);
  lcd.init();
  lcd.clear();
  lcd.backlight();
  myservo.attach(9);
  myservo.write(pos);
  digitalWrite(reset_pin, HIGH);
  pinMode(reset_pin, OUTPUT);
  pinMode(10, OUTPUT);
  
}

void loop() {
  serialData.Get(valsRec);
  if (valsRec[0] == 1) {
    digitalWrite(10, HIGH);
    lcd.clear();
    lcd.setCursor(2, 0);
    lcd.print("Number Plate");
    lcd.setCursor(2, 1);
    lcd.print("Matched");
    delay(2000);
    lcd.clear();
    lcd.setCursor(1, 0);
    lcd.print("Fair Deducted");
    delay(2000);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Gate Opening...");
    for (pos = 150; pos >=60; pos -= 1) {
      myservo.write(pos);
      delay(15);
    }
    delay(2000);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Gate Closing...");
    for (pos = 60; pos <= 150; pos += 1) {
      myservo.write(pos);
      delay(15);
    }
    delay(1000);
    digitalWrite(reset_pin, LOW);
  }
  else {
    digitalWrite(10, LOW);
    lcd.clear();
    lcd.setCursor(2, 0);
    lcd.print("Automatic");
    lcd.setCursor(2, 1);
    lcd.print("Toll Booth");
    delay(1000);
    digitalWrite(reset_pin, HIGH);
  }
}
