from datetime import datetime
import boto3
import os

def main():
    path_hoje = datetime.today().strftime('%Y-%m-%d')

    with open('../input/credentials.txt', 'r') as f:
        KEY_ID = f.readline().strip()
        ACCESS_KEY = f.readline().strip()
        BUCKET_NAME = f.readline().strip()
    
    s3 = boto3.client('s3', region_name='us-east-1',
                  aws_access_key_id=KEY_ID,
                  aws_secret_access_key=ACCESS_KEY)
    

    # Checando se o bucket BUCKET_NAME existe no s3; criando se não existir
    lista_nome_buckets = []

    for bucket in s3.list_buckets()['Buckets']:
        lista_nome_buckets.append(bucket['Name'])

    if BUCKET_NAME not in lista_nome_buckets:
        s3.create_bucket(Bucket=BUCKET_NAME)
     

    # Incrementa o sufixo com base em quantos dumps já existem na pasta de hoje
    obj_responses = s3.list_objects(Bucket=BUCKET_NAME)
    cont_dumps_hoje = 0
    try:
        for content in obj_responses.get('Contents'):
            if path_hoje in content.get('Key'):
                cont_dumps_hoje += 1
    except:
        pass

    s3.upload_file(
        Filename='/dumps/dump.sql',
        Bucket=BUCKET_NAME,
        Key=f'{path_hoje}/datadump{cont_dumps_hoje + 1}.sql'
        )
    
    os.remove('/dumps/dump.sql')

if __name__ == '__main__':
    if os.path.exists('/dumps/dump.sql'):
        main()

    else:
        print("Não há dump a ser enviado")