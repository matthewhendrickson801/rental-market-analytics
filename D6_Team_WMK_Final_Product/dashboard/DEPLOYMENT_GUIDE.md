# Dashboard Deployment Guide

## Option 1: Render (Recommended - Easiest)

### Step 1: Prepare Your Repository

1. Make sure all files are in a Git repository:
```bash
cd d4_modeling
git init
git add .
git commit -m "Add StateofJax dashboard"
```

2. Push to GitHub:
```bash
# Create a new repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Deploy to Render

1. Go to [render.com](https://render.com) and sign up (free)

2. Click "New +" → "Web Service"

3. Connect your GitHub repository

4. Configure:
   - **Name:** stateofjax-dashboard
   - **Root Directory:** `d4_modeling/dashboard`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn duval_dashboard:server`
   - **Instance Type:** Free

5. Click "Create Web Service"

6. Wait 5-10 minutes for deployment

7. Your dashboard will be live at: `https://stateofjax-dashboard.onrender.com`

### Important Notes:
- Free tier sleeps after 15 minutes of inactivity
- First load after sleep takes ~30 seconds
- Upgrade to paid ($7/month) for always-on

---

## Option 2: Heroku

### Step 1: Install Heroku CLI
```bash
brew install heroku/brew/heroku  # macOS
# or download from heroku.com
```

### Step 2: Create Heroku App
```bash
cd d4_modeling/dashboard
heroku login
heroku create stateofjax-dashboard
```

### Step 3: Create Procfile
Create `Procfile` (no extension):
```
web: gunicorn duval_dashboard:server
```

### Step 4: Deploy
```bash
git init
git add .
git commit -m "Deploy dashboard"
heroku git:remote -a stateofjax-dashboard
git push heroku main
```

### Step 5: Open Dashboard
```bash
heroku open
```

Your dashboard will be at: `https://stateofjax-dashboard.herokuapp.com`

---

## Option 3: PythonAnywhere

### Step 1: Sign Up
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create free account

### Step 2: Upload Files
1. Go to "Files" tab
2. Upload `duval_dashboard.py`, `requirements.txt`, and data file
3. Or clone from GitHub

### Step 3: Create Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask" (Dash is Flask-based)
4. Python 3.9

### Step 4: Configure WSGI
Edit `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`:
```python
import sys
path = '/home/YOUR_USERNAME/dashboard'
if path not in sys.path:
    sys.path.append(path)

from duval_dashboard import server as application
```

### Step 5: Install Dependencies
Open Bash console:
```bash
pip install --user dash plotly pandas gunicorn
```

### Step 6: Reload
Click "Reload" button on Web tab

Your dashboard will be at: `https://YOUR_USERNAME.pythonanywhere.com`

---

## Option 4: Streamlit Cloud (Requires Conversion)

If you want to use Streamlit Cloud (easiest deployment), I can convert the Dash app to Streamlit. Let me know!

---

## Troubleshooting

### "Module not found" error
- Make sure `requirements.txt` is in the same directory
- Check that all dependencies are listed

### "Data file not found" error
- Copy `predictions_city_normalized.csv` to dashboard directory
- Update path in `duval_dashboard.py`:
```python
df = pd.read_csv('predictions_city_normalized.csv')
```

### Port binding error (Heroku/Render)
- Make sure you're using `gunicorn` in start command
- Expose `server` variable: `server = app.server`

---

## Quick Start (Render - Recommended)

1. **Push code to GitHub**
2. **Go to render.com** → Sign up
3. **New Web Service** → Connect GitHub repo
4. **Root Directory:** `d4_modeling/dashboard`
5. **Start Command:** `gunicorn duval_dashboard:server`
6. **Deploy!**

Your link will be: `https://stateofjax-dashboard.onrender.com`

---

## Need Help?

If you run into issues:
1. Check Render/Heroku logs for errors
2. Verify all files are committed to Git
3. Make sure data file is included
4. Test locally first: `python duval_dashboard.py`
