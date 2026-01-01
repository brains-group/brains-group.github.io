# BRAINS Research Group Website

Website for the BRAINS (Bridging Resilient Accountable Intelligent Networked Systems) Research Group at RPI.

## Building the Website

This website is built using [Quarto](https://quarto.org/).

### Prerequisites

Install Quarto from [https://quarto.org/docs/get-started/](https://quarto.org/docs/get-started/)

### Local Development

To preview the website locally:

```bash
quarto preview
```

### Building for Production

To build the website:

```bash
quarto render
```

The output will be in the `_site/` directory.

## GitHub Pages Deployment

This repository is configured to be hosted on GitHub Pages at `brains-group.github.io`.

### Setup Instructions

1. Go to your repository settings on GitHub
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "GitHub Actions" (or "Deploy from a branch" and choose the `main` branch with `/docs` folder)
4. If using GitHub Actions, create a workflow file (see below)

### GitHub Actions Workflow

Create `.github/workflows/publish.yml`:

```yaml
name: Publish Website

on:
  push:
    branches: main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: quarto-dev/quarto-actions/setup@v2
      - run: quarto render
      - uses: actions/upload-pages-artifact@v2
        with:
          path: _site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v2
```

## Adding Content

- **Homepage**: Edit `index.qmd`
- **About**: Edit `about.qmd`
- **Projects**: Edit `projects.qmd`
- **People**: Edit `people.qmd`
- **News**: Edit `news.qmd`
- **Publications**: Edit `publications.qmd` (will integrate with BibTeX)
- **Alumni**: Edit `alumni.qmd`

## Customization

- Website configuration: `_quarto.yml`
- Custom styles: `styles.css`


