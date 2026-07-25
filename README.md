# VocalHand — AI-Driven Assistive Glove for Sign Language Translation

A wearable smart glove that translates hand gestures into speech, with two-way communication support — built as a course project for IoT-Based Systems (UEC-640) at Thapar Institute of Engineering and Technology.

## Team

5-member team project. This repository reflects the components I personally worked on: the mobile application and hardware wiring/connections.

## Problem Statement

Many individuals with speech and hearing impairments face difficulty communicating because sign language isn't widely understood. VocalHand addresses this by converting hand gestures into spoken words in real time, while also converting spoken responses back into text — enabling two-way communication.

## System Overview

- **Flex sensors** (one per finger) capture finger bending
- A **microcontroller** (Arduino) reads sensor data and runs a lightweight TinyML gesture recognition model on-device
- Recognized gestures are transmitted via **Bluetooth** to a companion mobile app
- The app displays the gesture as text and converts it to **speech**
- A **speech-to-text** module allows the hearing-impaired user to read spoken responses from others

## My Contribution

### Mobile Application (MIT App Inventor)
Built the companion Android app, including:
- Bluetooth connectivity to receive gesture data from the glove
- Text-to-Speech integration to voice recognized gestures
- Speech Recognizer integration for two-way communication (converting spoken responses to text)

All three components — Bluetooth connection, text-to-speech, and speech recognition — were functional.

### Hardware — Wiring & Connections
Assisted with wiring the flex sensors and other components to the microcontroller, ensuring the circuit was correctly set up for reliable analog sensor readings.

## Project Status

Flex sensors functioned correctly in early testing — gesture-related output was verified via the Arduino Serial Monitor. Over time, the flex sensors experienced physical wear/degradation, a common issue with this sensor type. After the TinyML gesture recognition model was built and deployed by a teammate, final end-to-end results were partial rather than fully consistent, due to this sensor degradation.

The mobile application itself functioned reliably and independently of the sensor issues.

## Tech Stack

MIT App Inventor · Arduino (C++) · TensorFlow Lite Micro · Python (model training) · Bluetooth (BLE)

## Repository Contents

- `iottoi.pdf` — team's submitted project report
- `budget.pdf` — component sourcing and budget breakdown
- `model.h`, `gesture_model.tflite` — trained gesture recognition model (built by teammate)
- Arduino firmware code
- Python model training script

## Notes

This was a hands-on hardware + software learning project. It highlighted the practical gap between a working proof-of-concept and a fully polished, reliable final product — particularly around physical sensor reliability in wearable devices.
