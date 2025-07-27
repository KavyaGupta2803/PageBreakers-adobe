import fitz  # PyMuPDF
import os
import json
from collections import defaultdict, Counter

input_dir = "input"
output_dir = "output"

def extract_title(page):
    blocks = page.get_text("dict")["blocks"]
    title_spans = []

    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                size = span["size"]
                text = span["text"].strip()
                if text and len(text) > 3 and "http" not in text.lower():
                    title_spans.append((size, text))

    title_spans.sort(reverse=True)  # Largest font sizes first
    title_lines = []
    max_font = title_spans[0][0] if title_spans else 0

    for size, text in title_spans:
        if abs(size - max_font) < 0.5:
            title_lines.append(text)
        if len(title_lines) >= 3:
            break

    return " ".join(title_lines).strip()

def get_level(size):
    if size >= 17:
        return "H1"
    elif size >= 14:
        return "H2"
    elif size >= 11.5:
        return "H3"
    else:
        return None

def clean_text(text):
    return text.strip().replace("\u00a0", " ").replace("–", "-")

def extract_headings(doc, title):
    all_headings = []
    seen = set()
    overview_counter = Counter()

    for page_num, page in enumerate(doc):
        spans_by_y = defaultdict(list)

        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = clean_text(span["text"])
                    if not text or len(text) <= 3:
                        continue
                    size = span["size"]
                    font = span.get("font", "").lower()
                    level = get_level(size)
                    if not level:
                        continue

                    # New: filter out short or irrelevant lines
                    if len(text.strip()) < 12 or len(text.split()) < 2:
                        continue

                    # New: skip small, non-bold fonts
                    if size < 12 and "bold" not in font:
                        continue

                    y = round(span["bbox"][1], 1)
                    spans_by_y[(level, y)].append(text)

        for (level, y), texts in spans_by_y.items():
            full_line = " ".join(texts).strip()
            if full_line.lower().startswith("http"):
                continue
            if full_line in seen:
                continue
            if "overview" in full_line.lower():
                overview_counter[full_line] += 1
                if overview_counter[full_line] > 1:
                    continue
            if full_line == title:
                continue
            seen.add(full_line)
            all_headings.append({
                "level": level,
                "text": full_line,
                "page": page_num
            })

    return all_headings

def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    title = extract_title(doc[0])
    headings = extract_headings(doc, title)
    return {
        "title": title,
        "outline": headings
    }

def main():
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if not filename.endswith(".pdf"):
            continue
        filepath = os.path.join(input_dir, filename)
        output_filename = filename.replace(".pdf", ".json")
        outpath = os.path.join(output_dir, output_filename)

        try:
            result = process_pdf(filepath)
            with open(outpath, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"✅ {filename} → {output_filename}")
        except Exception as e:
            print(f"❌ Error in {filename}: {e}")

if __name__ == "__main__":
    main()
