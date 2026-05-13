# Render Deployment Guide for Crime Rate Prediction Project

## ✅ Pre-Deployment Checklist - COMPLETED

- [x] Updated `app.py` to use PORT environment variable
- [x] Changed debug mode to False
- [x] Set host to '0.0.0.0' for external connections
- [x] Updated `requirements.txt` with gunicorn and all dependencies
- [x] Created `Procfile` for deployment configuration
- [x] Created `runtime.txt` specifying Python version
- [x] Created `.gitignore` file

---

## 📋 Step-by-Step Deployment Instructions

### **Step 1: Prepare Your GitHub Repository**

1. Open Git Bash or PowerShell in your project directory
2. Initialize a Git repository (if not already done):
   ```bash
   git init
   ```
3. Add all files:
   ```bash
   git add .
   ```
4. Create your first commit:
   ```bash
   git commit -m "Initial commit: Crime Rate Prediction App"
   ```
5. Create a GitHub repository at https://github.com/new
6. Push your code to GitHub:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

### **Step 2: Create a Render Account**

1. Go to https://render.com
2. Click "Sign Up" and create an account (you can use GitHub to sign up)
3. Verify your email

### **Step 3: Deploy on Render**

1. Log in to Render Dashboard
2. Click **"New +"** button → **"Web Service"**
3. Select **"Build and deploy from a Git repository"**
4. Click **"Connect your GitHub account"** and authorize Render
5. Select your repository from the list
6. Fill in the deployment settings:
   - **Name:** `crime-rate-prediction` (or your preferred name)
   - **Environment:** `Python 3`
   - **Region:** Choose closest to your users (e.g., Ohio for US)
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app` (should auto-fill from Procfile)
   - **Instance Type:** `Free` (or Paid if needed)

7. Click **"Create Web Service"**

### **Step 4: Monitor Deployment**

1. Render will automatically build and deploy your app
2. Check the "Logs" tab to see build progress
3. Wait for the message: **"Your service is live!"**
4. Your app will be available at: `https://YOUR-APP-NAME.onrender.com`

### **Step 5: Test Your Deployed App**

1. Visit your Render URL
2. Test predictions to ensure everything works
3. If there are errors, check the logs in Render dashboard

---

## 🚨 Important Notes

### **Free Tier Limitations:**
- Auto-spins down after 15 minutes of inactivity (~30 sec startup delay)
- Limited to 512MB RAM memory
- Monthly reset on free databases
- Good for testing/demo purposes

### **To Upgrade to Paid:**
1. Go to your service settings
2. Choose **"Paid"** instance
3. Instant startup and 24/7 uptime

### **Data Persistence Issues:**
- The `static/prediction_graph.png` will be recreated each time
- The trained models (`.pkl` files) persist in the repository
- For production, consider using Render's databases or AWS S3

### **Troubleshooting Common Issues:**

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Check `requirements.txt` has all dependencies |
| Port error | Don't hardcode port; use `os.environ.get('PORT')` ✅ (Fixed) |
| Debug mode error | Set `debug=False` in production ✅ (Fixed) |
| Host binding error | Use `host='0.0.0.0'` ✅ (Fixed) |
| Long startup time | Upgrade to paid instance |
| Missing files | Commit all files to Git before pushing |

### **Environment Variables (if needed later):**
1. Go to your Render service
2. Click **"Environment"**
3. Add any needed variables (API keys, secrets, etc.)
4. Service auto-restarts

---

## 📁 Final Project Structure

```
├── app.py                          ✅ Updated with PORT binding
├── train.py                        (No changes needed)
├── requirements.txt                ✅ Updated with gunicorn
├── Procfile                        ✅ CREATED
├── runtime.txt                     ✅ CREATED
├── .gitignore                      ✅ CREATED
├── data/
│   ├── crime_data.csv
│   └── future_predictions.csv
├── models/
│   └── rf_model.joblib
├── static/
│   ├── app.js
│   ├── style.css
│   └── prediction_graph.png        (Generated at runtime)
└── templates/
    └── index.html
```

---

## 🔄 Future Updates

To update your deployed app:
1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. Render automatically redeploys (watch in Dashboard)

---

## 📞 Support

- **Render Docs:** https://render.com/docs
- **Flask Deployment:** https://flask.palletsprojects.com/deployment/
- **Gunicorn Docs:** https://docs.gunicorn.org/

---

**✨ Your app is now ready to deploy! Follow Steps 1-5 above to go live.** 🚀
