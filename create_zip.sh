#!/bin/bash

# Script para criar um ZIP limpo do projeto para upload no Pella
# Remove arquivos desnecessários antes de zipar

# Nome do projeto
PROJECT_NAME="Amigo-kkkkk"
ZIP_NAME="${PROJECT_NAME}.zip"

# Criar um diretório temporário
mkdir -p temp_zip/$PROJECT_NAME

# Copiar apenas os arquivos necessários
cp main.py temp_zip/$PROJECT_NAME/
cp requirements.txt temp_zip/$PROJECT_NAME/
cp .env.example temp_zip/$PROJECT_NAME/
cp README.md temp_zip/$PROJECT_NAME/
cp .gitignore temp_zip/$PROJECT_NAME/

# Criar o ZIP
cd temp_zip
zip -r ../$ZIP_NAME $PROJECT_NAME

# Voltar ao diretório original e limpar temporário
cd ..
rm -rf temp_zip

echo "✅ ZIP criado com sucesso: $ZIP_NAME"
echo "📦 Arquivo pronto para upload no Pella!"
