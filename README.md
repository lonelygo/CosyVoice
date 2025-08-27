## 对于使用 Apple Silicon M 系列芯片的 macOS 用户

本`fork`已经在`M4 MacBook Pro`上进行了测试，并且启用了`torch`的`mps`后端，以便获得更优的性能。

同时提供了`macOS`下的`Dockerfile`可以构建镜像。但是，并不建议这样使用，因为目前`macOS`下`Docker`并不支持`GPU直通`模式，所以，如果你用`Docker`运行，就只能跑在`CPU`上，失去了`mps`后端的加速优势。

基本的安装与使用，与上游[CosyVoice](https://github.com/FunAudioLLM/CosyVoice)相同，使用方法与主要安装步骤，请参考原项目的[README.md](README_upstream.md)。

### macOS下的安装

- 安装`Homebrew`，如果你还没有安装的话。可以参考[Homebrew官网](https://brew.sh/)。
- 使用`Homebrew`安装关键依赖:`ffmpeg`:

    ```bash
    brew install ffmpeg
    ```

- Clone the repo

    ``` sh
    git clone --recursive https://github.com/lonelygo/CosyVoice
    # If you failed to clone the submodule due to network failures, please run the following command until success
    cd CosyVoice
    git submodule update --init --recursive
    ```

- Create environment and install dependencies:

    使用你喜欢的任何虚拟环境管理工具创建虚拟环境，比如使用`[uv](https://github.com/astral-sh/uv)`:

    ``` bash
    brew install uv
    # 先进入项目目录
    cd CosyVoice
    uv venv --python 3.10.0
    source .venv/bin/activate
    uv pip install -r requirements-mac.txt
    ```

### 如果你确实有使用`Docker`的需求：

    ```bash
    cd runtime/python
    docker build -f Dockerfile.macOS -t cosyvoice:v1.0 .
    ```

启动命令，与原项目一致。

## RESTful API

[`cosyvoice-api`](https://github.com/jianchang512/cosyvoice-api)项目提供了一个`RESTful API`，可以通过`HTTP`请求来合成语音。

为了方便使用，本`fork`将其也集成了进来，并做了一点点代码重构和优化，具体的使用可以参考[`cosyvoice-api`](https://github.com/jianchang512/cosyvoice-api)项目的文档。

使用非常简单：

```bash
python rest-api.py
```

增加了一些命令行参数，可以通过`--help`查看，比如：下载目录、模型目录、参考音频目录等。

`api`后端服务起来后，你就可以在第三方语音合成的应用中使用`CoSyVoice`的语音合成服务了。

## 特别说明

### `jit`开启

由于原项目仅在`cuda`后端下才开启`jit`,对于`mps`后端来说，打开`jit`也会有一丢丢的性能提升，所以对于`api`的使用默认开启了`jit`。

如果，你确实不想开启`jit`，可以修改`rest-api.py`中的相关代码:

```python
# 90~93行：
    if model_type == 'sft':
        sft_model = CosyVoice(str(local_dir), load_jit=False, fp16=False)
    elif model_type == 'tts':
        tts_model = CosyVoice2(str(local_dir), load_jit=False, fp16=False)
```

对于原项目的`webui`的使用，默认不开启`jit`,如果你要开启`jit`，可以增加启动参数：

```bash
python webui.py --load_jit
```

### 其他提示

`ttsfrd`在`macOS`下无法正常安装，所以原始项目的安装中有关这部分的安装以及模型权重下载部分可以忽略，不要陷入无意义的安装包错处理。

`权重`下载方法与上游相同，参考[README.md](README_upstream.md)。
