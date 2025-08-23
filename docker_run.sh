#!/bin/bash

docker run -d \
      -p 50000:50000 \
      -v ./pretrained_models:/opt/CosyVoice/pretrained_models \
      --name cosyvoice-mac \
      cosyvoice-mac:v1.0 \
      python runtime/python/fastapi/server.py \
      --port 50000 \
      --model_dir "/opt/CosyVoice/pretrained_models/CosyVoice2-0.5B" \
      --load_jit \
      --fp16
      