import requests
from bs4 import BeautifulSoup
import re
from xml.etree import ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# إعداد المتصفح لـ selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # تشغيل بدون واجهة
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

# رابط صفحة البحث (استبدله برابطك الفعلي)
url = "https://uindex.org/search.php?search=Daredevil+Born+Again"
driver.get(url)

# انتظر تحميل المحتوى (اضبط الوقت حسب الحاجة)
driver.implicitly_wait(10)

# استخراج مصدر الصفحة بعد تحميل JavaScript
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# البحث عن <div id="content">
content = soup.find('div', id='content')

if content:
    # استخراج النتائج (اضبط هذا السطر حسب بنية الموقع)
    results = content.find_all('div', class_='result')  # افتراضي، قد تحتاج لتغييره

    # إنشاء هيكل ملف RSS
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "خلاصة RSS من البحث"
    ET.SubElement(channel, "link").text = url
    ET.SubElement(channel, "description").text = "خلاصة لنتائج البحث"

    # تعبير منتظم لتصفية النتائج (مثال)
    pattern = r"Daredevil Born Again S01E04 1080p HEVC x265-MeGusta"

    for result in results:
        title_tag = result.find('h2')  # العنوان (اضبط حسب الموقع)
        link_tag = result.find('a', href=re.compile(r'\.torrent$|^magnet:'))  # الرابط

        if title_tag and re.search(pattern, title_tag.text, re.IGNORECASE):
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = title_tag.text.strip()
            ET.SubElement(item, "link").text = link_tag['href'] if link_tag else url
            ET.SubElement(item, "description").text = "رابط متاح"

    # حفظ ملف RSS
    tree = ET.ElementTree(rss)
    tree.write("search_rss.xml", encoding="utf-8", xml_declaration=True)
else:
    print("لم يتم العثور على <div id='content'>")
