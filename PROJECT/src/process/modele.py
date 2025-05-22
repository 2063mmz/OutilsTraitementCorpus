import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.metrics import accuracy_score, f1_score

# Charger les données
df = pd.read_csv("comments_sr_augmented.csv") 
dataset = Dataset.from_pandas(df).train_test_split(test_size=0.2)

# Convertir le DataFrame en Dataset Hugging Face
model_name = "bert-base-multilingual-cased"

# Charger le tokenizer et le modèle
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Segmentation de l'ensemble des données pour le modèle
def tokenize(comments):
    return tokenizer(comments["text"], padding="max_length", truncation=True)
# 'batched=True' permet de traiter plusieurs exemples en parallèle
tokenized_dataset = dataset.map(tokenize, batched=True)

# Définir les paramètres d'entraînement
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)

# Définir les métriques d’évaluation
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds),
    }

#  Créer l'objet Trainer pour gérer l'entraînement et l’évaluation
trainer = Trainer(
    model=model,
    args=training_args,
    tokenizer=tokenizer,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    compute_metrics=compute_metrics,
)

# Fine-tuning du modèle
trainer.train()
