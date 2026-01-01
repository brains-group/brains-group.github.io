#!/usr/bin/env python3
"""
Generate publications page for BRAINS Group website from BibTeX files.
This script reads from the shared citations.bib and bib-entries.sty files
and generates a Quarto markdown page with categorized, searchable publications.

Requirements:
    pip install bibtexparser

Or use the fallback parser (less robust but no dependencies).
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set

# Try to import bibtexparser, fall back to simple parser if not available
try:
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.customization import convert_to_unicode
    HAS_BIBTEXPARSER = True
except ImportError:
    HAS_BIBTEXPARSER = False
    print("Warning: bibtexparser not installed. Using fallback parser (may miss some entries).")
    print("Install with: pip install bibtexparser")

# Paths - adjust these to point to your CV project
# Script is in scripts/ folder, so go up one level to project root
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CV_DIR = PROJECT_ROOT.parent / "Oshani-CV"
BIB_FILE = CV_DIR / "citations.bib"
CATEGORIES_FILE = CV_DIR / "bib-entries.sty"
OUTPUT_FILE = PROJECT_ROOT / "publications.qmd"

# Category display names
CATEGORY_NAMES = {
    "thesis": "Theses",
    "books": "Books",
    "chapters": "Book Chapters",
    "journals": "Journal Articles",
    "magazines": "Magazine Articles",
    "conferences": "Conference Papers",
    "workshops": "Workshop Papers",
    "posters": "Poster Papers",
    "demos": "Demo Papers",
    "techreports": "Technical Reports",
    "patents": "Patents"
}

def parse_bib_entries_sty(file_path: Path) -> Dict[str, Set[str]]:
    """Parse bib-entries.sty to extract categories and their entries."""
    categories = defaultdict(set)
    
    if not file_path.exists():
        print(f"Warning: {file_path} not found")
        return categories
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match \addtocategory{category}{entry1, entry2, ...}
    pattern = r'\\addtocategory\{(\w+)\}\s*\{([^}]+)\}'
    
    for match in re.finditer(pattern, content):
        category = match.group(1)
        entries_str = match.group(2)
        # Extract entry keys (remove whitespace, split by comma)
        entries = [e.strip() for e in entries_str.split(',') if e.strip()]
        categories[category].update(entries)
    
    return categories

def extract_braced_content(text: str, start_pos: int = 0) -> tuple:
    """Extract content within braces, handling nested braces."""
    if start_pos >= len(text) or text[start_pos] != '{':
        return None, start_pos
    
    pos = start_pos + 1
    depth = 1
    content_start = pos
    
    while pos < len(text) and depth > 0:
        if text[pos] == '{':
            depth += 1
        elif text[pos] == '}':
            depth -= 1
        pos += 1
    
    if depth == 0:
        return text[content_start:pos-1], pos
    return None, start_pos

def parse_bibtex(file_path: Path) -> Dict[str, Dict]:
    """Parse BibTeX file and extract entries."""
    entries = {}
    
    if not file_path.exists():
        print(f"Warning: {file_path} not found")
        return entries
    
    if HAS_BIBTEXPARSER:
        # Use bibtexparser for robust parsing
        with open(file_path, 'r', encoding='utf-8') as bibtex_file:
            parser = BibTexParser()
            parser.customization = convert_to_unicode
            parser.ignore_nonstandard_types = False
            bib_database = bibtexparser.load(bibtex_file, parser=parser)
        
        for entry in bib_database.entries:
            entry_key = entry.get('ID', '')
            entry_type = entry.get('ENTRYTYPE', '').lower()
            
            # Extract year
            year_str = entry.get('year', '').strip()
            try:
                year_int = int(year_str) if year_str else 0
            except ValueError:
                year_int = 0
            
            # Only include publications from 2022 onwards
            if year_int >= 2022:
                entries[entry_key] = {
                    'type': entry_type,
                    'key': entry_key,
                    'year': year_int,
                    'fields': entry
                }
    else:
        # Fallback simple parser
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments
        content = re.sub(r'%.*$', '', content, flags=re.MULTILINE)
        
        # Find all @ entries
        entry_pattern = r'@(\w+)\{([^,]+),([^@]*?)(?=@|\Z)'
        
        for match in re.finditer(entry_pattern, content, re.DOTALL):
            entry_type = match.group(1).lower()
            entry_key = match.group(2).strip()
            fields_str = match.group(3)
            
            # Parse fields
            fields = {}
            field_patterns = [
                r'(\w+)\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',
                r'(\w+)\s*=\s*"([^"]*)"',
                r'(\w+)\s*=\s*(\d+)',
            ]
            
            for pattern in field_patterns:
                for field_match in re.finditer(pattern, fields_str):
                    field_name = field_match.group(1).lower()
                    field_value = field_match.group(2)
                    field_value = re.sub(r'\{([^}]+)\}', r'\1', field_value)
                    fields[field_name] = field_value.strip()
            
            # Extract year
            year = fields.get('year', '').strip()
            try:
                year_int = int(year) if year else 0
            except ValueError:
                year_int = 0
            
            if year_int >= 2022:
                entries[entry_key] = {
                    'type': entry_type,
                    'key': entry_key,
                    'year': year_int,
                    'fields': fields
                }
    
    return entries

def format_authors(authors_str: str) -> str:
    """Format author string for display."""
    if not authors_str:
        return ""
    # Handle "and" separators
    authors = [a.strip() for a in authors_str.split(' and ')]
    if len(authors) == 1:
        return authors[0]
    elif len(authors) == 2:
        return f"{authors[0]} and {authors[1]}"
    elif len(authors) <= 4:
        return ", ".join(authors[:-1]) + f", and {authors[-1]}"
    else:
        return ", ".join(authors[:3]) + ", et al."

def format_publication(entry: Dict, category: str) -> str:
    """Format a single publication entry for display."""
    fields = entry['fields']
    entry_type = entry['type']
    key = entry['key']
    
    # Extract fields
    title = fields.get('title', '').strip()
    # Remove extra braces from title
    title = re.sub(r'\{([^}]+)\}', r'\1', title)
    
    authors = format_authors(fields.get('author', ''))
    year = entry['year']
    
    # Build citation based on type
    citation_parts = []
    
    if authors:
        citation_parts.append(f"**{authors}**")
    
    if title:
        citation_parts.append(f"*{title}*")
    
    # Add venue information based on entry type
    if entry_type == 'inproceedings':
        booktitle = fields.get('booktitle', '').strip()
        if booktitle:
            citation_parts.append(f"In {booktitle}")
    elif entry_type == 'article':
        journal = fields.get('journal', '').strip()
        if journal:
            citation_parts.append(f"In *{journal}*")
    elif entry_type == 'inbook' or entry_type == 'incollection':
        booktitle = fields.get('booktitle', '').strip()
        if booktitle:
            citation_parts.append(f"In {booktitle}")
    
    # Add year
    citation_parts.append(f"({year})")
    
    # Add links
    links = []
    if 'url' in fields:
        url = fields['url'].strip()
        links.append(f"[PDF]({url})")
    if 'doi' in fields:
        doi = fields['doi'].strip()
        links.append(f"[DOI](https://doi.org/{doi})")
    
    citation = ". ".join(citation_parts)
    
    if links:
        citation += " " + " | ".join(links)
    
    return f"- {citation}"

def generate_publications_page(entries: Dict, categories: Dict[str, Set[str]]) -> str:
    """Generate the Quarto markdown page."""
    
    # Organize entries by category
    categorized = defaultdict(list)
    uncategorized = []
    
    for key, entry in entries.items():
        found = False
        for cat, keys in categories.items():
            if key in keys:
                categorized[cat].append(entry)
                found = True
                break
        if not found:
            uncategorized.append(entry)
    
    # Sort entries within each category by year (descending)
    for cat in categorized:
        categorized[cat].sort(key=lambda x: x['year'], reverse=True)
    
    # Generate markdown
    # Note: The intro section (heading, description, callout) is NOT auto-generated
    # so it can be manually edited. The script only generates the search box and publication lists.
    lines = [
        "---",
        "title: \"Publications\"",
        "---",
        "",
        "```{=html}",
        "<div style='margin: 2rem 0;'>",
        "<input type='text' id='pubSearch' placeholder='Search publications...' ",
        "       style='width: 100%; padding: 0.75rem; font-size: 1rem; border: 2px solid #ddd; border-radius: 8px;' />",
        "</div>",
        "```",
        "",
        "```{=html}",
        "<div id='publications-container'>",
        "```",
        ""
    ]
    
    # Add publications by category
    category_order = ["books", "chapters", "journals", "conferences", "workshops", 
                      "techreports", "posters", "demos", "thesis", "magazines", "patents"]
    
    for cat in category_order:
        if cat in categorized and categorized[cat]:
            cat_name = CATEGORY_NAMES.get(cat, cat.title())
            lines.append(f"### {cat_name}")
            lines.append("")
            lines.append("```{=html}")
            lines.append(f"<div class='pub-category' data-category='{cat}'>")
            lines.append("```")
            lines.append("")
            for entry in categorized[cat]:
                lines.append(format_publication(entry, cat))
                lines.append("")
            lines.append("```{=html}")
            lines.append("</div>")
            lines.append("```")
            lines.append("")
    
    # Add uncategorized if any
    if uncategorized:
        lines.append("### Other Publications")
        lines.append("")
        lines.append("```{=html}")
        lines.append("<div class='pub-category' data-category='other'>")
        lines.append("```")
        lines.append("")
        for entry in sorted(uncategorized, key=lambda x: x['year'], reverse=True):
            lines.append(format_publication(entry, "other"))
            lines.append("")
        lines.append("```{=html}")
        lines.append("</div>")
        lines.append("```")
        lines.append("")
    
    # Close container and add search script
    lines.extend([
        "```{=html}",
        "</div>",
        "```",
        "",
        "```{=html}",
        "<script>",
        "document.addEventListener('DOMContentLoaded', function() {",
        "  const searchInput = document.getElementById('pubSearch');",
        "  const categories = document.querySelectorAll('.pub-category');",
        "",
        "  searchInput.addEventListener('input', function(e) {",
        "    const searchTerm = e.target.value.toLowerCase();",
        "",
        "    categories.forEach(category => {",
        "      const items = category.querySelectorAll('li');",
        "      let hasVisible = false;",
        "",
        "      items.forEach(item => {",
        "        const text = item.textContent.toLowerCase();",
        "        if (text.includes(searchTerm)) {",
        "          item.style.display = '';",
        "          hasVisible = true;",
        "        } else {",
        "          item.style.display = 'none';",
        "        }",
        "      });",
        "",
        "      // Hide category if no visible items",
        "      const categoryHeading = category.previousElementSibling;",
        "      if (categoryHeading && categoryHeading.tagName === 'H3') {",
        "        if (hasVisible || searchTerm === '') {",
        "          categoryHeading.style.display = '';",
        "          category.style.display = '';",
        "        } else {",
        "          categoryHeading.style.display = 'none';",
        "          category.style.display = 'none';",
        "        }",
        "      }",
        "    });",
        "  });",
        "});",
        "</script>",
        "```"
    ])
    
    return "\n".join(lines)

def main():
    """Main function."""
    print("Parsing bibliography files...")
    
    # Parse files
    categories = parse_bib_entries_sty(CATEGORIES_FILE)
    entries = parse_bibtex(BIB_FILE)
    
    print(f"Found {len(entries)} publications from 2022 onwards")
    print(f"Found {len(categories)} categories")
    
    # Generate page
    print("Generating publications page...")
    content = generate_publications_page(entries, categories)
    
    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Generated {OUTPUT_FILE}")
    print("Done! You can now render the site with 'quarto render'")

if __name__ == "__main__":
    main()

