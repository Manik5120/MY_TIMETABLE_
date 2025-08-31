# Render Deployment Guide for Timetable Management System

## 🚀 **Deploy to Render (Recommended)**

Render is a modern cloud platform that's very reliable for Django applications and doesn't have the redirect loop issues we experienced with Railway.

### **Step 1: Prepare Your Repository**

1. **Push your code to GitHub** (if not already done)
2. **Make sure all changes are committed**

### **Step 2: Deploy to Render**

1. **Go to [render.com](https://render.com)** and sign up/login
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**

   **Name:** `mytimetable`
   
   **Environment:** `Python 3`
   
   **Build Command:** `pip install -r requirements.txt`
   
   **Start Command:** 
   ```
   cd backend && python manage.py migrate --settings=my_timetable.settings_render && python manage.py create_timeslots --settings=my_timetable.settings_render && python manage.py collectstatic --noinput --settings=my_timetable.settings_render && gunicorn --bind 0.0.0.0:$PORT my_timetable.wsgi:application --env DJANGO_SETTINGS_MODULE=my_timetable.settings_render
   ```

### **Step 3: Add Environment Variables**

In Render dashboard, go to **Environment** tab and add:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
EMAIL_HOST_USER=bhagatmanik4321@gmail.com
EMAIL_HOST_PASSWORD=xvde dtop bxvq rayh
```

### **Step 4: Add Database**

1. **Click "New +" → "PostgreSQL"**
2. **Name:** `mytimetable-db`
3. **Plan:** Free
4. **Copy the DATABASE_URL** from the database settings
5. **Add it to your web service environment variables**

### **Step 5: Deploy**

1. **Click "Create Web Service"**
2. **Wait for deployment** (5-10 minutes)
3. **Your app will be available at:** `https://your-app-name.onrender.com`

## ✅ **Why Render is Better**

- **No redirect loop issues** - Better handling of Django authentication
- **More reliable** - Stable platform for Django apps
- **Free tier** - Generous free plan
- **Auto-deploy** - Automatic deployments from GitHub
- **Better logs** - Clearer error messages

## 🔧 **Troubleshooting**

If you encounter issues:

1. **Check Render logs** in the dashboard
2. **Verify environment variables** are set correctly
3. **Ensure database is connected** properly
4. **Check static files** are being collected

## 📱 **Your App URL**

After deployment, your app will be available at:
`https://your-app-name.onrender.com`

Replace `your-app-name` with the actual name you chose during setup.

## 🎉 **Success!**

Your Timetable Management System will be live and working without redirect loops!
