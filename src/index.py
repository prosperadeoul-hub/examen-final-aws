import json
import os
import boto3
from decimal import Decimal
from datetime import datetime

# Initialisation des clients AWS
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE')
S3_BUCKET = os.environ.get('S3_BUCKET')

def handler(event, context):
    try:
        # 1. Extraire et analyser (parser) le corps JSON de la requête
        body = json.loads(event.get('body', '{}'))
        
        # Validation basique du payload
        if 'measures' not in body or not isinstance(body['measures'], list):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Payload invalide", "details": "Le champ 'measures' est manquant ou invalide."})
            }
        
        # Validation de la structure interne de chaque mesure
        for m in body['measures']:
            if 'temperature' not in m or 'sensor_id' not in m or 'status' not in m:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Payload corrompu", "details": "Champs obligatoires (sensor_id, temperature, status) manquants."})
                }

        # 2. Stratégie de partitionnement temporel dans la clé de stockage S3
        request_id = context.aws_request_id
        now = datetime.utcnow()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        
        s3_key = f"raw-zone/year={year}/month={month}/{request_id}.json"
        
        # Sauvegarde du JSON brut original dans le Data Lake S3
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=json.dumps(body)
        )

        # 3. Calculer à la volée les métriques (moyenne et anomalies)
        measures = body['measures']
        total_records = len(measures)
        
        somme_temperatures = sum(float(m['temperature']) for m in measures)
        avg_temperature = somme_temperatures / total_records if total_records > 0 else 0
        
        error_count = sum(1 for m in measures if m.get('status') == 'ERROR')

        # 4. Enregistrer un rapport d'exécution condensé dans la table DynamoDB
        table = dynamodb.Table(DYNAMODB_TABLE)
        timestamp_iso = now.isoformat() + 'Z'
        
        table.put_item(
            Item={
                'requestId': request_id,
                'timestamp': timestamp_iso,
                's3_path': f"s3://{S3_BUCKET}/{s3_key}",
                'average_temperature': Decimal(str(round(avg_temperature, 2))),
                'anomaly_count': error_count
            }
        )
        
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Donnees IoT traitees et stockees avec succes", 
                "requestId": request_id,
                "metrics": {
                    "avg_temp": round(avg_temperature, 2),
                    "anomalies": error_count
                }
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Payload invalide ou corrompu", "details": str(e)})
        }