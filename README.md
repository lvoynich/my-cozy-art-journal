# 🎨 End-to-End Programmatic Art Journal & Data Pipeline Engine (2027)

An automated data pipeline and high-fidelity programmatic PDF layout engine built from scratch using **Python** and **ReportLab**. This system automates the ingestion of daily creative prompts and inspirational quotes into clean JSON databases, which are then compiled algorithmically into a 365-day interactive digital journaling notebook optimized for tablets and print.

## 🚀 The Development Journey & Engineering Pipeline
Building this planner required solving complex data-handling constraints and building a multi-stage software pipeline:

### 1. Data Harvesting & Array Ingestion Phase
- **`build_365_prompts.py`**: A specialized data utility engine designed to programmatically generate, format, and sequentially array 365 unique drawing and journaling prompts, outputting a sanitized `prompts.json` payload structure.
- **`build_365_quotes.py`**: A parsing utility that aggregated classic historical quotes and dynamically synthesized custom inspirational datasets, standardizing varied author properties into a uniform dictionary schema mapping `{"text": "...", "from": "..."}` inside `quotes.json`.

### 2. Geometry Mapping & Hyperlink Resolving Engine
- **`weekly_planner.py`**: The core rendering engine. It handles complex coordinate translations to draw a premium 3D paper stack aesthetic, dynamic bounding margins, and functional layout blocks.
- **The Navigation Link Tree:** Overcame strict ReportLab link compilation mechanics to bind all 365 unique dates, 12 monthly dividers, and a **Unified Yearly Index Page** into a zero-error internal hyperlink routing network.

### 3. AI Asset Generation & Resourceful Engineering
- **Generative AI Art Integration:** Leveraged state-of-the-art text-to-image models to generate a custom, minimalist abstract boho line-art graphic. This asset was scaled and embedded directly into the title page using ReportLab's pixel-precise image boundary matrix.
- **AI-Assisted Pair Programming & Agile Problem-Solving:** Utilized a collaborative development process—combining rigorous technical documentation search via Google with generative AI pair programming—to troubleshoot complex compilation bugs, refactor low-level ReportLab vector calculations, and optimize internal hyperlink trees.
--

## ✨ Key Features
- **Unified Master Index Dashboard:** An all-in-one calendar summary grid page where every date integer is a clickable button jumping directly to that day's journaling tracking sheet.
- **Interactive Month Dividers:** Navigation benchmarks featuring custom horizontal day calendar charts, target-matched side tabs, and expanded **290pt grid pads** for project manifestations.
- **Adaptive Sidebar Binder Tabs:** A 13-tab physical binder stack featuring a custom highlighted **"2027"** index selector that dynamically shifts brand color highlights to match active viewing ranges.
- **Micro-Journaling Vector Components:** Font-independent, custom flowable layout classes utilizing raw canvas vector line transformations to build a 3-state mood reflection selector and a 5-row handwriting lettering tracker.
- **Growth Benchmarking Logic:** A temporary loop state system that caches Day 1 prompts and dynamically injects them onto month-end review sheets, letting users visually analyze their long-term lettering progress.

## 🛠️ Tech Stack
- **Language:** Python 3.13
- **Graphics Framework:** ReportLab PDF Library (Platypus Layouts, Flowables, Vector Canvas Engine)
- **Data Layers:** JSON (Decoupled, modular asset pools)

## 🚀 Quick Start
1. Clone this repository:
   ```bash
   git clone https://github.com
   ```
2. Download the free handwritten font **Gloria Hallelujah** directly from [Google Fonts](https://google.com) and save `GloriaHallelujah-Regular.ttf` in the root folder.
3. Bring any custom asset graphic named `cover_art.png` to act as the title page illustration.
4. Execute the pipeline scripts to build the local databases if needed, then compile the book:
   ```bash
   python build_365_prompts.py
   python build_365_quotes.py
   python weekly_planner.py
   ```
5. Find your fully hyperlinked planner saved cleanly inside your User Home directory!
