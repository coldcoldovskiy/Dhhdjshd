import os
import random
import requests
import json
import re
import asyncio
import aiohttp
import time
import urllib.parse
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any
import subprocess
import platform
import sys

# Ссылка на ваш файл с разрешенными HWID (Raw версия с GitHub Gist)
AUTHORIZED_HWIDS_URL = "https://raw.githubusercontent.com/coldcoldovskiy/Nbbbbbn/refs/heads/main/Hshsha"



# --- ФУНКЦИИ ЗАЩИТЫ ---
def get_hwid():
    """Безопасный метод получения HWID для Termux."""
    try:
        # uname -a выдает информацию о ядре (версия, дата сборки и т.д.)
        # Это уникально для устройства и прошивки
        cmd = "uname -a"
        result = subprocess.check_output(cmd, shell=True).decode().strip()
        
        # Хешируем результат, чтобы получить чистый HWID (например, A1B2...)
        import hashlib
        hwid = hashlib.sha256(result.encode()).hexdigest()[:16].upper()
        
        print(f"DEBUG: Ваш HWID: {hwid}") # Скопируйте это
        return hwid
    except Exception as e:
        print(f"DEBUG: Критическая ошибка: {e}")
        return "ERROR_FAIL"


def check_access():
    """Проверка HWID и пароля с очисткой данных."""
    local_hwid = get_hwid()
    
    try:
        response = requests.get(AUTHORIZED_HWIDS_URL, timeout=10)
        if response.status_code == 200:
            user_password = input(f"{COLOR_CODE['CYAN']}Введите пароль доступа: {COLOR_CODE['RESET']}").strip()
            
            # Читаем построчно
            lines = response.text.splitlines()
            
            for line in lines:
                if ':' in line:
                    # Очищаем каждую часть от пробелов и управляющих символов
                    parts = line.split(':')
                    file_hwid = parts[0].strip()
                    file_pass = parts[1].strip()
                    
                    # Сравниваем
                    if local_hwid == file_hwid and user_password == file_pass:
                        print(f"{COLOR_CODE['GREEN']}Авторизация успешна!{COLOR_CODE['RESET']}")
                        return True
            
            print(f"{COLOR_CODE['RED']}Ошибка: Неверный пароль или HWID ({local_hwid}) не найден!{COLOR_CODE['RESET']}")
            return False
        else:
            print(f"{COLOR_CODE['RED']}Ошибка подключения к серверу (Код {response.status_code}){COLOR_CODE['RESET']}")
            return False
    except Exception as e:
        print(f"DEBUG: Ошибка в функции check_access: {e}")
        return False





COLOR_CODE = {
    "RESET": "\033[0m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[93m",
    "CYAN": "\033[36m",
    "BOLD": "\033[01m",
    "PINK": "\033[95m",
    "URL_L": "\033[36m",
    "LI_G": "\033[92m",
    "DARK": "\033[90m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[95m",
}

# ============== КОНФИГУРАЦИЯ API ==============
DEPSEARCH_BASE_URL = "https://api.depsearch.sbs/"
DEPSEARCH_TOKEN = "fWd0HTsq0Ye9nwfxZyqIPGxYmD7mB8eT"

BIGBASE_URL = "https://bigbase.top/api"
BIGBASE_TOKEN = "BOqMzQ63vPTPKs7gfUDrJru62SX2JaqC"


OK_LOGIN_URL = 'https://www.ok.ru/dk?st.cmd=anonymMain&st.accRecovery=on&st.error=errors.password.wrong'
OK_RECOVER_URL = 'https://www.ok.ru/dk?st.cmd=anonymRecoveryAfterFailedLogin&st._aid=LeftColumn_Login_ForgotPassword'
REFIND_API_TOKEN = '62ee6897-79a5-4fb9-b166-4cc6672eb8dd'
VERIPHONE_API_KEY = '1A85D514E9B04073AC51FA394182728A'
VK_TOKEN = '0af157510af157510af15751aa0a89e69600af10af157516a0bc15996e74fe2b440998c'
TELEGRAM_API_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI3Nzc3Njk4MzAyIiwianRpIjoiYWVhMDAwY2MtMzM3Zi00MTZhLWIyOTItNWY3YWE3OTU5NzY5IiwiZXhwIjoxNzgxNzg1NDAzfQ.lDngeYk_Dg-v3VeKkxp-yulvvEdOQxgLC0QMe6c779PdC5IjAclLgkPrgHDgExRuBMsde3tLRZQlZgyPYfcQxwXCN0hpyJfG0Ne8m0k25laY4vJaFCyz0lNUcIoDMRSF6HWgoONCXZtV5Uc0-HtczSL4wjtlGRsAyIzVYlENV-c'
TOKEN = ""
BASE_URL = "https://api.vk.com/method/"
ACCESS_TOKEN = VK_TOKEN
API_VERSION = "5.131"
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
]

class OSINTTool:
    def __init__(self):
        pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""{COLOR_CODE["RED"]}
            _     _ _____  ______ _____  
           | |   | |  __ \|  ____|  __ \ 
   ___ ___ | | __| | |__) | |__  | |  | |
  / __/ _ \| |/ _` |  _  /|  __| | |  | |
 | (_| (_) | | (_| | | \ \| |____| |__| |
  \___\___/|_|\__,_|_|  \_\______|_____/ 
                                               
                                                                                                                  
{COLOR_CODE["RESET"]}"""
    print(banner)

def print_menu():
    menu = f"""
{COLOR_CODE["RED"]}[ 1 ] поиск по номеру
[ 2 ] ВК осинт
[ 3 ] Поиск по IP-адресу
[ 4 ] Поиск по email
[ 5 ] Поиск по адресу
[ 6 ] Поиск по MAC
[ 7 ] Поиск по ФИО
[ 8 ] Поиск по VIN
[ 9 ] поиск по СНИЛС
[ 10 ] Поиск по ИНН
[ 11 ] Поиск по токену бота
{COLOR_CODE["RED"]}[ 0 ] Выход{COLOR_CODE["RESET"]}
"""
    print(menu)

def get_address_by_coordinates(latitude, longitude):
    try:
        response = requests.get(
            f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json",
            headers={"User-Agent": random.choice(USER_AGENTS)},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("display_name", "Адрес не найден")
    except Exception:
        return "Не удалось получить адрес"

def translate_address(address):
    translations = {
        "road": "Улица",
        "house_number": "Номер дома",
        "town": "Город",
        "city": "Город",
        "village": "Деревня",
        "county": "Район",
        "state": "Область",
        "country": "Страна",
        "postcode": "Почтовый индекс"
    }
    result = {}
    for key, value in address.items():
        if key in translations:
            result[translations[key]] = value
        else:
            result[key] = value
    return result

def identify_type(val):
    val = val.strip()
    digits_only = re.sub(r"\D", "", val)
    if re.match(r"^(\+?7|8|9).*", val) and 10 <= len(digits_only) <= 11:
        if digits_only.startswith("8"): 
            digits_only = "7" + digits_only[1:]
        elif digits_only.startswith("9") and len(digits_only) == 10:
            digits_only = "7" + digits_only
        return digits_only, "ТЕЛЕФОН"
    
    snils_raw = re.sub(r"[\s-]", "", val)
    if len(snils_raw) == 11 and snils_raw.isdigit():
        return snils_raw, "СНИЛС"
        
    if len(snils_raw) in (10, 12) and snils_raw.isdigit():
        return snils_raw, "ИНН"
        
    if len(val) == 17 and re.match(r"^[A-HJ-NPR-Z0-9]{17}$", val.upper()):
        return val.upper(), "VIN"
        
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", val):
        return val, "EMAIL"
        
    clean_plate = val.replace(" ", "").upper()
    if re.match(r"^[АВЕКМНОРСТУХABEKMHOPCTYX]\d{3}[АВЕКМНОРСТУХABEKMHOPCTYX]{2}\d{2,3}$", clean_plate):
        return clean_plate, "АВТО-НОМЕР"
        
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", val):
        return val, "IP-АДРЕС"
        
    name_parts = val.split()
    if len(name_parts) >= 2 and all(re.match(r"^[а-яА-Яa-zA-Z\-]+$", p) for p in name_parts):
        return val, "ФИО / ИМЯ"
        
    return val, "ОБЩИЙ ПОИСК / АДРЕС"

# ================= ИНТЕГРАЦИЯ РАБОЧИХ ПАРСЕРОВ ИЗ 2.py =================

async def bigbase_check(user_input):
    print(f"\n{COLOR_CODE['YELLOW']}=== ПРОВЕРКА BIGBASE ==={COLOR_CODE['RESET']}")
    url = f"{BIGBASE_URL}/search"
    headers = {
        "Authorization": BIGBASE_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {"search": user_input, "page": 1}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=25) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    results = []
                    
                    def extract(obj, prefix=""):
                        if isinstance(obj, dict):
                            for k, v in obj.items():
                                if k not in ["error", "success"] and v:
                                    if isinstance(v, (dict, list)):
                                        extract(v, f"{prefix}{k} ")
                                    else:
                                        results.append({"field": f"{prefix}{k}".strip(), "value": str(v)})
                        elif isinstance(obj, list):
                            for item in obj: extract(item, prefix)
                            
                    extract(data)
                    
                    if results:
                        print(f"{COLOR_CODE['GREEN']}╠═Найдено данных (BigBase): {len(results)}{COLOR_CODE['RESET']}")
                        for item in results[:30]:
                            field_name = item['field'].replace("_", " ").capitalize()
                            print(f"{COLOR_CODE['GREEN']}║   • {field_name}: {item['value']}{COLOR_CODE['RESET']}")
                    else:
                        print(f"{COLOR_CODE['RED']}╠═Данные не найдены в BigBase{COLOR_CODE['RESET']}")
                else:
                    print(f"{COLOR_CODE['RED']}╠═Ошибка сервера BigBase: {resp.status}{COLOR_CODE['RESET']}")
    except Exception as e:
        print(f"{COLOR_CODE['RED']}╠═Ошибка запроса BigBase: {e}{COLOR_CODE['RESET']}")



def identify_type(val):
    val = val.strip()
    digits_only = re.sub(r"\D", "", val)
    if re.match(r"^(\+?7|8|9).*", val) and 10 <= len(digits_only) <= 11:
        if digits_only.startswith("8"): 
            digits_only = "7" + digits_only[1:]
        elif digits_only.startswith("9") and len(digits_only) == 10:
            digits_only = "7" + digits_only
        return digits_only, "ТЕЛЕФОН"
    
    snils_raw = re.sub(r"[\s-]", "", val)
    if len(snils_raw) == 11 and snils_raw.isdigit():
        return snils_raw, "СНИЛС"
        
    if len(snils_raw) in (10, 12) and snils_raw.isdigit():
        return snils_raw, "ИНН"
        
    if len(val) == 17 and re.match(r"^[A-HJ-NPR-Z0-9]{17}$", val.upper()):
        return val.upper(), "VIN"
        
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", val):
        return val, "EMAIL"
        
    clean_plate = val.replace(" ", "").upper()
    if re.match(r"^[АВЕКМНОРСТУХABEKMHOPCTYX]\d{3}[АВЕКМНОРСТУХABEKMHOPCTYX]{2}\d{2,3}$", clean_plate):
        return clean_plate, "АВТО-НОМЕР"
        
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", val):
        return val, "IP-АДРЕС"
        
    name_parts = val.split()
    if len(name_parts) >= 2 and all(re.match(r"^[а-яА-Яa-zA-Z\-]+$", p) for p in name_parts):
        return val, "ФИО / ИМЯ"
        
    return val, "ОБЩИЙ ПОИСК / АДРЕС"

async def depsearch_check(user_input):
    print(f"\n{COLOR_CODE['YELLOW']}=== ПРОВЕРКА DEPSEARCH ==={COLOR_CODE['RESET']}")
    query, q_type = identify_type(user_input)
    encoded_query = urllib.parse.quote(query)
    url = f"{DEPSEARCH_BASE_URL}quest={encoded_query}&token={DEPSEARCH_TOKEN}"
    
    print(f"{COLOR_CODE['CYAN']}🔎 Анализ: {query} | Тип: {q_type}{COLOR_CODE['RESET']}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=25) as resp:
                if resp.status == 401:
                    print(f"{COLOR_CODE['RED']}╠═Ошибка 401: Токен не принят.{COLOR_CODE['RESET']}")
                    return
                if resp.status != 200:
                    print(f"{COLOR_CODE['RED']}╠═Ошибка сервера: {resp.status}{COLOR_CODE['RESET']}")
                    return
                
                text = await resp.text()
                if not text.strip():
                    print(f"{COLOR_CODE['RED']}╠═Пустой ответ от сервера.{COLOR_CODE['RESET']}")
                    return
                
                data = json.loads(text)
                
                results = []
                if isinstance(data, dict):
                    results = data.get('Results', [data])
                elif isinstance(data, list):
                    results = data

                if not results or (isinstance(results, list) and len(results) == 0):
                    print(f"{COLOR_CODE['RED']}╠═Данные не найдены{COLOR_CODE['RESET']}")
                    return

                print(f"{COLOR_CODE['GREEN']}╠═Найдено записей: {len(results)}{COLOR_CODE['RESET']}")
                
                # Расширенный словарь переводов полей
                labels = {
                    "phone": "Телефон",
                    "email": "Email",
                    "snils": "СНИЛС",
                    "inn": "ИНН",
                    "name": "ФИО",
                    "fio": "ФИО",
                    "full_name": "Полное имя",
                    "birthday": "Дата рождения",
                    "dob": "Дата рождения",
                    "bdate": "Дата рождения",
                    "last_name": "Фамилия",
                    "first_name": "Имя",
                    "middle_name": "Отчество",
                    "patronymic": "Отчество",
                    "passport": "Паспорт",
                    "doc_num": "Номер документа",
                    "citizenship": "Гражданство",
                    "event": "Событие",
                    "checkpoint": "Пункт пропуска",
                    "data": "База данных",
                    "sources": "Источник",
                    "source": "Источник",
                    "event_date1": "Дата/Время события",
                    "address": "Адрес",
                    "city": "Город",
                    "region": "Регион",
                    "country": "Страна",
                    "ip": "IP-адрес",
                    "password": "Пароль",
                    "pass": "Пароль",
                    "login": "Логин",
                    "username": "Имя пользователя",
                    "vk_id": "VK ID",
                    "telegram_id": "Telegram ID",
                    "vin": "VIN",
                    "car_plate": "Номер авто",
                    "plate": "Номер авто",
                    "car_model": "Марка/Модель авто",
                    "model": "Модель",
                    "job": "Место работы",
                    "company": "Компания",
                    "position": "Должность",
                    "gender": "Пол",
                    "age": "Возраст",
                    "phone_operator": "Мобильный оператор",
                    "mac": "MAC-адрес"
                }

                for i, item in enumerate(results, 1):
                    print(f"\n{COLOR_CODE['GREEN']}╠═ Запись #{i}{COLOR_CODE['RESET']}")
                    for key, value in item.items():
                        if value:
                            label = labels.get(key.lower(), key.replace("_", " ").capitalize())
                            print(f"{COLOR_CODE['GREEN']}║   • {label}: {value}{COLOR_CODE['RESET']}")

    except Exception as e:
        print(f"{COLOR_CODE['RED']}╠═Ошибка DepSearch: {e}{COLOR_CODE['RESET']}")

# --- END DEPSEARCH INTEGRATION ---

async def fetch_data(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return (await response.text()).split("\n")
    except Exception:
        return []

async def phone_search_part(phone):
    print(f"{COLOR_CODE['YELLOW']}[ - ] Поиск по номеру...{COLOR_CODE['RESET']}")
    
    path = f"{phone[:2]}/{phone[2:4]}/{phone[4:6]}/{phone[6:8]}.csv"
    url = f"https://data.intelx.io/saverudata/db2/dbpn/{path}"
    async with aiohttp.ClientSession() as session:
        try:
            lines = await fetch_data(session, url)
            if not lines:
                print(f"{COLOR_CODE['RED']}[ + ] Данные не найдены в Intelx{COLOR_CODE['RESET']}")
            else:
                headers = [h.strip().strip('"') for h in lines[0].split(",")]
                query_lower = phone.lower()
                found_data = defaultdict(set)
                for line in lines[1:]:
                    values = [v.strip().strip('"') for v in line.split(",")]
                    if any(query_lower in v.lower() for v in values):
                        for i, value in enumerate(values):
                            if value:
                                found_data[headers[i]].add(value)
                if found_data:
                    print(f"{COLOR_CODE['GREEN']}[ + ] Найденные данные в Intelx:{COLOR_CODE['RESET']}")
                    for key, values in found_data.items():
                        for value in values:
                            print(f"{COLOR_CODE['GREEN']}[ + ] {key}: {value}{COLOR_CODE['RESET']}")
                else:
                    print(f"{COLOR_CODE['RED']}[ + ] Данные не найдены в Intelx{COLOR_CODE['RESET']}")
        except Exception as e:
            print(f"{COLOR_CODE['RED']}[ + ] Ошибка Intelx: {e}{COLOR_CODE['RESET']}")

async def run_async_checks(query):
    # Универсальная функция запуска всех трёх API последовательно
    await depsearch_check(query)
    await bigbase_check(query)

# ================= ОРИГИНАЛЬНЫЕ ФУНКЦИИ ИЗ GAZ111.PY =================

async def fetch_data(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return (await response.text()).split("\n")
    except Exception:
        return []

async def phone_search_part(phone):
    print(f"{COLOR_CODE['YELLOW']}[ - ] Поиск по номеру...{COLOR_CODE['RESET']}")
    
    path = f"{phone[:2]}/{phone[2:4]}/{phone[4:6]}/{phone[6:8]}.csv"
    url = f"https://data.intelx.io/saverudata/db2/dbpn/{path}"
    async with aiohttp.ClientSession() as session:
        try:
            lines = await fetch_data(session, url)
            if not lines:
                print(f"{COLOR_CODE['RED']}[ + ] Данные не найдены в Intelx{COLOR_CODE['RESET']}")
            else:
                headers = [h.strip().strip('"') for h in lines[0].split(",")]
                query_lower = phone.lower()
                found_data = defaultdict(set)
                for line in lines[1:]:
                    values = [v.strip().strip('"') for v in line.split(",")]
                    if any(query_lower in v.lower() for v in values):
                        for i, value in enumerate(values):
                            if value:
                                found_data[headers[i]].add(value)
                if found_data:
                    print(f"{COLOR_CODE['GREEN']}[ + ] Найденные данные в Intelx:{COLOR_CODE['RESET']}")
                    for key, values in found_data.items():
                        for value in values:
                            print(f"{COLOR_CODE['GREEN']}[ + ] {key}: {value}{COLOR_CODE['RESET']}")
                else:
                    print(f"{COLOR_CODE['RED']}[ + ] Данные не найдены в Intelx{COLOR_CODE['RESET']}")
        except Exception as e:
            print(f"{COLOR_CODE['RED']}[ + ] Ошибка Intelx: {e}{COLOR_CODE['RESET']}")

async def search_vk(phone: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://find.vk.com/phone/{phone}",
                headers={"User-Agent": random.choice(USER_AGENTS)},
                timeout=10
            ) as response:
                if response.status == 200:
                    print(f"{COLOR_CODE['GREEN']}╠═Аккаунт найден в VK{COLOR_CODE['RESET']}")
                    print(f"{COLOR_CODE['GREEN']}╠═Ссылка на профиль: https://vk.com/phone/{phone}{COLOR_CODE['RESET']}")
                else:
                    print(f"{COLOR_CODE['RED']}╠═Аккаунт не найден в VK{COLOR_CODE['RESET']}")
    except Exception as e:
        print(f"{COLOR_CODE['RED']}╠═Ошибка VK: {str(e)}{COLOR_CODE['RESET']}")

async def check_geolocation(phone):
    print(f"\n{COLOR_CODE['YELLOW']}=== ГЕОЛОКАЦИЯ НОМЕРА ==={COLOR_CODE['RESET']}")
    try:
        response = requests.get(
            f"https://htmlweb.ru/geo/api.php?json&telcod={phone}",
            headers={"User-Agent": random.choice(USER_AGENTS)},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        TELCOD = data.get("country", {}).get("telcod", "Неизвестно")
        COUNTRY = data.get("country", {}).get("fullname", "Неизвестно")
        OKRUG = data.get("okrug", "Неизвестно")
        OBLAST = data.get("region", {}).get("name", "Неизвестно")
        CITY = data.get("0", {}).get("name", "Неизвестно")
        latitude = data.get("0", {}).get("latitude", "Неизвестно")
        longitude = data.get("0", {}).get("longitude", "Неизвестно")
        TIMEZONE = data.get("0", {}).get("time_zone", data.get("time_zone", "Неизвестно"))
        OPER = data.get("0", {}).get("oper", "Неизвестно")
        
        print(f"{COLOR_CODE['GREEN']}╠═Телефонный код: +{TELCOD}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}╠═Страна: {COUNTRY}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}╠═Округ: {OKRUG}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}╠═Регион: {OBLAST}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}╠═Город: {CITY}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}╠═Широта: {latitude}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}╠═Долгота: {longitude}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}╠═Часовой пояс: +{TIMEZONE} UTC{COLOR_CODE['RESET']}")
        
        if latitude != "Неизвестно" and longitude != "Неизвестно":
            address = get_address_by_coordinates(latitude, longitude)
            if isinstance(address, dict):
                translated_address = translate_address(address)
                print(f"{COLOR_CODE['GREEN']}╠═Адрес:{COLOR_CODE['RESET']}")
                for key, value in translated_address.items():
                    print(f"{COLOR_CODE['GREEN']}║   • {key}: {value}{COLOR_CODE['RESET']}")
            else:
                print(f"{COLOR_CODE['GREEN']}╠═Адрес: {address}{COLOR_CODE['RESET']}")
    except Exception as e:
        print(f"{COLOR_CODE['RED']}Ошибка при запросе к HTMLWEB: {e}{COLOR_CODE['RESET']}")

async def combined_phone_search():
    phone = input(f"{COLOR_CODE['CYAN']}Введите номер телефона (79123456789): {COLOR_CODE['RESET']}").strip()
    
    # 1. Геолокация
    print(f"\n{COLOR_CODE['YELLOW']}=== ГЕОЛОКАЦИЯ НОМЕРА ==={COLOR_CODE['RESET']}")
    await check_geolocation(phone)
    
    # 2. Поиск в ВК
    print(f"\n{COLOR_CODE['YELLOW']}=== ПРОВЕРКА VK ==={COLOR_CODE['RESET']}")
    await search_vk(phone)
    
    # 3. Основной поиск по базам
    await run_async_checks(phone)

def whatsapp_search_part(phone):
    if not phone.isdigit():
        print(f"{COLOR_CODE['RED']}╠═Номер должен содержать только цифры{COLOR_CODE['RESET']}")
        return
    
    print(f"{COLOR_CODE['YELLOW']}[ - ] Поиск в WhatsApp...{COLOR_CODE['RESET']}")
    url = f"https://wa.me/{phone}"
    try:
        response = requests.head(
            url,
            allow_redirects=True,
            timeout=5,
            headers={"User-Agent": random.choice(USER_AGENTS)}
        )
        if 'message/' in response.url:
            print(f"{COLOR_CODE['GREEN']}╠═Номер телефона: {phone}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}╠═Зарегистрирован: Нет{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}╠═Ссылка: {url}{COLOR_CODE['RESET']}")
        else:
            parsed_url = urlparse(response.url)
            query_params = parse_qs(parsed_url.query)
            name = query_params.get('text', [None])[0]
            print(f"{COLOR_CODE['GREEN']}╠═Номер телефона: {phone}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}╠═Зарегистрирован: Да{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}╠═Имя/ник: {name if name else 'Не удалось получить'}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}╠═Ссылка: {response.url}{COLOR_CODE['RESET']}")
    except Exception as e:
        print(f"{COLOR_CODE['RED']}╠═Ошибка: {e}{COLOR_CODE['RESET']}")

def vk_search():
    user_id = input(f"{COLOR_CODE['CYAN']}Введите ID/Username пользователя VK: {COLOR_CODE['RESET']}")
    print(f"{COLOR_CODE['YELLOW']}[ - ] Поиск через API ВКонтакте...{COLOR_CODE['RESET']}")
    try:
        params = {
            "access_token": VK_TOKEN,
            "v": "5.131",
            "user_ids": user_id,
            "fields": "first_name,last_name,status,sex,city,country,photo_max_orig,mobile_phone,home_phone,schools,universities"
        }
        response = requests.get("https://api.vk.com/method/users.get", params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if "response" not in data or not data["response"]:
            print(f"{COLOR_CODE['RED']}[ + ] Пользователь не найден{COLOR_CODE['RESET']}")
        else:
            user = data["response"][0]
            
            print(f"{COLOR_CODE['GREEN']}[ + ] Найден пользователь ВКонтакте:{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] Имя: {user.get('first_name', 'Не указано')}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] Фамилия: {user.get('last_name', 'Не указано')}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] Статус: {user.get('status', 'Не указан')}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] Пол: {'Мужской' if user.get('sex') == 2 else 'Женский' if user.get('sex') == 1 else 'Не указан'}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] Город: {user.get('city', {}).get('title', 'Не указан')}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] Страна: {user.get('country', {}).get('title', 'Не указана')}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] Мобильный телефон: {user.get('mobile_phone', 'Не указан')}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] Домашний телефон: {user.get('home_phone', 'Не указан')}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] ID: {user.get('id', 'Не указан')}{COLOR_CODE['RESET']}")

            schools = user.get('schools', [])
            universities = user.get('universities', [])
            
            if schools:
                print(f"{COLOR_CODE['GREEN']}[ + ] Школы:{COLOR_CODE['RESET']}")
                for school in schools:
                    print(f"  - {school.get('name', 'Неизвестно')} (г. {school.get('city', 'Не указан')})")
                    
            if universities:
                print(f"{COLOR_CODE['GREEN']}[ + ] Университеты:{COLOR_CODE['RESET']}")
                for uni in universities:
                    print(f"  - {uni.get('name', 'Неизвестно')} (г. {uni.get('city', 'Не указан')})")

            print(f"\n{COLOR_CODE['YELLOW']}[ - ] Поиск родственников по фамилии...{COLOR_CODE['RESET']}")
            last_name = user.get('last_name', '').lower()
            
            if not last_name:
                print(f"{COLOR_CODE['RED']}[ ! ] Фамилия не указана, поиск невозможен{COLOR_CODE['RESET']}")
            else:
                friends_params = {
                    "access_token": VK_TOKEN,
                    "v": "5.131",
                    "user_id": user["id"],
                    "fields": "last_name"
                }
                friends_response = requests.get("https://api.vk.com/method/friends.get", params=friends_params, timeout=10)
                friends_response.raise_for_status()
                
                friends_data = friends_response.json()
                
                if "error" in friends_data or "response" not in friends_data:
                    print(f"{COLOR_CODE['RED']}[ ! ] Не удалось получить список друзей{COLOR_CODE['RESET']}")
                else:
                    relatives = [
                        friend for friend in friends_data["response"]["items"] 
                        if friend.get('last_name', '').lower() == last_name
                    ]

                    print(f"\n{COLOR_CODE['GREEN']}[ + ] Найдено {len(relatives)} возможных родственников:{COLOR_CODE['RESET']}")
                    for rel in relatives:
                        print(f"  • {rel.get('first_name', '?')} {rel.get('last_name', '?')} (ID: {rel.get('id', 'N/A')}")
        
    except Exception as e:
        print(f"{COLOR_CODE['RED']}[ + ] Ошибка: {e}{COLOR_CODE['RESET']}")
    
    # ИНТЕГРАЦИЯ ОСНОВНЫХ БАЗ
    asyncio.run(run_async_checks(user_id))

def ip_search():
    ip = input(f"{COLOR_CODE['CYAN']}Введите IP-адрес (или 0 для выхода): {COLOR_CODE['RESET']}")
    if ip == "0":
        return
    
    print(f"{COLOR_CODE['YELLOW']}[ - ] Поиск информации...{COLOR_CODE['RESET']}")
    
    try:
        api1 = f"http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,region,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query&lang=ru"
        data1 = requests.get(api1, timeout=5).json()
        
        if data1['status'] == 'fail':
            print(f"{COLOR_CODE['RED']}[ + ] Ошибка: {data1['message']}{COLOR_CODE['RESET']}")
            return
        
        try:
            api2 = f"https://ipinfo.io/{ip}/json"
            data2 = requests.get(api2, timeout=5).json()
        except:
            data2 = {}
        
        address_info = {}
        if 'lat' in data1 and 'lon' in data1:
            address_info = get_address_by_coordinates(data1['lat'], data1['lon'])
        
        print(f"\n{COLOR_CODE['GREEN']}=== Основная информация ==={COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] IP: {data1.get('query', 'Неизвестно')}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] Провайдер: {data1.get('isp', data2.get('org', 'Неизвестно'))}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] Организация: {data1.get('org', data2.get('org', 'Неизвестно'))}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] ASN: {data1.get('as', data2.get('asn', 'Неизвестно'))}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] Город: {data1.get('city', data2.get('city', 'Неизвестно'))}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] Регион: {data1.get('regionName', data2.get('region', 'Неизвестно'))}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] Страна: {data1.get('country', data2.get('country', 'Неизвестно'))} ({data1.get('countryCode', '')}){COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] Континент: {data1.get('continent', 'Неизвестно')}{COLOR_CODE['RESET']}")
        
        if 'loc' in data2:
            print(f"{COLOR_CODE['GREEN']}[ + ] Координаты: {data2['loc']}{COLOR_CODE['RESET']}")
        elif 'lat' in data1 and 'lon' in data1:
            print(f"{COLOR_CODE['GREEN']}[ + ] Координаты: {data1['lat']}, {data1['lon']}{COLOR_CODE['RESET']}")
        
        print(f"{COLOR_CODE['GREEN']}[ + ] Почтовый индекс: {data1.get('zip', data2.get('postal', 'Неизвестно'))}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] Часовой пояс: {data1.get('timezone', data2.get('timezone', 'Неизвестно'))}{COLOR_CODE['RESET']}")
        
        if isinstance(address_info, dict) and address_info:
            print(f"\n{COLOR_CODE['GREEN']}=== Информация о местоположении ==={COLOR_CODE['RESET']}")
            translated_address = translate_address(address_info)
            for key, value in translated_address.items():
                print(f"{COLOR_CODE['GREEN']}[ + ] {key}: {value}{COLOR_CODE['RESET']}")
        
        print(f"\n{COLOR_CODE['GREEN']}=== Техническая информация ==={COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] VPN/Proxy: {'Да' if data1.get('proxy', False) else 'Нет'}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] Хостинг: {'Да' if data1.get('hosting', False) else 'Нет'}{COLOR_CODE['RESET']}")
        print(f"{COLOR_CODE['GREEN']}[ + ] Мобильное соединение: {'Да' if data1.get('mobile', False) else 'Нет'}{COLOR_CODE['RESET']}")
        
        # Интеграция dork search в поиск по IP
        print(f"\n{COLOR_CODE['YELLOW']}=== Google Dorks для IP ==={COLOR_CODE['RESET']}")
        ip_dork_search_links(ip)
        
    except Exception as e:
        print(f"{COLOR_CODE['RED']}[ + ] Ошибка: {e}{COLOR_CODE['RESET']}")
        
    # ИНТЕГРАЦИЯ ОСНОВНЫХ БАЗ ПО IP
    asyncio.run(run_async_checks(ip))

def ip_dork_search_links(ip):
    dorks = [f'"{ip}"', f'"{ip}" site:shodan.io', f'"{ip}" site:censys.io']
    for dork in dorks:
        encoded_dork = urllib.parse.quote_plus(dork)
        print(f"{COLOR_CODE['CYAN']}[ * ] https://www.google.com/search?q={encoded_dork}{COLOR_CODE['RESET']}")

def email_search():
    email = input(f"{COLOR_CODE['CYAN']}Введите email: {COLOR_CODE['RESET']}")
    print(f"{COLOR_CODE['YELLOW']}[ - ] Поиск...{COLOR_CODE['RESET']}")
    
    print(f"\n{COLOR_CODE['YELLOW']}=== ПРОВЕРКА В HUDSON ROCK ==={COLOR_CODE['RESET']}")
    try:
        url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email?email={email}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            stealers_data = data.get("stealers", [])
            if stealers_data:
                print(f"{COLOR_CODE['GREEN']}[ + ] Найдено записей: {len(stealers_data)}{COLOR_CODE['RESET']}")
                for entry in stealers_data[:3]: # Показываем первые 3 для компактности
                    print(f"{COLOR_CODE['GREEN']}║   • Дата: {entry.get('date_compromised', '/')}{COLOR_CODE['RESET']}")
                    print(f"{COLOR_CODE['GREEN']}║   • Пароли: {', '.join(entry.get('top_passwords', []))}{COLOR_CODE['RESET']}")
            else:
                print(f"{COLOR_CODE['RED']}[ + ] Данные в Hudson Rock не найдены{COLOR_CODE['RESET']}")
    except Exception as e:
        print(f"{COLOR_CODE['RED']}[ + ] Ошибка Hudson Rock: {e}{COLOR_CODE['RESET']}")

    # ОСНОВНЫЕ БАЗЫ ВЫЗЫВАЮТСЯ ТУТ
    asyncio.run(run_async_checks(email))

def address_search():
    address = input(f"{COLOR_CODE['CYAN']}Введите адрес для поиска (Город, Улица, Дом и т.д.): {COLOR_CODE['RESET']}").strip()
    if address:
        asyncio.run(run_async_checks(address))
    else:
        print(f"{COLOR_CODE['RED']}[ ! ] Адрес не может быть пустым{COLOR_CODE['RESET']}")

def mac_search():
    mac = input(f"{COLOR_CODE['CYAN']}Введите MAC-адрес: {COLOR_CODE['RESET']}").strip()
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}", timeout=5)
        if response.status_code == 200:
            print(f"{COLOR_CODE['GREEN']}[ + ] Производитель: {response.text}{COLOR_CODE['RESET']}")
        else:
            print(f"{COLOR_CODE['RED']}[ + ] Не найдено{COLOR_CODE['RESET']}")
    except Exception as e: print(f"Ошибка: {e}")

def name_search():
    name = input(f"{COLOR_CODE['CYAN']}Введите ФИО: {COLOR_CODE['RESET']}")
    print(f"{COLOR_CODE['YELLOW']}[ - ] Поиск по реестрам...{COLOR_CODE['RESET']}")
    url = f"https://api.ofdata.ru/v2/search?key=KBnpz1CHKNngFXxK&by=founder-name&obj=org&query={name}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('data', {}).get('Записи'):
            org = data['data']['Записи'][0]
            print(f"{COLOR_CODE['GREEN']}[ + ] Организация: {org.get('НаимПолн')}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] ИНН: {org.get('ИНН')}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] Адрес: {org.get('ЮрАдрес')}{COLOR_CODE['RESET']}")
    except: pass
    
    # ПОИСК ПО БАЗАМ ДЛЯ ФИО
    asyncio.run(run_async_checks(name))

def decode_vin():
    vin = input(f"{COLOR_CODE['CYAN']}Введите VIN: {COLOR_CODE['RESET']}").strip().upper()
    if len(vin) != 17: 
        print(f"{COLOR_CODE['RED']}[ ! ] Длина VIN-кода должна составлять 17 символов.{COLOR_CODE['RESET']}")
        return
    
    country_codes = {"J": "Япония", "K": "Корея", "L": "Китай", "W": "Германия", "X": "Россия"}
    print(f"{COLOR_CODE['GREEN']}[ + ] Страна: {country_codes.get(vin[0], 'Неизвестно')}{COLOR_CODE['RESET']}")
    
    year_codes = {'A': 2010, 'B': 2011, 'C': 2012, 'D': 2013, 'E': 2014, 'F': 2015, 'G': 2016}
    print(f"{COLOR_CODE['GREEN']}[ + ] Год: {year_codes.get(vin[9], 'Неизвестно')}{COLOR_CODE['RESET']}")

    # ИНТЕГРАЦИЯ БАЗ ПО VIN
    asyncio.run(run_async_checks(vin))

def telegram_bot_search():
    token = input(f"{COLOR_CODE['YELLOW']}Введите токен бота: {COLOR_CODE['RESET']}")
    try:
        data = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()
        if data.get("ok"):
            res = data["result"]
            print(f"{COLOR_CODE['GREEN']}[ + ] ID: {res['id']}{COLOR_CODE['RESET']}")
            print(f"{COLOR_CODE['GREEN']}[ + ] Username: @{res.get('username')}{COLOR_CODE['RESET']}")
    except: pass

def snils_search():
    snils = input(f"{COLOR_CODE['CYAN']}Введите СНИЛС (11 цифр): {COLOR_CODE['RESET']}").strip()
    cleaned = ''.join(c for c in snils if c.isdigit())
    if len(cleaned) == 11:
        asyncio.run(run_async_checks(cleaned))
    else:
        print("Ошибка формата")

def inn_search():
    inn = input("Введите ИНН: ").strip()
    if not inn.isdigit(): return
    try:
        res = requests.post("https://egrul.nalog.ru/", data={"query": inn}).json()
        token = res.get("t")
        if token:
            data = requests.get(f"https://egrul.nalog.ru/search-result/{token}").json()
            if data.get("rows"):
                c = data["rows"][0]
                print(f"Название: {c.get('n')}\nАдрес: {c.get('a')}")
    except: pass

    # ИНТЕГРАЦИЯ БАЗ ПО ИНН
    asyncio.run(run_async_checks(inn))

def main():
    # --- БЛОК ЗАЩИТЫ ---
    print("Инициализация системы защиты...")
    if not check_access():
        print(f"{COLOR_CODE['RED']}Ошибка доступа: Ваше устройство не авторизовано.{COLOR_CODE['RESET']}")
        sys.exit()
    # -------------------

    while True:
        clear_screen()
        print_banner()
        print_menu()
        choice = input(f"{COLOR_CODE['CYAN']}Выберите действие: {COLOR_CODE['RESET']}")
        
        if choice == '1':
            asyncio.run(combined_phone_search())
        elif choice == '2':
            vk_search()
        elif choice == '3':
            ip_search()
        elif choice == '4':
            email_search()
        elif choice == '5':
            address_search()
        elif choice == '6':
            mac_search()
        elif choice == '7':
            name_search()
        elif choice == '8':
            decode_vin()
        elif choice == '9':
            snils_search()
        elif choice == '10':
            inn_search()
        elif choice == '11':
            telegram_bot_search()
        elif choice == '0':
            break
        
        input(f"\n{COLOR_CODE['YELLOW']}Нажмите Enter для продолжения...{COLOR_CODE['RESET']}")

if __name__ == "__main__":
    main()
