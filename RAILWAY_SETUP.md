# Railway Deployment Setup Guide

## 🚀 **After Deployment Succeeds:**

### 1. **Get Your Deployment URL:**
- Go to Railway Dashboard → Your App
- Look for the domain: `web-production-xxxx.up.railway.app`
- This is your live app URL!

### 2. **Add Environment Variables:**
Go to **Variables** tab and add:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
EMAIL_HOST_USER=bhagatmanik4321@gmail.com
EMAIL_HOST_PASSWORD=xvde dtop bxvq rayh
```

### 3. **Database Setup:**
- Railway automatically creates a PostgreSQL database
- The `DATABASE_URL` is automatically set
- Your app will use this database automatically

### 4. **Test Your App:**
- Visit your Railway URL
- The app should be running with PostgreSQL database
- No more crashes!

## 🔧 **If Still Having Issues:**

1. **Check Railway Logs** for specific error messages
2. **Restart the deployment** from Railway dashboard
3. **Verify environment variables** are set correctly

## 📱 **Your App Will Be Available At:**
`https://web-production-xxxx.up.railway.app`

Replace `xxxx` with your actual Railway app ID.
