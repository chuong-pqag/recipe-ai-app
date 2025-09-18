<<<<<<< HEAD
import requests
from bs4 import BeautifulSoup
import csv
import time
import json
import re

BASE_URL = "https://monngonmoingay.com"
OUTPUT_CSV = "mon_an200.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

EXCLUDED_LINKS = {
    "https://monngonmoingay.com/lich-phat-song/",
    "https://monngonmoingay.com/thuc-don-dinh-duong/",
    "https://monngonmoingay.com/dieu-khoan-su-dung",
    "https://monngonmoingay.com/chinh-sach-bao-ve-du-lieu-ca-nhan",
    "https://monngonmoingay.com/gia-vi-ban-can/",
    "https://monngonmoingay.com/tich-diem-doi-qua-cung-ajinomoto-tai-qua-tang-ajinomoto/",
    "https://monngonmoingay.com/lay-lai-mat-khau/",
    "https://monngonmoingay.com/mach-nho/",
    "https://monngonmoingay.com/tim-kiem-mon-ngon/",
    "https://monngonmoingay.com/ke-hoach-nau-an/"
}


def get_links_from_page(page_num):
    url = f"{BASE_URL}/tim-kiem-mon-ngon/page/{page_num}/"
    print(f"📄 Đang xử lý trang {page_num} → {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        recipe_links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if re.fullmatch(r"https://monngonmoingay\.com/[^/]+/?", href) and href not in EXCLUDED_LINKS:
                recipe_links.add(href)
        return list(recipe_links)
    except Exception as e:
        print(f"❌ Lỗi tại trang {page_num}: {e}")
        return []


def extract_dom_section(soup, section_id):
    section = soup.find(id=section_id)
    lines = []
    if section:
        for tag in section.find_all(["p", "li", "div"]):
            txt = tag.get_text(strip=True)
            if txt:
                lines.append(txt)
    return lines


def extract_jsonld_recipe(soup):
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") == "Recipe":
                return data
        except:
            continue
    return None


def extract_video_url(soup, jsonld):
    # Ưu tiên video trong JSON-LD kiểu Recipe
    if jsonld and "video" in jsonld:
        video = jsonld["video"]
        if isinstance(video, dict):
            return video.get("contentUrl") or video.get("embedUrl") or video.get("url") or ""
        elif isinstance(video, list) and len(video) > 0:
            return video[0].get("contentUrl") or video[0].get("embedUrl") or video[0].get("url") or ""

    # Fallback: tìm trong các block VideoObject
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") in ["VideoObject", ["VideoObject", "LearningResource"]]:
                return data.get("contentUrl", "")
        except:
            continue

    # Fallback cuối: iframe YouTube
    iframe = soup.find("iframe", src=re.compile(r"(youtube\.com|youtu\.be)"))
    if iframe:
        return iframe.get("src", "")

    return ""


def parse_recipe(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Không rõ"

        image_tag = soup.select_one("img.img_detail_monan")
        image_url = image_tag["src"] if image_tag else ""
        if not image_url:
            return None

        ingredients = []
        ingr_list = soup.select("#section-nguyenlieu ul li span")
        for span in ingr_list:
            txt = span.get_text(strip=True)
            if txt:
                ingredients.append(txt)

        jsonld = extract_jsonld_recipe(soup)
        if not ingredients and jsonld and "recipeIngredient" in jsonld:
            ingredients = jsonld["recipeIngredient"]

        parts = {
            "Sơ chế": extract_dom_section(soup, "section-soche"),
            "Thực hiện": extract_dom_section(soup, "section-thuchien"),
            "Cách dùng": extract_dom_section(soup, "section-howtouse")
        }

        if jsonld and "recipeInstructions" in jsonld:
            for step in jsonld["recipeInstructions"]:
                name = step.get("name", "").strip()
                text = step.get("text", "").strip()
                if name.lower().startswith("sơ") and not parts["Sơ chế"]:
                    parts["Sơ chế"] = [text]
                elif name.lower().startswith("thực") and not parts["Thực hiện"]:
                    parts["Thực hiện"] = [text]
                elif name.lower().startswith("cách") and not parts["Cách dùng"]:
                    parts["Cách dùng"] = [text]

        def build_section(title, items):
            if not items:
                return f"{title}:\nKhông có nội dung."
            clean_items = [i for i in items if not re.match(fr"{title}[:：]?", i, re.IGNORECASE)]
            return f"{title}:\n" + "\n".join(clean_items)

        instruction_text = "\n\n".join([
            build_section("Sơ chế", parts["Sơ chế"]),
            build_section("Thực hiện", parts["Thực hiện"]),
            build_section("Cách dùng", parts["Cách dùng"])
        ])

        video_url = extract_video_url(soup, jsonld)

        return {
            "Tên món": title,
            "Nguyên liệu": "; ".join(ingredients),
            "Cách làm": instruction_text,
            "Ảnh": image_url,
            "Video": video_url,
            "URL": url
        }
    except Exception as e:
        print(f"⚠️ Lỗi đọc món: {url} → {e}")
        return None


def main():
    all_links = []
    for page in range(181, 202):  # có thể đổi giới hạn trang
        links = get_links_from_page(page)
        if not links:
            print(f"⚠️ Trang {page} không có link món ăn.")
        all_links.extend(links)
        time.sleep(0.5)

    all_links = list(set(all_links))
    print(f"✅ Đã thu thập {len(all_links)} link món ăn.")
    results = []

    for i, link in enumerate(all_links, 1):
        print(f"🔍 ({i}/{len(all_links)}) Lấy dữ liệu: {link}")
        data = parse_recipe(link)
        if data:
            results.append(data)
        time.sleep(0.5)

    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Tên món", "Nguyên liệu", "Cách làm", "Ảnh", "Video", "URL"])
        writer.writeheader()
        writer.writerows(results)

    print(f"🎉 Đã lưu thành công: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
=======
import requests
from bs4 import BeautifulSoup
import csv
import time
import json
import re

BASE_URL = "https://monngonmoingay.com"
OUTPUT_CSV = "mon_an200.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

EXCLUDED_LINKS = {
    "https://monngonmoingay.com/lich-phat-song/",
    "https://monngonmoingay.com/thuc-don-dinh-duong/",
    "https://monngonmoingay.com/dieu-khoan-su-dung",
    "https://monngonmoingay.com/chinh-sach-bao-ve-du-lieu-ca-nhan",
    "https://monngonmoingay.com/gia-vi-ban-can/",
    "https://monngonmoingay.com/tich-diem-doi-qua-cung-ajinomoto-tai-qua-tang-ajinomoto/",
    "https://monngonmoingay.com/lay-lai-mat-khau/",
    "https://monngonmoingay.com/mach-nho/",
    "https://monngonmoingay.com/tim-kiem-mon-ngon/",
    "https://monngonmoingay.com/ke-hoach-nau-an/"
}


def get_links_from_page(page_num):
    url = f"{BASE_URL}/tim-kiem-mon-ngon/page/{page_num}/"
    print(f"📄 Đang xử lý trang {page_num} → {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        recipe_links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if re.fullmatch(r"https://monngonmoingay\.com/[^/]+/?", href) and href not in EXCLUDED_LINKS:
                recipe_links.add(href)
        return list(recipe_links)
    except Exception as e:
        print(f"❌ Lỗi tại trang {page_num}: {e}")
        return []


def extract_dom_section(soup, section_id):
    section = soup.find(id=section_id)
    lines = []
    if section:
        for tag in section.find_all(["p", "li", "div"]):
            txt = tag.get_text(strip=True)
            if txt:
                lines.append(txt)
    return lines


def extract_jsonld_recipe(soup):
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") == "Recipe":
                return data
        except:
            continue
    return None


def extract_video_url(soup, jsonld):
    # Ưu tiên video trong JSON-LD kiểu Recipe
    if jsonld and "video" in jsonld:
        video = jsonld["video"]
        if isinstance(video, dict):
            return video.get("contentUrl") or video.get("embedUrl") or video.get("url") or ""
        elif isinstance(video, list) and len(video) > 0:
            return video[0].get("contentUrl") or video[0].get("embedUrl") or video[0].get("url") or ""

    # Fallback: tìm trong các block VideoObject
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") in ["VideoObject", ["VideoObject", "LearningResource"]]:
                return data.get("contentUrl", "")
        except:
            continue

    # Fallback cuối: iframe YouTube
    iframe = soup.find("iframe", src=re.compile(r"(youtube\.com|youtu\.be)"))
    if iframe:
        return iframe.get("src", "")

    return ""


def parse_recipe(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Không rõ"

        image_tag = soup.select_one("img.img_detail_monan")
        image_url = image_tag["src"] if image_tag else ""
        if not image_url:
            return None

        ingredients = []
        ingr_list = soup.select("#section-nguyenlieu ul li span")
        for span in ingr_list:
            txt = span.get_text(strip=True)
            if txt:
                ingredients.append(txt)

        jsonld = extract_jsonld_recipe(soup)
        if not ingredients and jsonld and "recipeIngredient" in jsonld:
            ingredients = jsonld["recipeIngredient"]

        parts = {
            "Sơ chế": extract_dom_section(soup, "section-soche"),
            "Thực hiện": extract_dom_section(soup, "section-thuchien"),
            "Cách dùng": extract_dom_section(soup, "section-howtouse")
        }

        if jsonld and "recipeInstructions" in jsonld:
            for step in jsonld["recipeInstructions"]:
                name = step.get("name", "").strip()
                text = step.get("text", "").strip()
                if name.lower().startswith("sơ") and not parts["Sơ chế"]:
                    parts["Sơ chế"] = [text]
                elif name.lower().startswith("thực") and not parts["Thực hiện"]:
                    parts["Thực hiện"] = [text]
                elif name.lower().startswith("cách") and not parts["Cách dùng"]:
                    parts["Cách dùng"] = [text]

        def build_section(title, items):
            if not items:
                return f"{title}:\nKhông có nội dung."
            clean_items = [i for i in items if not re.match(fr"{title}[:：]?", i, re.IGNORECASE)]
            return f"{title}:\n" + "\n".join(clean_items)

        instruction_text = "\n\n".join([
            build_section("Sơ chế", parts["Sơ chế"]),
            build_section("Thực hiện", parts["Thực hiện"]),
            build_section("Cách dùng", parts["Cách dùng"])
        ])

        video_url = extract_video_url(soup, jsonld)

        return {
            "Tên món": title,
            "Nguyên liệu": "; ".join(ingredients),
            "Cách làm": instruction_text,
            "Ảnh": image_url,
            "Video": video_url,
            "URL": url
        }
    except Exception as e:
        print(f"⚠️ Lỗi đọc món: {url} → {e}")
        return None


def main():
    all_links = []
    for page in range(181, 202):  # có thể đổi giới hạn trang
        links = get_links_from_page(page)
        if not links:
            print(f"⚠️ Trang {page} không có link món ăn.")
        all_links.extend(links)
        time.sleep(0.5)

    all_links = list(set(all_links))
    print(f"✅ Đã thu thập {len(all_links)} link món ăn.")
    results = []

    for i, link in enumerate(all_links, 1):
        print(f"🔍 ({i}/{len(all_links)}) Lấy dữ liệu: {link}")
        data = parse_recipe(link)
        if data:
            results.append(data)
        time.sleep(0.5)

    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Tên món", "Nguyên liệu", "Cách làm", "Ảnh", "Video", "URL"])
        writer.writeheader()
        writer.writerows(results)

    print(f"🎉 Đã lưu thành công: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
>>>>>>> e035a27e8418aa3c57b973fdc6c67abc1cd5bb51
