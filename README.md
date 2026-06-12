# Pipeline d'Ingestion de Données IoT en Temps Réel (Serverless & Big Data)

Ce dépôt contient l'infrastructure Cloud et le code applicatif pour l'implémentation d'une pipeline d'ingestion, de traitement analytique et de stockage de données IoT en mode **Serverless** sur Amazon Web Services (AWS). 

Le projet est entièrement automatisé selon l'approche **Infrastructure as Code (IaC)** à l'aide d'**AWS SAM (Serverless Application Model)** et déployé sur **AWS CloudFormation**.

## Architecture Globale du Système

L'architecture multi-niveaux mise en œuvre comprend les composants Cloud suivants :

1. **Couche d'Ingestion (Entrée API) :** Un point d'entrée unique HTTP géré par **Amazon API Gateway**, exposé globalement via une distribution **Amazon CloudFront** pour minimiser la latence et sécuriser les communications (HTTPS/TLS).
2. **Couche de Calcul (Unité de Traitement) :** Une fonction **AWS Lambda** exécutée sous l'environnement **Python 3.11** qui porte la logique métier (validation stricte du schéma JSON, calculs mathématiques et routage).
3. **Couche de Stockage Analytique (Hot Data) :** Une table **Amazon DynamoDB** NoSQL (`iot-analytics-store-kadeoul`) configurée en mode de capacité à la demande, indexée par `requestId` pour stocker immédiatement les métriques consolidées.
4. **Couche Data Lake (Cold Data / Historisation) :** Un compartiment **Amazon S3** (`iot-data-lake-kadeoul`) faisant office de zone brute (*Raw Zone*) où chaque payload initial est archivé de façon immuable avec un partitionnement temporel dynamique (`raw-zone/year=YYYY/month=MM/`).
5. **Couche de Documentation Technique :** Un bucket S3 privé (`iot-tech-doc-kadeoul`) hébergeant le site web statique de l'API (généré via Tailwind CSS), accessible de manière sécurisée uniquement via CloudFront à l'aide d'un mécanisme d'**Origin Access Control (OAC)**.

---

## Structure du Projet

.
├── src/
│   └── index.py             # Code Python 3.11 de ta fonction AWS Lambda (logique métier) [cite: 27, 
├── documentation/
│   └── index.html           # Site web de la documentation technique de l'API (Tailwind CSS) 
├── test_client.py           # Script local de simulation d'injection des capteurs IoT [cite: 44]
├── template.yaml            # Modèle AWS SAM / CloudFormation (Infrastructure as Code) [cite: 23, 117]
└── README.md                # Fichier d'accueil et documentation principale du dépôt

## Url du dépot github du projet: https://github.com/prosperadeoul-hub/examen-final-aws

## Etapes pour le déploiement du projet
### 1. se positonner dans le dossier du projet
cd examen-final-aws

### 2. Compilation de l'app
sam build

### 3. Déploiement automatisé
sam deploy --guided

### 4. Configuration de l'environnement local de test
Dupliquez le fichier d'exemple : cp .env.example .env

Ouvrez le fichier .env nouvellement créé et remplacez les valeurs génériques par les adresses réelles fournies dans les Outputs de l'étape précédente (CLOUDFRONT_INGESTION_URL et S3_DOC_URL).

### 5. Exécution des simulations d'injection IoT
Lancez le script de validation client pour vérifier le routage et le traitement analytique en direct :
python test_client.py