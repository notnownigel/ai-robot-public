# AI Robot - Installation Steps
Using DeGirum - https://github.com/DeGirum/hailo_examples/tree/main

Following - https://github.com/DeGirum/hailo_examples/blob/main/examples/face_recognition.ipynb

## Hardware
Once installed, enable PCIe Gen 3.0. 

Install dependencies:

sudo apt install hailo-all

Reboot then run to verify:

hailortcli fw-control identify

Should see:

Device Architecture: HAILO8

## Hailo RPI
Following - https://github.com/hailo-ai/hailo-rpi5-examples

git clone https://github.com/hailo-ai/hailo-rpi5-examples.git

cd hailo-rpi5-examples

./install.sh

## Hailo Apps setup
https://github.com/hailo-ai/hailo-apps-infra?tab=readme-ov-file

## Environment
python3 -m venv face-recognition

source face-recognition/bin/activate

### Add Site Packages
deactivate

edit pyvenv.cfg

include-system-site-packages = true

source face-recognition/bin/activate

## Setup
pip install --upgrade pip

pip install degirum_cli

pip install lancedb

## Verify
degirum_cli --help 

degirum sys-info

## Testing
degirum_cli predict-video --inference-host-address @local --model-name yolov8n_relu6_coco--640x640_quant_hailort_hailo8_1 --model-zoo-url degirum/hailo
i2cdetect -y 1

## Ollama LLM
### Download and verify install script
curl -fsSL https://ollama.com/install.sh | sh

### Enable service (auto-start on boot)
sudo systemctl enable ollama

### Verify installation
ollama --version  # Should return v0.1.20+

### Python Library
pip install ollama