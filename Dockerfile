FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-devel

RUN apt-get update && \
    apt-get install -y git libgl1-mesa-dev libglib2.0-0

WORKDIR /app
COPY . /app
ENV TORCH_CUDA_ARCH_LIST="7.0"
RUN pip install -r requirements.txt

# a modified gaussian splatting (+ depth, alpha rendering)
RUN git clone --recursive https://github.com/ashawkey/diff-gaussian-rasterization
RUN pip install ./diff-gaussian-rasterization

# simple-knn
RUN pip install ./app/dreamgaussian/src/core/simple-knn 
# nvdiffrast
RUN pip install git+https://github.com/NVlabs/nvdiffrast/

# kiuikit
RUN pip install git+https://github.com/ashawkey/kiuikit

# To use MVdream, also install:
RUN pip install git+https://github.com/bytedance/MVDream

# To use ImageDream, also install:
RUN pip install git+https://github.com/bytedance/ImageDream/#subdirectory=extern/ImageDream

RUN pip install .