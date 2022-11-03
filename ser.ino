int led = 3;
int rrr = A0;
bool env = false;
int incomingByte = 0;  

void setup() {
        Serial.begin(9600);     
        pinMode(led, OUTPUT);
        pinMode(rrr, INPUT);
}

void loop() {
        int val = analogRead(rrr);
        Serial.println(val);
        delay(100);
        if (Serial.available() > 0) {
                
                // read the incoming byte:
                incomingByte = Serial.read();
                if(incomingByte == '1'){
                  env = true;
                  }
                else if(incomingByte == '0'){
                  env = false;
                }

                else if(incomingByte == '2'){
                  env = !env;
                }
                digitalWrite(led, env);
          
        }
}
 
