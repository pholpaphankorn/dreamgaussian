FROM pytorch/pytorch:2.1.2-cuda11.8-cudnn8-runtime

RUN pip install -r requirements.txt

# a modified gaussian splatting (+ depth, alpha rendering)
RUN git clone --recursive https://github.com/ashawkey/diff-gaussian-rasterization
RUN pip install ./diff-gaussian-rasterization

# simple-knn
RUN pip install ./simple-knn

# nvdiffrast
RUN pip install git+https://github.com/NVlabs/nvdiffrast/

# kiuikit
RUN pip install git+https://github.com/ashawkey/kiuikit

# To use MVdream, also install:
RUN pip install git+https://github.com/bytedance/MVDream

# To use ImageDream, also install:
RUN pip install git+https://github.com/bytedance/ImageDream/#subdirectory=extern/ImageDream