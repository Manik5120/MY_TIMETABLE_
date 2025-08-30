# 🚀 Quick Railway Deployment Guide

## Prerequisites
- GitHub account (create at github.com if you don't have one)
- Git installed on your computer

## Method 1: Using Git Command Line

### 1. Install Git (if not installed)
- Download from: https://git-scm.com/download/win
- Install with default settings
- Restart PowerShell/Command Prompt

### 2. Run the Setup Script
Double-click `deploy_setup.bat` in your project folder

### 3. Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `my-timetable`
3. Make it **Public**
4. Don't initialize with README
5. Click "Create repository"

### 4. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/my-timetable.git
git branch -M main
git push -u origin main
```

### 5. Deploy on Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `my-timetable` repository
6. Railway will auto-deploy!

## Method 2: Using GitHub Desktop (Easier)

### 1. Install GitHub Desktop
- Download from: https://desktop.github.com/
- Sign in with your GitHub account

### 2. Create Repository
1. Open GitHub Desktop
2. File → "Add Local Repository"
3. Choose your `my-timetable` folder
4. Click "Create repository"
5. Click "Publish repository"
6. Make sure it's **Public**
7. Click "Publish repository"

### 3. Deploy on Railway
Same as Method 1, steps 5.

## After Deployment

### Add Database
1. In Railway project dashboard
2. Click "New" → "Database" → "Add PostgreSQL"
3. Database will be automatically connected

### Set Environment Variables
In Railway project → Variables tab, add:
```
DJANGO_SETTINGS_MODULE=my_timetable.settings_production
SECRET_KEY=make-this-a-long-random-string-50-characters
DEBUG=False
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

### Generate Secret Key
Run this in Python:
```python
import secrets
print(secrets.token_urlsafe(50))
```

## Your Live URL
Railway will give you a URL like:
`https://my-timetable-production.up.railway.app`

Share this with your friends! 🎉

## Troubleshooting

### Common Issues:
1. **Build fails**: Check logs in Railway dashboard
2. **Database errors**: Ensure PostgreSQL is added
3. **Static files missing**: Check if `collectstatic` runs in build
4. **Email not working**: Use Gmail app password, not regular password

### Getting Help:
- Check Railway logs in project dashboard
- Verify environment variables are set correctly
- Ensure all files are committed to Git

## What Your Friends Can Do:
- Register accounts
- Create faculties and subjects  
- Generate timetables
- Track attendance
- Manage lecture content

Enjoy your deployed timetable app! 🎓
