docker pull manticoresearch/manticore

docker run --name manticore -p 9306:9306 -p 9308:9308 -d manticoresearch/manticore

docker run --name manticore -v $(pwd)/data:/var/lib/manticore -p 127.0.0.1:9306:9306 -p 127.0.0.1:9308:9308 -d manticoresearch/manticore

mysql -P9306


