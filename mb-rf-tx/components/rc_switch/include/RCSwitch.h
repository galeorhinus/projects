#ifndef _RCSwitch_h
#define _RCSwitch_h

#if defined(ARDUINO) && ARDUINO >= 100
    #include "Arduino.h"
#else
    #include <stdint.h>
    #include <stddef.h>
    #include "freertos/FreeRTOS.h"
    #include "freertos/task.h"
    #include "driver/gpio.h"
    #include "esp_timer.h"
    #include "esp_log.h"
    
    // Mapping Arduino-style functions to ESP-IDF
    typedef bool boolean;
    typedef uint8_t byte;
    #define HIGH 1
    #define LOW 0
    #define OUTPUT GPIO_MODE_OUTPUT
    #define INPUT GPIO_MODE_INPUT
    
    // Helper to get micros
    static inline unsigned long micros() {
        return (unsigned long)(esp_timer_get_time());
    }
    
    static inline void delayMicroseconds(unsigned int us) {
        esp_rom_delay_us(us);
    }
#endif


class RCSwitch {

  public:
    RCSwitch();
    
    void enableTransmit(int nTransmitterPin);
    void disableTransmit();
    void setPulseLength(int nPulseLength);
    void setRepeatTransmit(int nRepeatTransmit);
    void setProtocol(int nProtocol);
    void setProtocol(int nProtocol, int nPulseLength);
    void send(unsigned long code, unsigned int length);
    void send(const char* sCodeWord);
    
    void enableReceive(int interrupt);
    void enableReceive();
    void disableReceive();
    bool available();
    void resetAvailable();
    
    unsigned long getReceivedValue();
    unsigned int getReceivedBitlength();
    unsigned int getReceivedDelay();
    unsigned int getReceivedProtocol();
    unsigned int* getReceivedRawdata();

  private:
    int nReceiverInterrupt;
    int nTransmitterPin;
    int nPulseLength;
    int nRepeatTransmit;
    char nProtocol;

    static void handleInterrupt(void* arg);
    bool receiveProtocol(const int p, unsigned int changeCount);
    void transmit(int nHighPulses, int nLowPulses);
};

#endif
