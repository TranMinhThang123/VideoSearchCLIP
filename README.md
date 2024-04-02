## Pipeline
<p align="center"><img src="figs/pipeline.jpg" width="800"/></p>

## Demo
[![YouTube](https://badges.aleen42.com/src/youtube.svg)](https://youtu.be/fULnllhIrqY)

## Hướng dẫn sử dụng Video Search
`Tạo sẵn env python`

### Bước 1: Clone Repository
```bash
git clone https://github.com/nlnamanh/Video_Search.git
```

### Bước 2: Download Keyframes và Dict
Download hai tệp Keyframes và Dict từ các đường dẫn sau:
- [Keyframes](https://drive.google.com/file/d/1-9Mn8ZjTNzKleQ4uMUYoGwXkXjep-CKP/view)
- [Dict](https://drive.google.com/file/d/1eJWNhsrcexLhZJuufuvODxndYzM_kvBm/view)

Sau đó, di chuyển hai tệp này vào thư mục `Video_Search`.

### Bước 3: Cài đặt các yêu cầu
```bash
pip install git+https://github.com/openai/CLIP.git
pip install -r requirements.txt
```

### Bước 4: Chạy ứng dụng
```bash
streamlit run main.py
```