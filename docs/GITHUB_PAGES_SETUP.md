# GitHub Pages Setup Instructions

## Step 1: Configure GitHub Pages Settings

1. Go to your repository on GitHub: `https://github.com/brains-group/brains-group.github.io`
2. Click on **Settings** (in the repository menu)
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select **GitHub Actions** (NOT "Deploy from a branch")
5. Save the settings

## Step 2: Verify the Workflow

1. Go to the **Actions** tab in your repository
2. You should see a workflow run after you push to the `main` branch
3. If there's no workflow run, you can manually trigger it:
   - Go to **Actions** tab
   - Click on **Publish Website** workflow
   - Click **Run workflow** button

## Step 3: Check Deployment Status

1. In the **Actions** tab, click on the latest workflow run
2. Make sure both jobs (`build` and `deploy`) complete successfully
3. Once deployed, your site should be available at `https://brains-group.github.io/`

## Troubleshooting

### If you still see the README:

1. **Clear browser cache** - GitHub Pages can be cached
2. **Check the Actions tab** - Make sure the workflow ran successfully
3. **Verify Pages source** - Make sure it's set to "GitHub Actions", not "Deploy from a branch"
4. **Wait a few minutes** - GitHub Pages can take 1-2 minutes to update after deployment

### If the workflow fails:

1. Check the error messages in the Actions tab
2. Make sure all required files are committed and pushed
3. Verify that `_quarto.yml` and `index.qmd` are in the repository

## Manual Deployment (Alternative)

If GitHub Actions isn't working, you can manually build and deploy:

```bash
# Build the site locally
quarto render

# Then push the _site directory to a gh-pages branch
# (This requires additional setup)
```

But GitHub Actions is the recommended approach for automatic deployments.

