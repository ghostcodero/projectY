# ProjectY Streamlit Deployment Guide

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export OPENAI_API_KEY="your_openai_api_key"
export PERPLEXITY_API_KEY="your_perplexity_api_key"
```

3. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

4. Open your browser and go to `http://localhost:8501`

## Deployment Options

### Option 1: Streamlit Cloud (Recommended for beginners)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Select your repository
5. Set the main file path to `streamlit_app.py`
6. Add your environment variables in the Streamlit Cloud dashboard
7. Deploy!

### Option 2: Heroku

1. Create a `Procfile`:
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

3. Deploy to Heroku:
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY="your_openai_api_key"
heroku config:set PERPLEXITY_API_KEY="your_perplexity_api_key"
git push heroku main
```

### Option 3: Docker

1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Build and run:
```bash
docker build -t projecty-streamlit .
docker run -p 8501:8501 -e OPENAI_API_KEY="your_key" -e PERPLEXITY_API_KEY="your_key" projecty-streamlit
```

## Environment Variables

Make sure to set these environment variables in your deployment platform:

- `OPENAI_API_KEY`: Your OpenAI API key
- `PERPLEXITY_API_KEY`: Your Perplexity API key

## Troubleshooting

### Common Issues:

1. **FFmpeg not found**: Make sure FFmpeg is installed on your deployment platform
2. **API key errors**: Verify environment variables are set correctly
3. **Memory issues**: Consider upgrading your deployment plan for larger files
4. **Timeout errors**: Some operations may take time, consider implementing progress indicators

### Performance Tips:

1. Use caching for expensive operations
2. Implement proper error handling
3. Consider using background tasks for long-running operations
4. Monitor memory usage and optimize accordingly 