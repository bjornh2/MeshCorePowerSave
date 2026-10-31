#pragma once

#define RADIOLIB_STATIC_ONLY 1
#include <RadioLib.h>
#include <XiaoC6Board.h>
#include <helpers/radiolib/RadioLibWrappers.h>
#include <helpers/ESP32Board.h>
#include <helpers/radiolib/CustomSX1262Wrapper.h>
#include <helpers/AutoDiscoverRTCClock.h>
#include <helpers/SensorManager.h>
#if defined(ENV_INCLUDE_BME280) || defined(ENV_INCLUDE_BMP280) || defined(ENV_INCLUDE_INA3221)
  #include <helpers/sensors/EnvironmentSensorManager.h>
#endif
#ifdef DISPLAY_CLASS
  #include <helpers/ui/SSD1306Display.h>
  #include <helpers/ui/MomentaryButton.h>
#endif

extern XiaoC6Board board;
extern WRAPPER_CLASS radio_driver;
extern AutoDiscoverRTCClock rtc_clock;
#if defined(ENV_INCLUDE_BME280) || defined(ENV_INCLUDE_BMP280) || defined(ENV_INCLUDE_INA3221)
  extern EnvironmentSensorManager sensors;
#else
  extern SensorManager sensors;
#endif

#ifdef DISPLAY_CLASS
  extern DISPLAY_CLASS display;
  extern MomentaryButton user_btn;
#endif

bool radio_init();
mesh::LocalIdentity radio_new_identity();

