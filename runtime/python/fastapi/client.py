# Copyright (c) 2024 Alibaba Inc (authors: Xiang Lyu)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import logging
import requests
import torch
import torchaudio
import numpy as np
from pathlib import Path


def main():
    url = "http://{}:{}/inference_{}".format(args.host, args.port, args.mode)
    
    # Default to POST, GET is not suitable for file uploads or large payloads
    method = "POST"
    files = None
    payload = {
        'tts_text': args.tts_text
    }

    if args.mode == 'sft':
        payload['spk_id'] = args.spk_id
    elif args.mode == 'zero_shot':
        payload['prompt_text'] = args.prompt_text
        files = [('prompt_wav', (Path(args.prompt_wav).name, open(args.prompt_wav, 'rb'), 'audio/wav'))]
    elif args.mode == 'cross_lingual':
        files = [('prompt_wav', (Path(args.prompt_wav).name, open(args.prompt_wav, 'rb'), 'audio/wav'))]
    elif args.mode == 'instruct':
        payload['spk_id'] = args.spk_id
        payload['instruct_text'] = args.instruct_text
    
    print(f"Sending {method} request to {url}...")
    response = requests.request(method, url, data=payload, files=files, stream=True)

    # --- FIX: Check if the request was successful before processing the response --- 
    if not response.ok:
        logging.error(f"Server returned an error: {response.status_code}")
        # Try to print the error message from the server
        try:
            error_info = response.json()
            logging.error(f"Server error details: {error_info}")
        except requests.exceptions.JSONDecodeError:
            logging.error(f"Server response (non-JSON): {response.text[:1000]}")
        return # Stop processing

    tts_audio = b''
    for r in response.iter_content(chunk_size=16000):
        tts_audio += r
    
    # Convert the 16-bit integer bytes to a float tensor and normalize to [-1, 1]
    tts_speech_int16 = torch.from_numpy(np.frombuffer(tts_audio, dtype=np.int16))
    # The unsqueeze is to create a (1, num_samples) shape, which is valid for mono
    tts_speech_float32 = (tts_speech_int16.float() / 32768.0).unsqueeze(dim=0)

    logging.info('save response to {}'.format(args.tts_wav))
    # Use the recommended torchcodec encoder to save the audio
    try:
        from torchcodec.encoders import AudioEncoder
        encoder = AudioEncoder(samples=tts_speech_float32, sample_rate=target_sr)
        encoder.to_file(args.tts_wav)
    except (ImportError, ModuleNotFoundError):
        logging.warning('torchcodec not found, falling back to torchaudio.save. Please consider installing torchcodec for future compatibility.')
        torchaudio.save(args.tts_wav, tts_speech_float32, target_sr)
    logging.info('get response')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        type=str,
                        default='0.0.0.0')
    parser.add_argument('--port',
                        type=int,
                        default='50000')
    parser.add_argument('--mode',
                        default='sft',
                        choices=['sft', 'zero_shot', 'cross_lingual', 'instruct'],
                        help='request mode')
    parser.add_argument('--tts_text',
                        type=str,
                        default='你好，我是通义千问语音合成大模型，请问有什么可以帮您的吗？')
    parser.add_argument('--spk_id',
                        type=str,
                        default='中文女')
    parser.add_argument('--prompt_text',
                        type=str,
                        default='希望你以后能够做的比我还好呦。')
    parser.add_argument('--prompt_wav',
                        type=str,
                        default='../../../asset/zero_shot_prompt.wav')
    parser.add_argument('--instruct_text',
                        type=str,
                        default='Theo \'Crimson\', is a fiery, passionate rebel leader. \
                                 Fights with fervor for justice, but struggles with impulsiveness.')
    parser.add_argument('--tts_wav',
                        type=str,
                        default='demo.wav')
    args = parser.parse_args()
    prompt_sr, target_sr = 16000, 24000
    main()
