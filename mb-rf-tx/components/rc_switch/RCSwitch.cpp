#include "RCSwitch.h"

/* Format for protocol definitions:
 * {pulselength, Sync bit, "0" bit, "1" bit}
 * * first integer is base pulse length in microseconds (approx.)
 * * next 3 are pairs of high/low pulses (normalized to base pulse length)
 * {high, low}
 */
static const struct Protocol {
    int pulseLength;
    int syncFactor_high; 
    int syncFactor_low;
    int zero_high;
    int zero_low;
    int one_high;
    int one_low;
    bool invertedSignal;
} proto[] = {
    { 350, 1, 31, 1, 3,  3, 1, false },    // protocol 1 (Standard EV1527/PT2262)
    { 650, 1, 10, 1, 2,  2, 1, false },    // protocol 2
    { 100, 30, 71, 4, 11, 9, 6, false },   // protocol 3
};

enum {
   numProto = sizeof(proto) / sizeof(proto[0])
};

volatile unsigned long nReceivedValue = 0;
volatile unsigned int nReceivedBitlength = 0;
volatile unsigned int nReceivedDelay = 0;
volatile unsigned int nReceivedProtocol = 0;
int nReceivedTolerance = 60;
const unsigned int nSeparationLimit = 4300; // Separation between packets (us)

// Variables for the interrupt handler
static unsigned int timings[300]; // buffer to store timing
static unsigned int changeCount = 0;
static unsigned long lastTime = 0;
static unsigned int repeatCount = 0;

RCSwitch::RCSwitch() {
  this->nTransmitterPin = -1;
  this->setPulseLength(350);
  this->setRepeatTransmit(10);
  this->setProtocol(1);
  this->nReceiverInterrupt = -1;
}

// --- TRANSMITTER METHODS ---

void RCSwitch::setProtocol(int nProtocol) {
  this->nProtocol = nProtocol;
  if (nProtocol == 1){
    this->setPulseLength(350);
  } else if (nProtocol == 2) {
    this->setPulseLength(650);
  } else if (nProtocol == 3) {
    this->setPulseLength(100);
  }
}

void RCSwitch::setProtocol(int nProtocol, int nPulseLength) {
  this->nProtocol = nProtocol;
  this->setPulseLength(nPulseLength);
}

void RCSwitch::setPulseLength(int nPulseLength) {
  this->nPulseLength = nPulseLength;
}

void RCSwitch::setRepeatTransmit(int nRepeatTransmit) {
  this->nRepeatTransmit = nRepeatTransmit;
}

void RCSwitch::enableTransmit(int nTransmitterPin) {
  this->nTransmitterPin = nTransmitterPin;
  gpio_reset_pin((gpio_num_t)this->nTransmitterPin);
  gpio_set_direction((gpio_num_t)this->nTransmitterPin, GPIO_MODE_OUTPUT);
}

void RCSwitch::disableTransmit() {
  this->nTransmitterPin = -1;
}

void RCSwitch::send(unsigned long code, unsigned int length) {
  if (this->nTransmitterPin == -1) return;

  for (int nRepeat = 0; nRepeat < nRepeatTransmit; nRepeat++) {
    for (int i = length-1; i >= 0; i--) {
      if (code & (1L << i))
        this->transmit(proto[nProtocol-1].one_high, proto[nProtocol-1].one_low);
      else
        this->transmit(proto[nProtocol-1].zero_high, proto[nProtocol-1].zero_low);
    }
    this->transmit(proto[nProtocol-1].syncFactor_high, proto[nProtocol-1].syncFactor_low);
  }
}

void RCSwitch::transmit(int nHighPulses, int nLowPulses) {
    boolean inverted = proto[nProtocol-1].invertedSignal;
    int basePulse = this->nPulseLength;
    
    gpio_set_level((gpio_num_t)this->nTransmitterPin, inverted ? LOW : HIGH);
    delayMicroseconds(basePulse * nHighPulses);
    gpio_set_level((gpio_num_t)this->nTransmitterPin, inverted ? HIGH : LOW);
    delayMicroseconds(basePulse * nLowPulses);
}

// --- RECEIVER METHODS ---

void RCSwitch::enableReceive(int interrupt) {
  this->nReceiverInterrupt = interrupt;
  this->enableReceive();
}

void RCSwitch::enableReceive() {
  if (this->nReceiverInterrupt != -1) {
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_ANYEDGE;
    io_conf.pin_bit_mask = (1ULL << this->nReceiverInterrupt);
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE; // RF modules usually drive active high/low
    gpio_config(&io_conf);

    gpio_install_isr_service(0);
    gpio_isr_handler_add((gpio_num_t)this->nReceiverInterrupt, RCSwitch::handleInterrupt, this);
  }
}

void RCSwitch::disableReceive() {
  // Not fully implemented for ESP-IDF/ISR cleanup in this snippet
  this->nReceiverInterrupt = -1;
}

bool RCSwitch::available() {
  return nReceivedValue != 0;
}

void RCSwitch::resetAvailable() {
  nReceivedValue = 0;
}

unsigned long RCSwitch::getReceivedValue() {
  return nReceivedValue;
}

unsigned int RCSwitch::getReceivedBitlength() {
  return nReceivedBitlength;
}

unsigned int RCSwitch::getReceivedDelay() {
  return nReceivedDelay;
}

unsigned int RCSwitch::getReceivedProtocol() {
  return nReceivedProtocol;
}

unsigned int* RCSwitch::getReceivedRawdata() {
  return timings;
}

// --- INTERRUPT HANDLER ---

void IRAM_ATTR RCSwitch::handleInterrupt(void* arg) {
    // RCSwitch* self = (RCSwitch*)arg; // Not needed for static logic
    unsigned long time = micros();
    unsigned int duration = time - lastTime;

    if (duration > nSeparationLimit && duration > timings[0] - 200 && duration < timings[0] + 200) {
       repeatCount++; // Check for repeats
       changeCount--; 
       
       if (repeatCount == 2) {
            // Decoded signal (decoding logic simplified for brevity/stability)
            // In a real ISR, we would trigger a task notification.
            // For now, we rely on the loop checking available().
       }
       changeCount = 0;
    } else if (duration > 5000) { // Sync pulse detected
        changeCount = 0;
    }
 
    if (changeCount >= 300) {
        changeCount = 0;
        lastTime = time;
        return;
    }

    timings[changeCount++] = duration;
    lastTime = time;
    
    // Attempt decoding on the fly if buffer looks full or sync received
    // Note: The original RC-Switch does decoding here. 
    // We are implementing a simplified logic to catch Protocol 1
    if (changeCount > 20 && duration > 5000) {
         // Try to decode protocol 1
         unsigned long code = 0;
         unsigned int delay = timings[0] / 31;
         unsigned int bits = (changeCount - 1) / 2;
         
         if (bits > 0) {
            bool fail = false;
            for (int i = 1; i < changeCount - 1; i += 2) {
                code <<= 1;
                // Logic 0: High(1) Low(3)
                // Logic 1: High(3) Low(1)
                // We check the High pulse (timings[i])
                if (timings[i] > delay * 2 && timings[i+1] < delay * 2) {
                    code |= 1; // It's a 1
                } else if (timings[i] < delay * 2 && timings[i+1] > delay * 2) {
                    // It's a 0
                } else {
                    fail = true;
                }
            }
            if (!fail) {
                nReceivedValue = code;
                nReceivedBitlength = bits;
                nReceivedDelay = delay;
                nReceivedProtocol = 1;
            }
         }
    }
}
