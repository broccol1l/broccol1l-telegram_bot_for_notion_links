import re

async def is_valid_url(url: str) -> bool:
    """
    Validate if the input string is a valid URL.
    """
    pattern = r'^(https?|ftp):\/\/(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\/[^\s]*)?$'
    return re.match(pattern, url) is not None

# Асинхронная функция для извлечения источника из URL
async def get_source_from_url(url: str) -> str:
    """
    Извлекает источник из URL, например: 
    https://instagram.com -> Instagram
    https://facebook.com -> Facebook
    """
    # Регулярное выражение для поиска домена
    domain_pattern = r"https?://(?:www\.)?([^/]+)"

    match = re.search(domain_pattern, url)
    if match:
        domain = match.group(1).lower()

        # Соответствие доменов с названиями источников
        sources = {
            "instagram.com": "Instagram",
            "facebook.com": "Facebook",
            "twitter.com": "Twitter",
            "youtube.com": "YouTube",
            "linkedin.com": "LinkedIn",
            "t.me": "Telegram",
            "reddit.com": "Reddit",
            "vk.com": "VKontakte",
            # Добавьте другие домены по мере необходимости
        }

        # Возвращаем название источника, если оно найдено, иначе возвращаем сам домен
        return sources.get(domain, domain.capitalize())

    return "Неизвестный источник"  # Если не удалось извлечь домен