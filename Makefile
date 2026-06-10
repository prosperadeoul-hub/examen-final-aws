# Variables
TEMPLATE_PATH=infrastructure/template.yaml

.PHONY: build deploy clean validate venv test

# Valide la syntaxe du fichier template.yaml
validate:
	sam validate --template $(TEMPLATE_PATH)

# Prépare et compile le code de la Lambda
build:
	sam build --template $(TEMPLATE_PATH)

# Déploie l'infrastructure sur AWS
deploy: build
	sam deploy

# Crée l'environnement virtuel Python et installe les dépendances requises
venv:
	python -m venv venv
	.\venv\Scripts\pip install requests python-dotenv boto3

# Lance le script de test client avec l'environnement virtuel
test:
	.\venv\Scripts\python test_client.py

# Nettoie les fichiers temporaires de build locaux
clean:
	if exist .aws-sam rmdir /s /q .aws-sam
	@echo "Dossier de build .aws-sam nettoye."