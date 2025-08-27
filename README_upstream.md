**CosyVoice 2.0** has been released! Compared to version 1.0, the new version offers more accurate, more stable, faster, and better speech generation capabilities.
### Multilingual
- **Supported Language**: Chinese, English, Japanese, Korean, Chinese dialects (Cantonese, Sichuanese, Shanghainese, Tianjinese, Wuhanese, etc.)
- **Crosslingual & Mixlingual**：Support zero-shot voice cloning for cross-lingual and code-switching scenarios.
### Ultra-Low Latency
- **Bidirectional Streaming Support**: CosyVoice 2.0 integrates offline and streaming modeling technologies.
- **Rapid First Packet Synthesis**: Achieves latency as low as 150ms while maintaining high-quality audio output.
### High Accuracy
- **Improved Pronunciation**: Reduces pronunciation errors by 30% to 50% compared to CosyVoice 1.0.
- **Benchmark Achievements**: Attains the lowest character error rate on the hard test set of the Seed-TTS evaluation set.
### Strong Stability
- **Consistency in Timbre**: Ensures reliable voice consistency for zero-shot and cross-language speech synthesis.
- **Cross-language Synthesis**: Marked improvements compared to version 1.0.
### Natural Experience
- **Enhanced Prosody and Sound Quality**: Improved alignment of synthesized audio, raising MOS evaluation scores from 5.4 to 5.53.
- **Emotional and Dialectal Flexibility**: Now supports more granular emotional controls and accent adjustments.

## Roadmap

- [x] 2025/08

    - [x] Thanks to the contribution from NVIDIA Yuekai Zhang, add triton trtllm runtime support

- [x] 2025/07

    - [x] release cosyvoice 3.0 eval set

- [x] 2025/05

    - [x] add cosyvoice 2.0 vllm support

- [x] 2024/12

    - [x] 25hz cosyvoice 2.0 released

- [x] 2024/09

    - [x] 25hz cosyvoice base model
    - [x] 25hz cosyvoice voice conversion model

- [x] 2024/08

    - [x] Repetition Aware Sampling(RAS) for llm stability
    - [x] Streaming inference mode support, including kv cache and sdpa for rtf optimization

- [x] 2024/07

    - [x] Flow matching training support
    - [x] WeTextProcessing support when ttsfrd is not available
    - [x] Fastapi server and client


## Install

### Clone and install

- Clone the repo

    ``` sh
    git clone --recursive https://github.com/FunAudioLLM/CosyVoice
    # If you failed to clone the submodule due to network failures, please run the following command until success
    cd CosyVoice
    git submodule update --init --recursive
    ```

- Create environment and install dependencies:

    ``` sh
    conda create -n cosyvoice python=3.10
    conda activate cosyvoice
    pip install -r requirements.txt
    ```

#### Using vLLM for deployment

Notice that `vllm==v0.9.0` has a lot of specific requirements, for example `torch==2.7.0`. You can create a new env to in case your hardward do not support vllm and old env is corrupted.

``` sh
conda create -n cosyvoice_vllm --clone cosyvoice
conda activate cosyvoice_vllm
pip install vllm==v0.9.0 -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
python vllm_example.py
```

#### Example Usage

```python
cosyvoice = CosyVoice('pretrained_models/CosyVoice-300M-Instruct')
# instruct usage, support <laughter></laughter><strong></strong>[laughter][breath]
for i, j in enumerate(cosyvoice.inference_instruct('在面对挑战时，他展现了非凡的<strong>勇气</strong>与<strong>智慧</strong>。', '中文男', 'Theo \'Crimson\', is a fiery, passionate rebel leader. Fights with fervor for justice, but struggles with impulsiveness.', stream=False)):
    torchaudio.save('instruct_{}.wav'.format(i), j['tts_speech'], cosyvoice.sample_rate)
```

#### Start web demo

You can use our web demo page to get familiar with CosyVoice quickly.

Please see the demo website for details.

```python
# change iic/CosyVoice-300M-SFT for sft inference, or iic/CosyVoice-300M-Instruct for instruct inference
python3 webui.py --port 50000 --model_dir pretrained_models/CosyVoice-300M
```

#### Advanced Usage

For advanced users, we have provided training and inference scripts in `examples/libritts/cosyvoice/run.sh`.

#### Build for deployment

Optionally, if you want service deployment,
You can run the following steps.

``` sh
cd runtime/python
docker build -t cosyvoice:v1.0 .
# change iic/CosyVoice-300M to iic/CosyVoice-300M-Instruct if you want to use instruct inference
# for grpc usage
docker run -d --runtime=nvidia -p 50000:50000 cosyvoice:v1.0 /bin/bash -c "cd /opt/CosyVoice/CosyVoice/runtime/python/grpc && python3 server.py --port 50000 --max_conc 4 --model_dir iic/CosyVoice-300M && sleep infinity"
cd grpc && python3 client.py --port 50000 --mode <sft|zero_shot|cross_lingual|instruct>
# for fastapi usage
docker run -d --runtime=nvidia -p 50000:50000 cosyvoice:v1.0 /bin/bash -c "cd /opt/CosyVoice/CosyVoice/runtime/python/fastapi && python3 server.py --port 50000 --model_dir iic/CosyVoice-300M && sleep infinity"
cd fastapi && python3 client.py --port 50000 --mode <sft|zero_shot|cross_lingual|instruct>
```

## Discussion & Communication

You can directly discuss on [Github Issues](https://github.com/FunAudioLLM/CosyVoice/issues).

You can also scan the QR code to join our official Dingding chat group.

<img src="./asset/dingding.png" width="250px">

## Acknowledge

1. We borrowed a lot of code from [FunASR](https://github.com/modelscope/FunASR).
2. We borrowed a lot of code from [FunCodec](https://github.com/modelscope/FunCodec).
3. We borrowed a lot of code from [Matcha-TTS](https://github.com/shivammehta25/Matcha-TTS).
4. We borrowed a lot of code from [AcademiCodec](https://github.com/yangdongchao/AcademiCodec).
5. We borrowed a lot of code from [WeNet](https://github.com/wenet-e2e/wenet).

## Citations

``` bibtex
@article{du2024cosyvoice,
  title={Cosyvoice: A scalable multilingual zero-shot text-to-speech synthesizer based on supervised semantic tokens},
  author={Du, Zhihao and Chen, Qian and Zhang, Shiliang and Hu, Kai and Lu, Heng and Yang, Yexin and Hu, Hangrui and Zheng, Siqi and Gu, Yue and Ma, Ziyang and others},
  journal={arXiv preprint arXiv:2407.05407},
  year={2024}
}

@article{du2024cosyvoice,
  title={Cosyvoice 2: Scalable streaming speech synthesis with large language models},
  author={Du, Zhihao and Wang, Yuxuan and Chen, Qian and Shi, Xian and Lv, Xiang and Zhao, Tianyu and Gao, Zhifu and Yang, Yexin and Gao, Changfeng and Wang, Hui and others},
  journal={arXiv preprint arXiv:2412.10117},
  year={2024}
}

@article{du2025cosyvoice,
  title={CosyVoice 3: Towards In-the-wild Speech Generation via Scaling-up and Post-training},
  author={Du, Zhihao and Gao, Changfeng and Wang, Yuxuan and Yu, Fan and Zhao, Tianyu and Wang, Hao and Lv, Xiang and Wang, Hui and Shi, Xian and An, Keyu and others},
  journal={arXiv preprint arXiv:2505.17589},
  year={2025}
}

@inproceedings{lyu2025build,
  title={Build LLM-Based Zero-Shot Streaming TTS System with Cosyvoice},
  author={Lyu, Xiang and Wang, Yuxuan and Zhao, Tianyu and Wang, Hao and Liu, Huadai and Du, Zhihao},
  booktitle={ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  pages={1--2},
  year={2025},
  organization={IEEE}
}
```

## Disclaimer
The content provided above is for academic purposes only and is intended to demonstrate technical capabilities. Some examples are sourced from the internet. If any content infringes on your rights, please contact us to request its removal.