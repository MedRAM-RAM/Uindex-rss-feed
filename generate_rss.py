import requests
from bs4 import BeautifulSoup
import re
from xml.etree import ElementTree as ET

# تحديد معايير البحث
show_name = "Daredevil Born Again"  # اسم المسلسل
season = "01"                       # رقم الموسم
episode = "04"                      # رقم الحلقة
quality = ""                   # الجودة
encoding = ""                   # الترميز
team = ""                    # اسم الفريق

# بناء نمط البحث باستخدام تعبير منتظم
pattern = rf"{re.escape(show_name)}\s+S{season}E{episode}\s+{quality}\s+.*{encoding}.* -{team}"

# رابط صفحة البحث (يجب تعديله حسب الموقع المستخدم)
url = "https://uindex.org/search.php?search=" + show_name.replace(" ", "+")

# تحميل الصفحة
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# استخراج النتائج (يجب تعديل هذا السطر حسب بنية الموقع)
results = soup.find_all('div', class_='search-result')  # افتراضي

# إنشاء هيكل ملف RSS
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = f"{show_name} S{season}E{episode} {quality} RSS"
ET.SubElement(channel, "link").text = url
ET.SubElement(channel, "description").text = f"RSS feed for {show_name} S{season}E{episode}"

# تصفية النتائج وإضافتها إلى RSS
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
