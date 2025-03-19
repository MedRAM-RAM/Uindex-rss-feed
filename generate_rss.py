import requests
from bs4 import BeautifulSoup
import re
from xml.etree import ElementTree as ET

# معايير البحث (يمكنك تغييرها حسب رغبتك)
search_term = "daredevil born again"  # اكتب ما تبحث عنه
quality = "1080p"            # الجودة المطلوبة
encoding = "x265"            # نوع الترميز

# رابط صفحة البحث
url = f"https://uindex.org/search.php?search={search_term}"

# تحميل الصفحة
headers = {"User-Agent": "Mozilla/5.0"}  # لتجنب حظر الموقع
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# استخراج النتائج (قد تحتاج لتعديل هذا السطر حسب بنية الموقع)
results = soup.find_all('div', class_='search-result')  # افتراضي

# إنشاء ملف RSS
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = f"نتائج البحث: {search_term}"
ET.SubElement(channel, "link").text = url
ET.SubElement(channel, "description").text = f"RSS لـ {search_term} بجودة {quality}"

# تصفية النتائج باستخدام تعبير منتظم
pattern = rf".*{quality}.*{encoding}.*"

for result in results:
    title_tag = result.find('h2') or result.find('a')  # استخراج العنوان
    if title_tag and re.search(pattern, title_tag.text, re.IGNORECASE):
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title_tag.text.strip()
        
        # استخراج رابط التورنت أو المغناطيسي
        link = result.find('a', href=re.compile(r'\.torrent$')) or result.find('a', href=re.compile(r'^magnet:'))
        ET.SubElement(item, "link").text = link['href'] if link else url
        ET.SubElement(item, "description").text = "رابط متاح"

# حفظ ملف RSS
tree = ET.ElementTree(rss)
tree.write("search_rss.xml", encoding="utf-8", xml_declaration=True)
