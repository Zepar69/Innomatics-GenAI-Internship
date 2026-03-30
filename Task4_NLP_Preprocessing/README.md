# 🧠 NLP Preprocessing Engine

A production-ready Natural Language Processing (NLP) preprocessing pipeline designed to clean, normalize, and transform noisy real-world text into structured data suitable for machine learning models.

---

## 📌 Project Overview

In real-world NLP applications, raw text data is often messy and unstructured. This project builds a robust, modular preprocessing engine that handles such data effectively using advanced text cleaning techniques.

The pipeline is designed to be reusable, scalable, and easy to integrate into ML workflows.

---

## 🎯 Objectives

- Clean noisy real-world text data
- Normalize and standardize textual inputs
- Generate meaningful tokens
- Perform token-level statistical analysis
- Build a complete NLP preprocessing pipeline

---

## ⚙️ Features

- ✅ Lowercasing text
- ✅ Removal of numbers
- ✅ Removal of URLs and email patterns
- ✅ Handling repeated characters (e.g., `soooo` → `so`)
- ✅ Removal of special characters and emojis
- ✅ Removal of extra spaces
- ✅ Tokenization
- ✅ Removal of short tokens (≤ 2 characters, except `no`, `not`)
- ✅ Error handling for edge cases (empty strings, emoji-only, number-only inputs)

---

## 🧪 Sample Input

```python
[
    "Get 100% FREE access now!!!",
    "I absolutely looooved this product 😍😍",
    "Visit https://openai.com now!",
    "I am not happy with this"
]
```

## 📤 Sample Output

```python
{
    "tokens": [
        ["get", "free", "access", "now"],
        ["absolutely", "loved", "product"],
        ["visit", "now"],
        ["not", "happy"]
    ],
    "clean_sentences": [
        "get free access now",
        "absolutely loved product",
        "visit now",
        "not happy"
    ]
}
```

---

## 🗂️ Tasks Covered

| Task | Description |
|------|-------------|
| Task 1 | Conceptual Understanding (Written) |
| Task 2 | Advanced Preprocessing Function |
| Task 3 | Stress Testing on 10 diverse sentences |
| Task 4 | Token Analytics per sentence |
| Task 5 | Frequency Analysis using Counter |
| Task 6 | Full Pipeline Function |
| Task 7 | Error Handling & Edge Cases |

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Libraries:** `re`, `collections`, `string`
- **Environment:** Google Colab / Jupyter Notebook

---

## 📁 File Structure

```
NLP-preprocessing-engine/
│
└── NLP_Assignment1.ipynb   # Main notebook with all tasks
```

---

## 🚀 How to Run

1. Open `NLP_Assignment1.ipynb` in Google Colab or Jupyter Notebook
2. Run all cells from top to bottom
3. No additional installations required — uses Python standard libraries only

---

*Data Science Internship – February 2026*
