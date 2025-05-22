import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Charger les données augmentées et les encoder
df = pd.read_csv("commits_sr_augmented.csv")
dataset = Dataset.from_pandas(df).train_test_split(test_size=0.2)

model_name = "bert-base-multilingual-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained("./results/checkpoint-12")  # 用你训练后的模型

# Segmentation de l'ensemble des données pour le modèle
def tokenize(comments):
    return tokenizer(comments["text"], padding="max_length", truncation=True)
tokenized_dataset = dataset.map(tokenize, batched=True)

# Faire les prédictions
from transformers import Trainer, TrainingArguments

args = TrainingArguments(output_dir="./eval_tmp", per_device_eval_batch_size=8)
trainer = Trainer(model=model, tokenizer=tokenizer, args=args)

predictions = trainer.predict(tokenized_dataset["test"])
y_pred = np.argmax(predictions.predictions, axis=1)
y_true = predictions.label_ids

# Afficher les métriques d’évaluation
print("Classification Report :")
print(classification_report(y_true, y_pred, digits=4))

print("\nMatrice de confusion :")
print(confusion_matrix(y_true, y_pred))
