#include <TensorFlowLite.h>
#include "model.h"

// TensorFlow Lite libraries
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"

// Tensor arena memory
constexpr int tensor_arena_size = 4 * 1024;
uint8_t tensor_arena[tensor_arena_size];

tflite::MicroInterpreter* interpreter;
TfLiteTensor* input;
TfLiteTensor* output;

// Class labels
const char* gestures[] = {
  "CALL",
  "FIST BUMP",
  "FOUR",
  "GUN",
  "HELLO",
  "NO",
  "POINT",
  "ROCK",
  "SPIDER",
  "YES"
};

void setup() {
  Serial.begin(9600);
  delay(1000);

  // Load model from model.h
  const tflite::Model* tflModel = tflite::GetModel(model);

  // Check model version
  if (tflModel->version() != TFLITE_SCHEMA_VERSION) {
    Serial.println("Model version mismatch!");
    while (1);
  }

  static tflite::AllOpsResolver resolver;

  interpreter = new tflite::MicroInterpreter(
    tflModel,
    resolver,
    tensor_arena,
    tensor_arena_size
  );

  TfLiteStatus allocate_status = interpreter->AllocateTensors();

  if (allocate_status != kTfLiteOk) {
    Serial.println("Tensor allocation failed!");
    while (1);
  }

  input = interpreter->input(0);
  output = interpreter->output(0);

  Serial.println("Model Loaded Successfully!");
}

void loop() {

  // Replace these with real sensor values
  float thumb  = 300;
  float index  = 650;
  float ring   = 700;
  float little = 720;

  // Normalize values (0 to 1)
  input->data.f[0] = thumb / 1023.0;
  input->data.f[1] = index / 1023.0;
  input->data.f[2] = ring / 1023.0;
  input->data.f[3] = little / 1023.0;

  // Run model
  TfLiteStatus invoke_status = interpreter->Invoke();

  if (invoke_status != kTfLiteOk) {
    Serial.println("Inference Failed!");
    delay(1000);
    return;
  }

  // Find highest output score
  int predicted_class = 0;
  float max_val = output->data.f[0];

  for (int i = 1; i < 10; i++) {
    if (output->data.f[i] > max_val) {
      max_val = output->data.f[i];
      predicted_class = i;
    }
  }

  // Print result
  Serial.print("Predicted Gesture: ");
  Serial.println(gestures[predicted_class]);

  delay(1000);
}
