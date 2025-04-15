FROM python:3.13-slim
ENV APP_PATH=/usr/src/app
WORKDIR $APP_PATH

COPY requirements.txt ./
COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# コンテナが終了しないようにする
CMD ["sh", "-c", "while true; do sleep 3600; done"]
