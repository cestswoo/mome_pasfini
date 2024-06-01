from transformers import BertTokenizer, BertForSequenceClassification
import os

model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'
model_dir = "./models"
os.makedirs(model_dir, exist_ok=True)

# 토크나이저와 모델을 다운로드하여 로컬 디렉토리에 저장
tokenizer = BertTokenizer.from_pretrained(model_name, cache_dir=model_dir, use_fast=True)
model = BertForSequenceClassification.from_pretrained(model_name, cache_dir=model_dir)