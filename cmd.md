docker pull manticoresearch/manticore

docker run --name manticore -p 9306:9306 -p 9308:9308 -d manticoresearch/manticore

docker run --name manticore -v $(pwd)/data:/var/lib/manticore -p 127.0.0.1:9306:9306 -p 127.0.0.1:9308:9308 -d manticoresearch/manticore

mysql -P9306



docker pull opensearchproject/opensearch:3

docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=S202512sss" opensearchproject/opensearch:3

docker compose up -d

docker compose down
