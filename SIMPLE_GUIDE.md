# 🎨 Simple Guide for Updating Raichuu Website

This is a simple guide for making changes to the Raichuu website without needing to know command line or Linux.

## 🚀 Quick Start

### Step 1: Open the Project
1. Open **VS Code** (or any code editor)
2. Open the folder: `/Users/rachel/Development/CattySmoothy`

### Step 2: Make Your Changes
You can edit these files to update the website:

**📄 Website Pages:**
- `templates/home.html` - Home page content
- `templates/about.html` - About page content  
- `templates/collections.html` - Collections page content

**🎨 Styling:**
- `static/css/style.css` - Colors, fonts, layout

**🖼️ Images:**
- Add images to `static/images/` folder
- Use them in HTML with: `{{ url_for('static', filename='images/your-image.jpg') }}`

### Step 3: Test Your Changes
1. Open **Terminal** (you can find it in Applications → Utilities)
2. Type these commands one by one:
   ```bash
   cd /Users/rachel/Development/CattySmoothy
   python3 app.py
   ```
3. Open your web browser and go to: `http://localhost:5001`
4. See your changes! Press `Ctrl+C` in Terminal to stop the test server

### Step 4: Publish Your Changes
1. In **VS Code**, click the **Source Control** icon (looks like a branch) in the left sidebar
2. Type a message describing your changes (like "Updated home page text")
3. Click **Commit**
4. Click **Push** (this sends your changes to GitHub)
5. Your website will automatically update at https://eclipsogate.org/ in a few minutes!

## 📝 Common Updates

### Changing Text on Home Page
1. Open `templates/home.html`
2. Find the text you want to change
3. Edit it and save the file
4. Follow Step 3 and 4 above

### Adding a New Image
1. Save your image to `static/images/` folder
2. In your HTML file, add: `<img src="{{ url_for('static', filename='images/your-image.jpg') }}" alt="Description">`
3. Follow Step 3 and 4 above

### Changing Colors or Fonts
1. Open `static/css/style.css`
2. Find the section you want to change
3. Edit the colors (like `color: blue;`) or fonts
4. Follow Step 3 and 4 above

## 🆘 Need Help?

If something doesn't work:
1. Make sure you saved all your files
2. Try the test server again (Step 3)
3. Check that you followed all the steps
4. Ask for help if you're stuck!

## 🎯 Tips

- **Always test locally first** (Step 3) before publishing
- **Save your files frequently** (Ctrl+S or Cmd+S)
- **Use descriptive commit messages** so you remember what you changed
- **Keep images small** for faster loading (under 1MB is good)

Happy creating! 🎨✨
