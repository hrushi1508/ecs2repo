#include <LiquidCrystal.h>

// Motor driver pins
int m1 = 3;
int m2 = 4;
int m3 = 5;
int m4 = 6;
#define hitsensor 2
// LCD pins
const int rs = 8, en = 9, d4 = 10, d5 = 11, d6 = 12, d7 = 13;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  // Initialize LCD
  pinMode(hitsensor, INPUT_PULLUP);
  lcd.begin(16, 2);
  lcd.setCursor(2, 0);
  lcd.print("WELCOME");
  lcd.setCursor(0, 1);
  lcd.print("Speed Control Sys");
  delay(2000);
  lcd.clear();

  // Setup pins
  pinMode(m1, OUTPUT);
  pinMode(m2, OUTPUT);
  pinMode(m3, OUTPUT);
  pinMode(m4, OUTPUT);

  // Start Serial Communication
  Serial.begin(9600);
  lcd.setCursor(0, 0);
  lcd.print("Waiting Speed...");
}

void loop() {

  if (digitalRead(hitsensor) == 0) {
    delay(100);
    if (digitalRead(hitsensor) == 0) {
      lcd.setCursor(0, 0);
      lcd.print("Accident Detected");
      lcd.setCursor(0, 1);
      lcd.print("Help Needed to me");
      analogWrite(m1, 0);
      digitalWrite(m2, 0);
      analogWrite(m3, 0);
      digitalWrite(m4, 0);
      delay(250);
      
    }
  } else {

    if (Serial.available()) {
      String data = Serial.readStringUntil('\n');
      data.trim();

      int speedVal = data.toInt();
      lcd.clear();

      if (speedVal == 20) {
        analogWrite(m1, 90);
        digitalWrite(m2, 0);
        analogWrite(m3, 90);
        digitalWrite(m4, 0);
        lcd.setCursor(0, 0);
        lcd.print("Speed: 20 km/h");
        lcd.setCursor(0, 1);
        lcd.print("Low Speed Zone");
      }

      else if (speedVal == 30) {
        analogWrite(m1, 130);
        digitalWrite(m2, 0);
        analogWrite(m3, 130);
        digitalWrite(m4, 0);
        lcd.setCursor(0, 0);
        lcd.print("Speed: 30 km/h");
        lcd.setCursor(0, 1);
        lcd.print("Maintain Speed");
      }

      else if (speedVal == 60) {
        analogWrite(m1, 175);
        digitalWrite(m2, 0);
        analogWrite(m3, 175);
        digitalWrite(m4, 0);
        lcd.setCursor(0, 0);
        lcd.print("Speed: 60 km/h");
        lcd.setCursor(0, 1);
        lcd.print("Safe Speed");
      }

      else if (speedVal == 80) {
        analogWrite(m1, 205);
        digitalWrite(m2, 0);
        analogWrite(m3, 205);
        digitalWrite(m4, 0);
        lcd.setCursor(0, 0);
        lcd.print("Speed: 80 km/h");
        lcd.setCursor(0, 1);
        lcd.print("Good Condition");
      }

      else if (speedVal == 100) {
        analogWrite(m1, 255);
        digitalWrite(m2, 0);
        analogWrite(m3, 255);
        digitalWrite(m4, 0);
        lcd.setCursor(0, 0);
        lcd.print("Speed: 100 km/h");
        lcd.setCursor(0, 1);
        lcd.print("Highway Mode");
      }

      else {
        // Stop motors if data invalid
        digitalWrite(m1, 0);
        digitalWrite(m2, 0);
        digitalWrite(m3, 0);
        digitalWrite(m4, 0);
        lcd.setCursor(0, 0);
        lcd.print("No valid data");
      }

      Serial.print("Speed Updated to: ");
      Serial.println(speedVal);
    }
  }
}