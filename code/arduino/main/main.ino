const byte ROWS = 4;
const byte COLS = 4;

byte rowPins[ROWS] = {2, 3, 4, 5};
byte colPins[COLS] = {6, 7, 8, 9};

#define LONG_PRESS_TIME 500  // ms

struct ButtonState {
  bool pressed = false;
  unsigned long startTime = 0;
};

ButtonState buttonStates[ROWS][COLS];

void setup() {
  Serial.begin(9600);

  // set rows as outputs
  for (int r = 0; r < ROWS; r++) pinMode(rowPins[r], OUTPUT);
  // set columns as inputs with pullups
  for (int c = 0; c < COLS; c++) pinMode(colPins[c], INPUT_PULLUP);

  // deactivate all rows
  for (int r = 0; r < ROWS; r++) digitalWrite(rowPins[r], HIGH);
}

void loop() {
  for (int r = 0; r < ROWS; r++) {
    // activate row
    digitalWrite(rowPins[r], LOW);

    for (int c = 0; c < COLS; c++) {
      bool isPressed = digitalRead(colPins[c]) == LOW;
      int btnNumber = c * ROWS + r + 1; // row-major layout

      if (isPressed && !buttonStates[r][c].pressed) {
          buttonStates[r][c].pressed = true;
          buttonStates[r][c].startTime = millis();
      }
      else if (!isPressed && buttonStates[r][c].pressed) {
          unsigned long duration = millis() - buttonStates[r][c].startTime;
          buttonStates[r][c].pressed = false;

          Serial.print("btn");
          Serial.print(btnNumber);
          Serial.print(duration >= LONG_PRESS_TIME ? " long" : " short");
          Serial.println();
      }
    }

    // deactivate row
    digitalWrite(rowPins[r], HIGH);
  }
}
