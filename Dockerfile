FROM python:3.10

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

COPY requirements.txt .

COPY model/video_capture_yolo.pt /app/model/video_capture_yolo.pt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/templates /app/templates

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
