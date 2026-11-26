#pragma once
#include "BoardConfig.h"

#if ENABLE_MATTER
#include <string>
#include "esp_timer.h"

enum class MatterState {
    UNCOMMISSIONED,
    COMMISSIONING,
    COMMISSIONED
};

class MatterManager {
public:
    static MatterManager& instance();
    void begin();
    void startCommissioning();  // open commissioning window (stub)
    void factoryReset();        // wipes Wi-Fi + NVS and restarts
    bool isCommissioned() const;

    MatterState getState() const;
    const char* getQrCode() const;
    const char* getManualCode() const;
    int getPinCode() const;
    int getDiscriminator() const;
    int getVid() const;
    int getPid() const;

    void markCommissioned(); // mark state and persist (stub)

public:
    MatterManager() = default;
    void scheduleCommissioningWindowTimeout();
    void onCommissioningTimeout();

    bool commissioned = false;
    MatterState state = MatterState::UNCOMMISSIONED;
    esp_timer_handle_t commissioningTimer = nullptr;
};
#else
class MatterManager {
public:
    static MatterManager& instance() { static MatterManager m; return m; }
    void begin() {}
    void startCommissioning() {}
    void factoryReset() {}
    bool isCommissioned() const { return false; }
    int getPinCode() const { return 0; }
    int getDiscriminator() const { return 0; }
    int getVid() const { return 0; }
    int getPid() const { return 0; }
    const char* getQrCode() const { return ""; }
    const char* getManualCode() const { return ""; }
    MatterState getState() const { return MatterState::UNCOMMISSIONED; }
    void markCommissioned() {}
};
#endif
