import requests as req
bot_token = '8013793190:AAFmUBLpgT6MYXfwLzgVA1p0TxXxpKOgui4'

def send_task_tg_users(task):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    chat_ids = task.performers.values_list('tg_id', flat=True)
    message = (
        f"🔰 #topshiriq №{task.id}\n\n"
        f"⚜️ {task.author.full_name}\n\n"
        f"🧾 {task.title}\n\n"
        f"📃 {task.description}\n\n"
        f"📆 {task.deadline.strftime('%d.%m.%Y %H:%M')}\n\n"
    )
    for chat_id in chat_ids:
        if chat_id:  # None yoki bo'sh bo'lmaganini tekshiradi
            payload = {
                'chat_id': chat_id,
                'text': message
            }
            try:
                res = req.get(url, params=payload, timeout=5)
                if res.status_code != 200:
                    print(f"⚠️ Xatolik yuborishda (chat_id={chat_id}): {res.text}")
            except Exception as e:
                print(f"❌ Ulanishda xatolik: {e}")