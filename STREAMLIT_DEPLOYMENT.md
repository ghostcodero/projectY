# Streamlit Cloud Deployment Guide

## Quick Setup for Streamlit Cloud

### 1. Push Your Code to GitHub
Make sure your repository is up to date on GitHub with all the latest changes.

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `ghostcodero/projectY`
5. Set the main file path: `streamlit_app.py`
6. Click "Deploy!"

### 3. Set Environment Variables

**IMPORTANT:** You must set environment variables before the app will work!

1. In your deployed app, click "Manage app" (bottom right)
2. Go to "Settings" tab
3. Scroll down to "Secrets"
4. Add your API keys in this format:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"
PERPLEXITY_API_KEY = "your_perplexity_api_key_here"
```

### 4. Restart the App

After setting the environment variables:
1. Go back to "Main" tab
2. Click "Redeploy" button
3. Wait for the app to restart

## Important Notes

### YouTube Functionality Limitation
- **YouTube video analysis may not work** due to missing FFmpeg in Streamlit Cloud
- **Recommended alternatives:**
  - Use "Upload Transcript" to upload a text file
  - Use "Paste Transcript" to copy/paste transcript text
- These alternatives work reliably in all environments

### Working Features
✅ **Transcript Upload** - Upload .txt files  
✅ **Paste Transcript** - Copy/paste text directly  
✅ **Prediction Analysis** - Full analysis functionality  
✅ **Results Download** - Export analysis results  
⚠️ **YouTube Download** - May not work due to FFmpeg dependency  

## Troubleshooting

### Common Issues:

1. **"API Keys Not Found" Error**
   - Make sure you've set both environment variables in Streamlit Cloud
   - Check that the variable names are exactly correct (case-sensitive)
   - Redeploy after setting variables

2. **"ffprobe and ffmpeg not found" Error**
   - This is expected for YouTube downloads
   - Use "Upload Transcript" or "Paste Transcript" instead
   - These methods work without FFmpeg

3. **Import Errors**
   - Make sure all dependencies are in `requirements.txt`
   - Check that the main file path is correct (`streamlit_app.py`)

### Cost Control:

- The app includes rate limiting (10 requests/day per session)
- Monitor your API usage in OpenAI and Perplexity dashboards
- Set spending limits in your API accounts

## Security Notes:

- Never commit API keys to your repository
- Use Streamlit Cloud's secrets management
- The app validates environment variables before running

## Support:

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Verify environment variables are set correctly
3. Test locally first with `streamlit run streamlit_app.py`
4. Use transcript upload/paste methods for reliable functionality 