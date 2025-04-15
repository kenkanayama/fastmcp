#!/bin/bash

# 既存のコンテナがある場合に停止・削除
docker stop fastmcp-server 2>/dev/null || true
docker rm fastmcp-server 2>/dev/null || true

# イメージをビルド
docker build --force-rm=true -t fastmcp-server  . --no-cache=true

# コンテナを起動
docker run -d -it --name fastmcp-server -p 8080:8080 -v $(pwd):/usr/src/app fastmcp-server
