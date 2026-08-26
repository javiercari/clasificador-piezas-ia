// Pins del sensor ultrasónico HC-SR04
const int PIN_TRIG = 9;
const int PIN_ECHO = 8;

void setup() {
  Serial.begin(115200);
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
}

void loop() {
  // Generar pulso de 10 microsegundos en TRIG
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  // Medir el tiempo de retorno en ECHO
  long duracion = pulseIn(PIN_ECHO, HIGH);

  // Calcular la distancia en centímetros
  int distancia = duracion * 0.034 / 2;

  // Enviar el dato por puerto serial (un solo número por línea)
  Serial.println(distancia);

  // Pausa entre lecturas (ajusta según la velocidad de la banda)
  delay(50); 
}