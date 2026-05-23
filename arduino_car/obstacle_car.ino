#include <NewPing.h>

// ======================================================
// HC-SR04 超音波感測器設定
// ======================================================

#define LEFT_TRIG_PIN     6
#define LEFT_ECHO_PIN     7

#define CENTER_TRIG_PIN   10
#define CENTER_ECHO_PIN   11

#define RIGHT_TRIG_PIN    12
#define RIGHT_ECHO_PIN    13

#define MAX_DISTANCE      200   // 最大偵測距離（cm）
#define SAFE_DISTANCE     25    // 安全距離（cm）

// ======================================================
// 馬達控制腳位
// ======================================================

#define RIGHT_MOTOR_IN1   5
#define RIGHT_MOTOR_IN2   4

#define LEFT_MOTOR_IN3    3
#define LEFT_MOTOR_IN4    2

// ======================================================
// 建立超音波感測器物件
// ======================================================

NewPing sonarLeft(
  LEFT_TRIG_PIN,
  LEFT_ECHO_PIN,
  MAX_DISTANCE
);

NewPing sonarCenter(
  CENTER_TRIG_PIN,
  CENTER_ECHO_PIN,
  MAX_DISTANCE
);

NewPing sonarRight(
  RIGHT_TRIG_PIN,
  RIGHT_ECHO_PIN,
  MAX_DISTANCE
);

// ======================================================
// Setup
// ======================================================

void setup() {

  // 馬達輸出設定
  pinMode(RIGHT_MOTOR_IN1, OUTPUT);
  pinMode(RIGHT_MOTOR_IN2, OUTPUT);

  pinMode(LEFT_MOTOR_IN3, OUTPUT);
  pinMode(LEFT_MOTOR_IN4, OUTPUT);

  // Serial Monitor
  Serial.begin(9600);

  Serial.println("Obstacle Avoidance Car Started");
}

// ======================================================
// Main Loop
// ======================================================

void loop() {

  // 讀取距離
  int leftDistance   = readDistance(sonarLeft);
  int centerDistance = readDistance(sonarCenter);
  int rightDistance  = readDistance(sonarRight);

  // 顯示感測器資訊
  printDistanceInfo(
    leftDistance,
    centerDistance,
    rightDistance
  );

  // ==================================================
  // 避障邏輯
  // ==================================================

  // 前方有障礙物
  if (centerDistance > 0 &&
      centerDistance < SAFE_DISTANCE) {

    stopMotors();

    moveBackward();
    delay(500);

    stopMotors();
    delay(200);

    // 比較左右距離
    if (leftDistance > rightDistance) {

      Serial.println("Turning Left");
      turnLeft();

    } else {

      Serial.println("Turning Right");
      turnRight();
    }

  } else {

    // 前方安全
    moveForward();
  }

  delay(100);
}

// ======================================================
// 感測器讀取
// ======================================================

int readDistance(NewPing &sensor) {

  int distance = sensor.ping_cm();

  // 避免回傳 0
  if (distance == 0) {
    return MAX_DISTANCE;
  }

  return distance;
}

// ======================================================
// 顯示感測器資訊
// ======================================================

void printDistanceInfo(
  int left,
  int center,
  int right
) {

  Serial.print("Left: ");
  Serial.print(left);

  Serial.print(" cm | Center: ");
  Serial.print(center);

  Serial.print(" cm | Right: ");
  Serial.print(right);

  Serial.println(" cm");
}

// ======================================================
// 馬達控制
// ======================================================

void moveForward() {

  digitalWrite(RIGHT_MOTOR_IN1, HIGH);
  digitalWrite(RIGHT_MOTOR_IN2, LOW);

  digitalWrite(LEFT_MOTOR_IN3, HIGH);
  digitalWrite(LEFT_MOTOR_IN4, LOW);
}

void moveBackward() {

  digitalWrite(RIGHT_MOTOR_IN1, LOW);
  digitalWrite(RIGHT_MOTOR_IN2, HIGH);

  digitalWrite(LEFT_MOTOR_IN3, LOW);
  digitalWrite(LEFT_MOTOR_IN4, HIGH);
}

void turnLeft() {

  digitalWrite(RIGHT_MOTOR_IN1, HIGH);
  digitalWrite(RIGHT_MOTOR_IN2, LOW);

  digitalWrite(LEFT_MOTOR_IN3, LOW);
  digitalWrite(LEFT_MOTOR_IN4, HIGH);

  delay(400);

  stopMotors();
}

void turnRight() {

  digitalWrite(RIGHT_MOTOR_IN1, LOW);
  digitalWrite(RIGHT_MOTOR_IN2, HIGH);

  digitalWrite(LEFT_MOTOR_IN3, HIGH);
  digitalWrite(LEFT_MOTOR_IN4, LOW);

  delay(400);

  stopMotors();
}

void stopMotors() {

  digitalWrite(RIGHT_MOTOR_IN1, LOW);
  digitalWrite(RIGHT_MOTOR_IN2, LOW);

  digitalWrite(LEFT_MOTOR_IN3, LOW);
  digitalWrite(LEFT_MOTOR_IN4, LOW);
}