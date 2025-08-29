# 🚀 Django Timetable Deployment Guide

This guide will help you deploy your Django timetable application on free hosting services so you can share it with your friends via a public URL.

## 📋 Table of Contents
1. [Railway (Recommended)](#-railway-recommended)
2. [Render](#-render)
3. [Heroku](#-heroku)
4. [Pre-deployment Checklist](#-pre-deployment-checklist)
5. [Post-deployment Setup](#-post-deployment-setup)
6. [Environment Variables](#-environment-variables)

---

## 🚂 Railway (Recommended)

Railway is the easiest and most reliable free option for Django deployment.

### Prerequisites
- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))

### Steps

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/my-timetable.git
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `my-timetable` repository
   - Railway will automatically detect it's a Python project

3. **Add Database**
   - In your Railway project dashboard
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway will automatically set the `DATABASE_URL` environment variable

4. **Set Environment Variables**
   Go to your project → Variables tab and add:
   ```
   DJANGO_SETTINGS_MODULE=my_timetable.settings_production
   SECRET_KEY=your-very-secret-key-here-make-it-long-and-random
   DEBUG=False
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-gmail-app-password
   ```

5. **Deploy**
   - Railway will automatically deploy your app
   - You'll get a URL like: `https://my-timetable-production.up.railway.app`

---

## 🎨 Render

Render offers 750 hours/month free tier.

### Steps

1. **Push code to GitHub** (same as Railway step 1)

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Name**: my-timetable
     - **Environment**: Python 3
     - **Build Command**: `cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput`
     - **Start Command**: `cd backend && python manage.py migrate && python manage.py create_timeslots && gunicorn my_timetable.wsgi:application`

3. **Add Database**
   - Go to Dashboard → "New" → "PostgreSQL"
   - Create database
   - Copy the "Internal Database URL"

4. **Set Environment Variables**
   In your web service → Environment tab:
   ```
   DJANGO_SETTINGS_MODULE=my_timetable.settings_production
   SECRET_KEY=your-very-secret-key-here
   DEBUG=False
   DATABASE_URL=your-postgres-url-from-step-3
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-gmail-app-password
   ```

---

## 🟪 Heroku

Heroku requires a credit card for verification but doesn't charge for basic usage.

### Steps

1. **Install Heroku CLI**
   Download from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-timetable-app-name
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set DJANGO_SETTINGS_MODULE=my_timetable.settings_production
   heroku config:set SECRET_KEY=your-very-secret-key-here
   heroku config:set DEBUG=False
   heroku config:set EMAIL_HOST_USER=your-email@gmail.com
   heroku config:set EMAIL_HOST_PASSWORD=your-gmail-app-password
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

---

## ✅ Pre-deployment Checklist

Before deploying, make sure you have:

- [ ] Updated `requirements.txt` with all dependencies
- [ ] Created production settings (`settings_production.py`)
- [ ] Set up environment variables template (`env.example`)
- [ ] Added deployment configuration files (`railway.toml`, `Procfile`, etc.)
- [ ] Committed all changes to Git
- [ ] Created a GitHub repository

---

## 🔧 Post-deployment Setup

After your app is deployed:

1. **Create Superuser**
   - Railway: Use the Railway CLI or web terminal
   - Render: Use the web shell in dashboard
   - Heroku: `heroku run python backend/manage.py createsuperuser`

2. **Access Admin Panel**
   - Go to `https://your-app-url/admin/`
   - Login with superuser credentials
   - Add some test data (faculties, subjects, etc.)

3. **Test the Application**
   - Register a new user
   - Create some faculties and subjects
   - Generate a timetable
   - Test all features

---

## 🔐 Environment Variables

### Required Variables
- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DEBUG`: Set to `False` for production
- `DATABASE_URL`: Automatically set by hosting services
- `DJANGO_SETTINGS_MODULE`: Set to `my_timetable.settings_production`

### Optional Variables
- `EMAIL_HOST_USER`: Your Gmail address for password reset emails
- `EMAIL_HOST_PASSWORD`: Gmail app password (not your regular password)
- `ALLOWED_HOST`: Your custom domain if you have one

### How to Generate a Secret Key
```python
import secrets
print(secrets.token_urlsafe(50))
```

---

## 🎉 Sharing Your App

Once deployed, you can share your app URL with friends:

- **Railway**: `https://your-project.up.railway.app`
- **Render**: `https://your-app-name.onrender.com`
- **Heroku**: `https://your-app-name.herokuapp.com`

### Sample User Guide for Friends

Send this to your friends:

```
🎓 Welcome to My Timetable App!

1. Visit: [YOUR_APP_URL]
2. Click "Register" to create an account
3. Login with your credentials
4. Start by adding faculties and subjects
5. Set faculty availability
6. Generate your timetable!

Features:
✅ Create and manage timetables
✅ Track attendance
✅ Manage lecture content
✅ Faculty availability management
✅ Password reset via email

Need help? Contact me at [your-email]
```

---

## 🐛 Troubleshooting

### Common Issues

1. **Static files not loading**
   - Check `STATIC_ROOT` and `STATICFILES_DIRS` in settings
   - Run `python manage.py collectstatic` locally to test

2. **Database connection errors**
   - Verify `DATABASE_URL` environment variable
   - Check if database service is running

3. **Email not working**
   - Verify Gmail app password (not regular password)
   - Check Gmail settings allow less secure apps

4. **Internal Server Error (500)**
   - Check application logs in hosting service dashboard
   - Verify all environment variables are set correctly

### Getting Help

- Railway: Check logs in project dashboard
- Render: Check logs in web service dashboard  
- Heroku: Use `heroku logs --tail`

---

## 📝 Notes

- **Railway** is recommended for beginners (easiest setup)
- **Render** has good free tier limits
- **Heroku** requires credit card but offers good documentation
- All these services provide HTTPS by default
- Free tiers may have some limitations (sleep after inactivity, etc.)

Choose the platform that best fits your needs and comfort level. Railway is generally the easiest to get started with!
