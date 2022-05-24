# Buildar as imagens dos containers do dumper e do uploader para a aws:
docker build -t client ./app/dumper/
docker build -t s3-sender ./app/s3-sender/

# Iniciar todos os containers:
docker-compose up -d

# pendente - crontab:
- fazer o crontab rodar de forma consistente no docker
- substituir o teste.sh pelo job do python (send-to-s3.py) para executar de 6h em 6h

# pendente - spark jobs:
- pegar o dump de maior data e numero_nome_arquivo
- carregar as tabelas necessarias do dump.sql num dataframe

# subir no gitlab/github 
- fazer um README.md de forma apresentável