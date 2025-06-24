# Dockerfile
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Gradio
EXPOSE 8501

# Default para CLI
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]