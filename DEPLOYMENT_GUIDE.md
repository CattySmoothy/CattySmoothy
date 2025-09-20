# 🚀 Raichuu Website Deployment Guide

This guide explains how to set up automatic deployment for the Raichuu website so that changes made locally are automatically pushed to the live site at https://eclipsogate.org/.

## 📋 Setup Instructions

### 1. Server Setup

Your server needs to have the repository cloned and be ready to receive updates:

1. **SSH into your server and ensure the repository is cloned:**
   ```bash
   ssh rachel@eclipsogate.org
   cd /home/rachel/eclipsogate.org/CattySmoothy
   git pull origin main  # Make sure you have the latest code
   ```

2. **Update the GitHub Actions workflow file:**
   - Edit `.github/workflows/deploy.yml` 
   - The paths are already configured for your server setup
   - Update `your-flask-app` to match your actual systemctl service name

### 2. GitHub Actions Setup (Recommended)

For automatic deployment when code is pushed to GitHub:

1. **Go to your GitHub repository:** https://github.com/CattySmoothy/CattySmoothy

2. **Add secrets to your repository:**
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret" and add these secrets:
     - `HOST`: Your server's IP address or domain (e.g., `eclipsogate.org`)
     - `USERNAME`: Your server username
     - `SSH_KEY`: Your private SSH key content (the entire content of your `~/.ssh/id_rsa` file)

3. **Generate SSH key pair (if you don't have one):**
   ```bash
   ssh-keygen -t rsa -b 4096 -C "github-actions@eclipsogate.org"
   # Copy the public key to your server
   ssh-copy-id your-username@eclipsogate.org
   ```

4. **Update the workflow file:**
   - Edit `.github/workflows/deploy.yml`
   - Change `/path/to/your/website/directory` to your actual website directory
   - Update the web server restart commands based on your setup

### 3. Alternative: Manual Deployment

If you prefer to keep your current manual process:

1. **Your daughter pushes code to GitHub**
2. **You SSH into your server and deploy manually:**
   ```bash
   ssh rachel@eclipsogate.org
   cd /home/rachel/eclipsogate.org/CattySmoothy
   git pull origin main
   /home/rachel/eclipsogate.org/CattySmoothy/.env/.venv/bin/pip install -r requirements.txt
   sudo systemctl restart your-flask-app
   ```

3. **Or set up a simple cron job for automatic pulling:**
   ```bash
   # Add to crontab: crontab -e
   */5 * * * * cd /home/rachel/eclipsogate.org/CattySmoothy && git pull origin main
   ```

## 🎯 How to Use (For Your Daughter)

### Making Changes Locally

1. **Open the project in your code editor** (VS Code, etc.)

2. **Make your changes:**
   - Edit HTML files in `templates/` folder
   - Edit CSS in `static/css/style.css`
   - Add images to `static/images/`

3. **Test locally:**
   ```bash
   cd /Users/rachel/Development/CattySmoothy
   python3 app.py
   ```
   - Visit http://localhost:5001 to see your changes

4. **Commit and push changes:**
   ```bash
   git add .
   git commit -m "Describe your changes"
   git push origin main
   ```

5. **Automatic deployment:**
   - If GitHub Actions is set up, the site will update automatically
   - If using manual deployment, you'll need to SSH and run `git pull` on the server
   - If using cron job, the server will pull changes automatically every 5 minutes

### Common Tasks

**Adding a new page:**
1. Create new HTML file in `templates/`
2. Add route in `routes.py`
3. Add navigation link in `templates/base.html`

**Updating content:**
1. Edit the relevant HTML file in `templates/`
2. Commit and push changes

**Adding images:**
1. Add image files to `static/images/`
2. Reference them in HTML: `{{ url_for('static', filename='images/your-image.jpg') }}`

## 🔧 Troubleshooting

**If deployment fails:**
1. Check the GitHub Actions logs (if using GitHub Actions):
   - Go to your repository → Actions tab
   - Click on the failed workflow run to see detailed logs
2. SSH into your server and run `git pull origin main` manually
3. Check server logs for any errors
4. Verify SSH key permissions and GitHub secrets are correct

**If changes don't appear:**
1. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
2. Check if the web server restarted properly
3. Verify the files were pulled correctly on the server
4. Check if GitHub Actions workflow completed successfully

**Common issues:**
- **SSH connection fails**: Verify your SSH key is correct and added to GitHub secrets
- **Permission denied**: Make sure the SSH key has proper permissions on your server
- **Path not found**: Update the paths in the workflow file to match your server setup
- **Web server not restarting**: Update the restart command in the workflow file

## 📞 Support

If you need help with any of these steps, the deployment can also be done manually by SSH'ing into the server and running:
```bash
cd /home/rachel/eclipsogate.org/CattySmoothy
git pull origin main
/home/rachel/eclipsogate.org/CattySmoothy/.env/.venv/bin/pip install -r requirements.txt
sudo systemctl restart your-flask-app
```

## 🎯 Summary

**Recommended approach:**
1. Set up GitHub Actions with SSH secrets
2. Your daughter pushes code to GitHub
3. GitHub Actions automatically deploys to your server
4. Website updates automatically at https://eclipsogate.org/

**Simple approach:**
1. Your daughter pushes code to GitHub
2. You SSH into server and run `git pull origin main`
3. Restart your web server
4. Website updates
