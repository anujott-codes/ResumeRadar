FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && curl -Lsf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"
ENV HF_HOME="/app/.cache/huggingface"

COPY requirements.txt .
RUN uv pip install --system --no-cache \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

RUN python -m spacy download en_core_web_sm

RUN python -c "\
from sentence_transformers import SentenceTransformer; \
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification; \
SentenceTransformer('BAAI/bge-small-en-v1.5'); \
AutoTokenizer.from_pretrained('feliponi/hirly-ner-multi'); \
AutoModel.from_pretrained('feliponi/hirly-ner-multi'); \
AutoTokenizer.from_pretrained('anujot/resumeradar-skill-classifier'); \
AutoModelForSequenceClassification.from_pretrained('anujot/resumeradar-skill-classifier'); \
print('All models cached.')"

COPY ./src ./src

EXPOSE 8000

CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]