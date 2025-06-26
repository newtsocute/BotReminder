from .db import get_all_users


def generate_mentions() -> str:
    users = get_all_users()
    if not users:
        return "Нет пользователей для упоминания."

    mentions = []
    for user_id, full_name in users:
        mention = f"<a href='tg://user?id={user_id}'>{full_name}</a>"
        mentions.append(mention)

    return " ".join(mentions)
