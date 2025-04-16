# 🔗 Government Links Current Affairs Grabber

A Python-based scraping system to collect exam-relevant current affairs content from official government websites.  
Perfect for SSC, UPSC, Railways, Banking, and other competitive exam content pipelines.

---

## 🔍 Features

- ✅ Scrapes articles from official sources like:
  - [PIB India](https://pib.gov.in)
  - [NewsOnAir](https://newsonair.gov.in)

- ✅ Collects:
  - Headlines
  - URLs
  - Post dates
- ✅ Filters **date-wise content**
- ✅ Supports pagination where available
- ✅ Outputs clean data for downstream processing (e.g., bilingual one-liners)

---

## 🛠 Tech Stack

- **Python 3**
- **requests** – for sending GET/POST requests
- **BeautifulSoup (bs4)** – HTML parsing
- **re / datetime** – pattern matching & date parsing
- **pandas** (optional) – tabular exports

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/govt-links-grabber.git
cd govt-links-grabber
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run scraper

```bash
python grab_links.py
```

---

## 📁 Project Structure

```
.
├── grab_links.py
├── modules/
│   ├── pib.py
│   ├── air.py
│   ├── mea.py
│   └── utils.py
├── output/
│   └── links_YYYY-MM-DD.csv
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ✅ Sample Output

```csv
Title, Source, Date, Link
PM launches solar scheme, pib.gov.in, 2025-04-14, https://pib.gov.in/PressRel.aspx?ID=2121577
India signs MoU with Japan, mea.gov.in, 2025-04-13, https://mea.gov.in/pressrelease.htm?ID=4987
...
```

---

## 💡 Use Case

This tool is used as a **feeder system** for your bilingual one-liner current affairs generator.  
It provides raw but clean source links and metadata that you can later process into PDF/HTML/WordPress formats.

---

## ✨ Author

Made with 🔥 by [Ujjawal Biswas](https://krispnotes.in)  
Like it? ⭐ the repo and help others discover it!

---

## 📄 License

This project is free to use and open-source.
