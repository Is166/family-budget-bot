import json
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import os

TOKEN = os.environ["BOT_TOKEN"]
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = update.message.from_user.first_name
    date = datetime.now().strftime("%Y-%m-%d")

    if text.startswith('+') or text.startswith('-'):
        try:
            parts = text[1:].strip().split(' ', 1)
            amount = float(parts[0])
            category = parts[1] if len(parts) > 1 else "Без категории"
            record = {
                "date": date,
                "type": "income" if text.startswith('+') else "expense",
                "amount": amount,
                "category": category,
                "user": user
            }
            data = load_data()
            data.append(record)
            save_data(data)
            await update.message.reply_text(f"Записано: {text}")
        except Exception as e:
            await update.message.reply_text("Ошибка в формате. Пример: +1000 зарплата")
    else:
        return

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    income = sum(item["amount"] for item in data if item["type"] == "income")
    expense = sum(item["amount"] for item in data if item["type"] == "expense")
    balance = income - expense
    await update.message.reply_text(
        f"📊 Статистика:\nДоход: {income:.2f} CHF\nРасход: {expense:.2f} CHF\nБаланс: {balance:.2f} CHF"
    )

async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    expense_by_cat = {}
    for item in data:
        if item["type"] == "expense":
            cat = item["category"]
            expense_by_cat[cat] = expense_by_cat.get(cat, 0) + item["amount"]
    if not expense_by_cat:
        await update.message.reply_text("Пока нет расходов для анализа.")
        return
    biggest = max(expense_by_cat, key=expense_by_cat.get)
    await update.message.reply_text(f"💡 Совет: ты тра_
