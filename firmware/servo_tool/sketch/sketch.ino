// servo_tool: test, centre and pre-position the twelve leg servos before assembly.
//
// Hardware: Arduino UNO Q + Adafruit 16-channel PWM/Servo Shield (PCA9685 at 0x40) on its headers,
// SZBK07 set to 6.0 V on the shield's V+ terminal. DS3218 180-degree servos (500-2500 us).
// Build guide: https://beriberikix.github.io/spotmicro-arduino-q/prepare/servos/
//
// Runs as an Arduino App Lab app (firmware/servo_tool). Two ways to drive it:
//  - the web page served by the app's Python side (python/main.py, assets/), which walks through the build guide's
//    steps and calls the functions below over the Bridge (set_angle, set_off, test_sweep);
//  - App Lab's Console > Serial Monitor, through the Bridge's Monitor (plain Serial is the D0/D1 UART on the UNO Q).
// Serial Monitor commands, typed and sent with Enter:
//   h              help and channel map
//   c              centre every channel (90 deg, 1500 us)
//   a              assembly angles (shoulders 90, hips L120/R60, knees L180/R0)
//   a <ch>         assembly angle for one channel
//   s <ch> <deg>   set one channel to an angle (0-180)
//   u <ch> <us>    set one channel to a pulse width in microseconds (500-2500)
//   t <ch>         test: sweep one channel 45-135 deg twice, then back to 90
//   o              all outputs off (servos go limp)
//   o <ch>         one output off
// Nothing moves until you type a command: at power-up every output is off.
//
// MIT License, see ../../LICENSE.

#include <Arduino_RouterBridge.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm(0x40, Wire);

const uint16_t US_MIN = 500;     // pulse at 0 deg
const uint16_t US_MAX = 2500;    // pulse at 180 deg
const uint8_t CHANNELS = 12;

// Channel map (shield channel -> joint). The firmware will use the same order.
struct Joint {
  const char *name;
  uint8_t assembly_deg;  // angle the servo must be at when its horn is fitted
};
const Joint JOINTS[CHANNELS] = {
  {"FL shoulder", 90}, {"FL hip", 120}, {"FL knee", 180},
  {"FR shoulder", 90}, {"FR hip", 60},  {"FR knee", 0},
  {"RL shoulder", 90}, {"RL hip", 120}, {"RL knee", 180},
  {"RR shoulder", 90}, {"RR hip", 60},  {"RR knee", 0},
};

uint16_t degToUs(float deg) {
  if (deg < 0) deg = 0;
  if (deg > 180) deg = 180;
  return US_MIN + (uint16_t)(deg * (US_MAX - US_MIN) / 180.0f + 0.5f);
}

void setUs(uint8_t ch, uint16_t us) {
  pwm.writeMicroseconds(ch, us);
}

void off(uint8_t ch) {
  pwm.setPWM(ch, 0, 4096);  // full off: no pulses, the servo goes limp
}

void report(uint8_t ch, int deg) {
  Monitor.print("  ch ");
  Monitor.print(ch);
  Monitor.print(" (");
  Monitor.print(JOINTS[ch].name);
  Monitor.print(") -> ");
  Monitor.print(deg);
  Monitor.print(" deg, ");
  Monitor.print(degToUs(deg));
  Monitor.println(" us");
}

void help() {
  Monitor.println();
  Monitor.println("servo_tool commands:");
  Monitor.println("  c            centre all (90 deg)");
  Monitor.println("  a [ch]       assembly angles (all, or one channel)");
  Monitor.println("  s ch deg     set angle 0-180");
  Monitor.println("  u ch us      set pulse 500-2500 us");
  Monitor.println("  t ch         test sweep");
  Monitor.println("  o [ch]       outputs off (all, or one channel)");
  Monitor.println("Channel map (assembly angle):");
  for (uint8_t i = 0; i < CHANNELS; i++) {
    Monitor.print("  ");
    if (i < 10) Monitor.print(' ');
    Monitor.print(i);
    Monitor.print("  ");
    Monitor.print(JOINTS[i].name);
    Monitor.print("  ");
    Monitor.println(JOINTS[i].assembly_deg);
  }
}

bool validChannel(long ch) {
  if (ch < 0 || ch >= CHANNELS) {
    Monitor.println("  channel must be 0-11");
    return false;
  }
  return true;
}

int8_t pendingSweep = -1;  // channel waiting for a test sweep from the web page, run from loop()

void sweep(uint8_t ch) {
  Monitor.print("  sweeping ch ");
  Monitor.println(ch);
  for (int rep = 0; rep < 2; rep++) {
    for (int d = 90; d <= 135; d++) { setUs(ch, degToUs(d)); delay(15); }
    for (int d = 135; d >= 45; d--) { setUs(ch, degToUs(d)); delay(15); }
    for (int d = 45; d <= 90; d++) { setUs(ch, degToUs(d)); delay(15); }
  }
  report(ch, 90);
}

void handle(String line) {
  line.trim();
  if (line.length() == 0) return;
  char cmd = tolower(line.charAt(0));
  String rest = line.substring(1);
  rest.trim();
  int space = rest.indexOf(' ');
  bool hasA = rest.length() > 0;
  long a = hasA ? rest.toInt() : -1;
  bool hasB = space > 0;
  long b = hasB ? rest.substring(space + 1).toInt() : -1;

  switch (cmd) {
    case 'h':
    case '?':
      help();
      break;
    case 'c':
      Monitor.println("Centre all:");
      for (uint8_t i = 0; i < CHANNELS; i++) { setUs(i, degToUs(90)); report(i, 90); delay(60); }
      break;
    case 'a':
      if (hasA) {
        if (!validChannel(a)) break;
        setUs(a, degToUs(JOINTS[a].assembly_deg));
        report(a, JOINTS[a].assembly_deg);
      } else {
        Monitor.println("Assembly angles:");
        for (uint8_t i = 0; i < CHANNELS; i++) {
          setUs(i, degToUs(JOINTS[i].assembly_deg));
          report(i, JOINTS[i].assembly_deg);
          delay(60);  // stagger the starts so the rail doesn't see twelve inrush spikes at once
        }
      }
      break;
    case 's':
      if (!hasB) { Monitor.println("  usage: s <ch> <deg>"); break; }
      if (!validChannel(a)) break;
      setUs(a, degToUs(b));
      report(a, (int)constrain(b, 0, 180));
      break;
    case 'u':
      if (!hasB) { Monitor.println("  usage: u <ch> <us>"); break; }
      if (!validChannel(a)) break;
      b = constrain(b, US_MIN, US_MAX);
      setUs(a, b);
      Monitor.print("  ch ");
      Monitor.print(a);
      Monitor.print(" -> ");
      Monitor.print(b);
      Monitor.println(" us");
      break;
    case 't':
      if (!hasA) { Monitor.println("  usage: t <ch>"); break; }
      if (!validChannel(a)) break;
      sweep(a);
      break;
    case 'o':
      if (hasA) {
        if (!validChannel(a)) break;
        off(a);
        Monitor.print("  ch ");
        Monitor.print(a);
        Monitor.println(" off");
      } else {
        for (uint8_t i = 0; i < 16; i++) off(i);
        Monitor.println("  all outputs off");
      }
      break;
    default:
      Monitor.println("  unknown command; type h for help");
  }
}

// ---- Bridge functions for the web page. provide_safe runs them between loop() iterations, so they never
// share the I2C bus with a command from the Serial Monitor.
void rpcSetAngle(int ch, int deg) {
  if (ch < 0 || ch >= CHANNELS) return;
  deg = constrain(deg, 0, 180);
  setUs(ch, degToUs(deg));
  report(ch, deg);
}

void rpcOff(int ch) {
  if (ch < 0) {
    for (uint8_t i = 0; i < 16; i++) off(i);
    Monitor.println("  all outputs off (web)");
  } else if (ch < CHANNELS) {
    off(ch);
    Monitor.print("  ch ");
    Monitor.print(ch);
    Monitor.println(" off (web)");
  }
}

void rpcTestSweep(int ch) {
  if (ch >= 0 && ch < CHANNELS) pendingSweep = ch;  // the sweep takes ~3 s: run it from loop(), not inside the call
}

void setup() {
  Monitor.begin();
  Bridge.begin();
  Bridge.provide_safe("set_angle", rpcSetAngle);
  Bridge.provide_safe("set_off", rpcOff);
  Bridge.provide_safe("test_sweep", rpcTestSweep);
  Wire.begin();
  // The shield ties A4/A5 to SDA/SCL. Leave A4/A5 unused (and don't call Wire2.begin()).
  if (!pwm.begin()) {
    Monitor.println("PCA9685 not found at 0x40. Check the shield is seated on the headers and VCC select is soldered to 3V.");
  }
  pwm.setOscillatorFrequency(25000000);
  pwm.setPWMFreq(50);
  for (uint8_t i = 0; i < 16; i++) off(i);
  delay(500);
  Monitor.println("servo_tool ready. All outputs off.");
  help();
}

void loop() {
  if (Monitor.available()) {
    handle(Monitor.readStringUntil('\n'));
  }
  if (pendingSweep >= 0) {
    uint8_t ch = pendingSweep;
    pendingSweep = -1;
    sweep(ch);
  }
}
