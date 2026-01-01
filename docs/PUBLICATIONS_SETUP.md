# Publications Page Setup

This document explains how to set up and maintain the publications page for the BRAINS Group website.

## Overview

The publications page is automatically generated from two shared files:
- `../Oshani-CV/citations.bib` - Contains all BibTeX entries
- `../Oshani-CV/bib-entries.sty` - Categorizes publications by type

## Requirements

- Python 3.6 or higher
- Python virtual environment (recommended)

## Initial Setup

1. **Create a Python virtual environment:**
   ```bash
   python3 -m venv venv
   ```
   
   This creates a virtual environment in a `venv` folder (you can use a different name if preferred).

2. **Activate the virtual environment:**
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   You should see `(venv)` at the beginning of your command prompt when the virtual environment is active.

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install `bibtexparser` for robust BibTeX parsing. If not installed, the script will use a fallback parser (may miss some entries).
   
   **Note:** Make sure your virtual environment is activated before running this command.

4. **Generate the publications page:**
   ```bash
   python3 scripts/generate_publications.py
   ```
   
   This will create/update `publications.qmd` in the project root.
   
   **Note:** Make sure your virtual environment is activated when running this script.

5. **Render the website:**
   ```bash
   quarto render
   ```

## How It Works

1. The script reads `../Oshani-CV/citations.bib` and extracts all publications from 2022 onwards
2. It reads `../Oshani-CV/bib-entries.sty` to determine which category each publication belongs to
3. It generates `publications.qmd` in the project root with:
   - Publications organized by category (Journals, Conferences, Workshops, etc.)
   - Search functionality
   - Links to PDFs and DOIs when available
   - Attractive formatting

## Adding New Publications

To add a new publication:

1. **Add the BibTeX entry** to `../Oshani-CV/citations.bib`
2. **Categorize it** in `../Oshani-CV/bib-entries.sty` by adding the entry key to the appropriate category:
   ```latex
   \addtocategory{conferences}
       {
       your_new_entry_key,
       }
   ```
3. **Activate the virtual environment** (if not already active):
   ```bash
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate      # Windows
   ```

4. **Regenerate the page:**
   ```bash
   python3 scripts/generate_publications.py
   quarto render
   ```

## Categories

The following categories are supported:
- `journals` - Journal Articles
- `conferences` - Conference Papers
- `workshops` - Workshop Papers
- `chapters` - Book Chapters
- `books` - Books
- `techreports` - Technical Reports
- `posters` - Poster Papers
- `demos` - Demo Papers
- `thesis` - Theses
- `magazines` - Magazine Articles
- `patents` - Patents

## Features

- **Search**: Real-time search across all publications
- **Categorization**: Publications organized by type
- **Links**: Automatic links to PDFs and DOIs
- **Year filtering**: Only shows publications from 2022 onwards
- **Responsive**: Works on all screen sizes

## Workflow for Updating Publications

1. **Activate the virtual environment** (if not already active):
   ```bash
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate      # Windows
   ```

2. **Edit source files** (in `../Oshani-CV/`):
   - Add new entries to `citations.bib`
   - Update categories in `bib-entries.sty`

3. **Generate the page:**
   ```bash
   python3 scripts/generate_publications.py
   ```

4. **Preview locally:**
   ```bash
   quarto preview
   ```

5. **Render for deployment:**
   ```bash
   quarto render
   ```

## Troubleshooting

If publications don't appear:
1. Check that the year in the BibTeX entry is >= 2022
2. Verify the entry key is listed in `bib-entries.sty`
3. Check for syntax errors in the BibTeX file
4. Ensure you're running the script from the project root:
   ```bash
   python3 scripts/generate_publications.py
   ```
5. Verify dependencies are installed (make sure virtual environment is activated):
   ```bash
   source venv/bin/activate  # macOS/Linux (if not already active)
   pip install -r requirements.txt
   ```

## File Structure

```
brains-group.github.io/
├── scripts/
│   └── generate_publications.py    # Script to generate publications page
├── docs/
│   └── PUBLICATIONS_SETUP.md       # This file
├── venv/                            # Python virtual environment (created during setup)
├── publications.qmd                 # Generated file (do not edit manually)
├── requirements.txt                 # Python dependencies
└── README.md                        # Main project README
```

**Note:** The `venv/` folder should be added to `.gitignore` if it's not already there, as virtual environments should not be committed to version control.
