# Installing Quarto on macOS

## Option 1: Download Installer (Recommended)

1. Visit: https://quarto.org/docs/get-started/
2. Download the macOS installer (.pkg file)
3. Run the installer and follow the prompts
4. After installation, verify with:
   ```bash
   quarto --version
   ```

## Option 2: Using Homebrew

If you have Homebrew installed, you can install Quarto with:

```bash
brew install --cask quarto
```

## Option 3: Using Conda/Mamba

If you're using conda (which I see you have based on your terminal prompt):

```bash
conda install -c conda-forge quarto
```

## After Installation

Once Quarto is installed, you can:

1. **Preview the website locally:**
   ```bash
   quarto preview
   ```

2. **Render the website:**
   ```bash
   quarto render
   ```

3. **Check Quarto version:**
   ```bash
   quarto --version
   ```

## Troubleshooting

If `quarto` command is not found after installation:
- Close and reopen your terminal
- Or run: `source ~/.zshrc` (or `source ~/.bash_profile` if using bash)


