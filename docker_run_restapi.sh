#!/bin/bash

docker run -d \
      -p 50000:50000 \
      -v ./pretrained_models:/opt/CosyVoice/pretrained_models \
      --name cosyvoice-mac \
      cosyvoice-mac:v1.0 \
      python rest-api.py \
      --disable-download \
      --preload-models tts \
      --models-dir ./pretrained_models
      