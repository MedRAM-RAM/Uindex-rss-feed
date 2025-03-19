import re
from xml.etree import ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# معايير البحث (يمكنك تغييرها حسب الحاجة)
search_params = {
    "show_name": "Daredevil Born Again",
    "season": "01",
    "episode": "04",
    "quality": "1080p",
    "encoding": "x265",
    "team": "MeGusta"
}

# بناء نمط البحث باستخدام تعبير منتظم
pattern = rf"{re.escape(search_params['show_name'])}\s+S{search_params['season']}E{search_params['episode']}\s+{search_params['quality']}\s+.*{search_params['encoding']}.* -{search_params['team']}"

# إعداد المتصفح لـ selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # تشغيل بدون واجهة
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

# رابط البحث في eztvx.to
search_query = search_params['show_name'].replace(" ", "+")
url = f"https://eztvx.to/search/?q={search_query}"
driver.get(url)

# انتظر تحميل المحتوى
driver.implicitly_wait(10)

# استخراج مصدر الصفحة
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# البحث عن النتائج (اضبط حسب بنية الموقع)
results = soup.find_all('div', class_='card')  # افتراضي، قد تحتاج لتغييره

# إنشاء هيكل ملف RSS
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = f"{search_params['show_name']} S{search_params['season']}E{search_params['episode']} RSS Feed"
ET.SubElement(channel, "link").text = url
ET.SubElement(channel, "description").text = f"RSS feed for {search_params['show_name']} S{search_params['season']}E{search_params['episode']}"

# تصفية النتائج وإضافتها إلى RSS
for result in results:
    title_tag = result.find('h2') or result.find('a', class_='title')  # العنوان
    link_tag = result.find('a', href=re.compile(r'\.torrent$|^magnet:'))  # الرابط

    if title_tag and re.search(pattern, title_tag.text, re.IGNORECASE):
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title_tag.text.strip()
        ET.SubElement(item, "link").text = link_tag['href'] if link_tag else url
        ET.SubElement(item, "description").text = "Available link"

# حفظ ملف RSS
tree = ET.ElementTree(rss)
tree.write("search_rss.xml", encoding="utf-8", xml_declaration=True)
