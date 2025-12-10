docker pull opensearchproject/opensearch:3

docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=S202512sss" opensearchproject/opensearch:3

docker compose up -d

docker compose down


http://127.0.0.1:5601/
admin
S202512sss

DBeaver opensearch
jdbc:opensearch://https://127.0.0.1:9200?auth=basic&user=admin&password=S202512sss&trustSelfSigned=true