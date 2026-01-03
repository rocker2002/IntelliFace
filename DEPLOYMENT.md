# Railway Deployment Guide

## Current Status: Core App Deployment

The ML features (face recognition, image enhancement) have been temporarily disabled to resolve dependency conflicts during deployment.

## Files Modified for Deployment:

### 1. Requirements
- `requirements.txt` - Core Django dependencies only
- `requirements-minimal.txt` - Backup minimal requirements

### 2. ML Features Temporarily Disabled:
- `apps/core/recognition.py` - Face recognition functions
- `apps/core/embedding.py` - Face embedding generation
- `apps/core/enhancement.py` - Image enhancement
- `apps/core/testing.py` - Face recognition testing

### 3. Deployment Configuration:
- `runtime.txt` - Python 3.11.9
- `railway.json` - Railway deployment settings
- `nixpacks.toml` - Build configuration
- `start.sh` - Startup script

## Deployment Steps:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment - ML features disabled"
   git push origin main
   ```

2. **Deploy to Railway:**
   - Go to railway.app
   - Connect your GitHub repository
   - Railway will auto-deploy

3. **Environment Variables:**
   Set these in Railway dashboard:
   - `DATABASE_URL`: Your existing Railway database URL
   - `SECRET_KEY`: Django secret key
   - `DEBUG`: False

## After Successful Deployment:

### Re-enabling ML Features:

1. **Update requirements.txt:**
   ```
   # Add back ML dependencies
   numpy>=1.25.0,<2.0.0
   opencv-python-headless==4.9.0.80
   scikit-learn==1.4.2
   scipy==1.12.0
   insightface==0.7.3
   ```

2. **Restore ML functions:**
   - Uncomment imports in recognition.py, embedding.py, etc.
   - Restore original function implementations

3. **Redeploy:**
   ```bash
   git add .
   git commit -m "Re-enable ML features"
   git push origin main
   ```

## Current Functionality:
- ✅ Django REST API
- ✅ User authentication (JWT)
- ✅ Database operations
- ✅ Static file serving
- ❌ Face recognition (temporarily disabled)
- ❌ Image enhancement (temporarily disabled)

## Next Steps:
1. Deploy core app first
2. Verify basic functionality
3. Gradually re-enable ML features
4. Test each feature incrementally