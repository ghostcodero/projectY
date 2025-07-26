import streamlit as st
import os
import tempfile
from pathlib import Path
import time
from datetime import datetime, timedelta
import json

# Check environment variables first before importing modules
if not os.getenv('OPENAI_API_KEY') or not os.getenv('PERPLEXITY_API_KEY'):
    st.error("""
    ❌ **API Keys Not Found!**
    
    Please set the following environment variables:
    - `OPENAI_API_KEY`
    - `PERPLEXITY_API_KEY`
    
    Contact the administrator if you need access.
    """)
    st.stop()

# Import your existing modules only after environment check
from projectY_modules import downloader
from projectY_modules import transcriber
from projectY_modules import prediction_extractor
from projectY_modules import prediction_verifier
from projectY_modules import narrative_generator

# Configure page
st.set_page_config(
    page_title="ProjectY - Prediction Analysis Tool",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Rate limiting and usage tracking
def load_usage_data():
    """Load usage data from session state or file"""
    if 'usage_data' not in st.session_state:
        st.session_state.usage_data = {
            'daily_requests': 0,
            'last_reset': datetime.now().strftime('%Y-%m-%d'),
            'total_requests': 0,
            'last_request_time': None
        }
    return st.session_state.usage_data

def check_rate_limit():
    """Check if user has exceeded rate limits"""
    usage = load_usage_data()
    now = datetime.now()
    
    # Reset daily counter if it's a new day
    if usage['last_reset'] != now.strftime('%Y-%m-%d'):
        usage['daily_requests'] = 0
        usage['last_reset'] = now.strftime('%Y-%m-%d')
    
    # Check daily limit (adjust as needed)
    DAILY_LIMIT = 10  # Maximum requests per day
    if usage['daily_requests'] >= DAILY_LIMIT:
        return False, f"Daily limit of {DAILY_LIMIT} requests reached. Please try again tomorrow."
    
    # Check time between requests (minimum 30 seconds)
    if usage['last_request_time']:
        last_request = datetime.fromisoformat(usage['last_request_time'])
        if (now - last_request).total_seconds() < 30:
            return False, "Please wait 30 seconds between requests."
    
    return True, ""

def update_usage():
    """Update usage statistics"""
    usage = load_usage_data()
    usage['daily_requests'] += 1
    usage['total_requests'] += 1
    usage['last_request_time'] = datetime.now().isoformat()
    st.session_state.usage_data = usage

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 ProjectY</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem;">Analyze and verify predictions from YouTube videos or transcripts</p>', unsafe_allow_html=True)
    
    # Usage information
    usage = load_usage_data()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Daily Requests", f"{usage['daily_requests']}/10")
    with col2:
        st.metric("Total Requests", usage['total_requests'])
    with col3:
        if usage['last_request_time']:
            last_time = datetime.fromisoformat(usage['last_request_time'])
            st.metric("Last Request", last_time.strftime('%H:%M:%S'))
    
    # Rate limit warning
    if usage['daily_requests'] >= 8:
        st.warning("⚠️ You're approaching the daily limit of 10 requests!")
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown('<h3 class="sub-header">⚙️ Configuration</h3>', unsafe_allow_html=True)
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["YouTube URL", "Upload Transcript", "Paste Transcript"]
        )
        
        # Verbose mode
        verbose = st.checkbox("Verbose output", value=False)
        
        # Intro file upload
        intro_file = st.file_uploader(
            "Upload intro context (optional)",
            type=['txt'],
            help="Provide additional context for the analysis"
        )
        
        # Usage information in sidebar
        st.markdown("---")
        st.markdown("**Usage Limits:**")
        st.markdown("- 10 requests per day")
        st.markdown("- 30 seconds between requests")
        st.markdown("- This helps control API costs")
        
        # Cost warning
        st.markdown("---")
        st.markdown("**⚠️ Cost Warning:**")
        st.markdown("Each analysis uses:")
        st.markdown("- OpenAI API (transcription + analysis)")
        st.markdown("- Perplexity API (verification)")
        st.markdown("Monitor your API usage!")
    
    # Main content area
    if input_method == "YouTube URL":
        st.markdown('<h3 class="sub-header">📺 YouTube Video Analysis</h3>', unsafe_allow_html=True)
        
        url = st.text_input(
            "Enter YouTube URL:",
            placeholder="https://www.youtube.com/watch?v=..."
        )
        
        if st.button("🚀 Analyze Video", type="primary"):
            if url:
                # Check rate limit
                allowed, message = check_rate_limit()
                if not allowed:
                    st.error(f"❌ {message}")
                else:
                    update_usage()
                    analyze_youtube_video(url, verbose, intro_file)
            else:
                st.error("Please enter a YouTube URL")
    
    elif input_method == "Upload Transcript":
        st.markdown('<h3 class="sub-header">📄 Transcript Upload</h3>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload transcript file:",
            type=['txt'],
            help="Upload a text file containing the transcript"
        )
        
        if st.button("🚀 Analyze Transcript", type="primary"):
            if uploaded_file is not None:
                # Check rate limit
                allowed, message = check_rate_limit()
                if not allowed:
                    st.error(f"❌ {message}")
                else:
                    update_usage()
                    analyze_uploaded_transcript(uploaded_file, verbose, intro_file)
            else:
                st.error("Please upload a transcript file")
    
    else:  # Paste Transcript
        st.markdown('<h3 class="sub-header">📝 Paste Transcript</h3>', unsafe_allow_html=True)
        
        transcript_text = st.text_area(
            "Paste your transcript here:",
            height=200,
            placeholder="Paste the transcript text here..."
        )
        
        if st.button("🚀 Analyze Transcript", type="primary"):
            if transcript_text.strip():
                # Check rate limit
                allowed, message = check_rate_limit()
                if not allowed:
                    st.error(f"❌ {message}")
                else:
                    update_usage()
                    analyze_pasted_transcript(transcript_text, verbose, intro_file)
            else:
                st.error("Please paste some transcript text")

def analyze_youtube_video(url, verbose, intro_file):
    """Analyze a YouTube video"""
    try:
        with st.spinner("🔄 Processing YouTube video..."):
            # Create progress container
            progress_container = st.container()
            
            with progress_container:
                st.info("Step 1/4: Downloading video...")
            
            # Download video
            try:
                audio_path = downloader.download_audio(url)
            except Exception as e:
                st.error(f"❌ Error downloading video: {str(e)}")
                st.warning("💡 Tip: Try using the 'Upload Transcript' or 'Paste Transcript' options instead.")
                return
            
            with progress_container:
                st.info("Step 2/4: Transcribing audio...")
            
            # Transcribe
            try:
                transcript = transcriber.transcribe_audio(audio_path)
            except Exception as e:
                st.error(f"❌ Error transcribing audio: {str(e)}")
                st.warning("💡 Tip: Try using the 'Upload Transcript' or 'Paste Transcript' options instead.")
                return
            
            with progress_container:
                st.info("Step 3/4: Extracting predictions...")
            
            # Get intro text if provided
            intro_text = ""
            if intro_file:
                intro_text = intro_file.getvalue().decode('utf-8')
            
            # Extract predictions
            predictions = prediction_extractor.extract_predictions(transcript, intro=intro_text)
            
            with progress_container:
                st.info("Step 4/4: Verifying predictions...")
            
            # Verify predictions
            verified_results = {}
            for prediction in predictions:
                gpt_response = prediction_verifier.verify_prediction_with_perplexity(prediction)
                
                actual_result = "Not found"
                rating = "UNCLEAR"
                
                for line in gpt_response.splitlines():
                    if line.strip().lower().startswith("actual result:"):
                        actual_result = line.split(":", 1)[1].strip()
                    elif line.strip().lower().startswith("rating:"):
                        rating = line.split(":", 1)[1].strip()
                
                verified_results[prediction] = {
                    "actual": actual_result,
                    "rating": rating
                }
            
            # Generate narrative
            video_title = os.path.splitext(os.path.basename(audio_path))[0]
            narrative = narrative_generator.generate_narrative(
                video_title=video_title,
                intro_text=intro_text,
                verified_results=verified_results
            )
            
            # Display results
            display_results(verified_results, narrative, transcript)
            
    except Exception as e:
        st.error(f"❌ Error processing video: {str(e)}")
        if verbose:
            st.exception(e)

def analyze_uploaded_transcript(uploaded_file, verbose, intro_file):
    """Analyze an uploaded transcript file"""
    try:
        with st.spinner("🔄 Processing uploaded transcript..."):
            # Read transcript
            transcript = uploaded_file.getvalue().decode('utf-8')
            
            # Get intro text if provided
            intro_text = ""
            if intro_file:
                intro_text = intro_file.getvalue().decode('utf-8')
            
            # Process transcript
            process_transcript(transcript, intro_text, verbose, "Uploaded Transcript")
            
    except Exception as e:
        st.error(f"❌ Error processing transcript: {str(e)}")
        if verbose:
            st.exception(e)

def analyze_pasted_transcript(transcript_text, verbose, intro_file):
    """Analyze pasted transcript text"""
    try:
        with st.spinner("🔄 Processing pasted transcript..."):
            # Get intro text if provided
            intro_text = ""
            if intro_file:
                intro_text = intro_file.getvalue().decode('utf-8')
            
            # Process transcript
            process_transcript(transcript_text, intro_text, verbose, "Pasted Transcript")
            
    except Exception as e:
        st.error(f"❌ Error processing transcript: {str(e)}")
        if verbose:
            st.exception(e)

def process_transcript(transcript, intro_text, verbose, video_title):
    """Process transcript and display results"""
    # Extract predictions
    predictions = prediction_extractor.extract_predictions(transcript, intro=intro_text)
    
    # Verify predictions
    verified_results = {}
    for prediction in predictions:
        gpt_response = prediction_verifier.verify_prediction_with_perplexity(prediction)
        
        actual_result = "Not found"
        rating = "UNCLEAR"
        
        for line in gpt_response.splitlines():
            if line.strip().lower().startswith("actual result:"):
                actual_result = line.split(":", 1)[1].strip()
            elif line.strip().lower().startswith("rating:"):
                rating = line.split(":", 1)[1].strip()
        
        verified_results[prediction] = {
            "actual": actual_result,
            "rating": rating
        }
    
    # Generate narrative
    narrative = narrative_generator.generate_narrative(
        video_title=video_title,
        intro_text=intro_text,
        verified_results=verified_results
    )
    
    # Display results
    display_results(verified_results, narrative, transcript)

def display_results(verified_results, narrative, transcript):
    """Display analysis results"""
    st.markdown('<h3 class="sub-header">📊 Analysis Results</h3>', unsafe_allow_html=True)
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    total_predictions = len(verified_results)
    true_count = sum(1 for details in verified_results.values() if details.get('rating') == 'TRUE')
    false_count = sum(1 for details in verified_results.values() if details.get('rating') == 'FALSE')
    unclear_count = sum(1 for details in verified_results.values() if details.get('rating') in ['UNCLEAR', 'NOT YET'])
    
    with col1:
        st.metric("Total Predictions", total_predictions)
    with col2:
        st.metric("True", true_count)
    with col3:
        st.metric("False", false_count)
    with col4:
        st.metric("Unclear/Not Yet", unclear_count)
    
    # Predictions details
    st.markdown('<h4>🔍 Predictions Analysis</h4>', unsafe_allow_html=True)
    
    for i, (prediction, details) in enumerate(verified_results.items(), 1):
        with st.expander(f"Prediction {i}: {prediction[:100]}..."):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("**Prediction:**", prediction)
                st.write("**Actual Result:**", details.get('actual', 'N/A'))
                st.write("**Rating:**", details.get('rating', 'N/A'))
            
            with col2:
                rating = details.get('rating', 'UNCLEAR')
                if rating == 'TRUE':
                    st.success("✅ TRUE")
                elif rating == 'FALSE':
                    st.error("❌ FALSE")
                else:
                    st.warning("⚠️ UNCLEAR/NOT YET")
    
    # Narrative
    st.markdown('<h4>📖 Generated Narrative</h4>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-box">{narrative}</div>', unsafe_allow_html=True)
    
    # Download results
    st.markdown('<h4>💾 Download Results</h4>', unsafe_allow_html=True)
    
    # Create downloadable text
    results_text = f"""ProjectY Analysis Results

PREDICTIONS SUMMARY:
Total Predictions: {total_predictions}
True: {true_count}
False: {false_count}
Unclear/Not Yet: {unclear_count}

DETAILED PREDICTIONS:
"""
    
    for i, (prediction, details) in enumerate(verified_results.items(), 1):
        results_text += f"""
Prediction {i}:
- Prediction: {prediction}
- Actual Result: {details.get('actual', 'N/A')}
- Rating: {details.get('rating', 'N/A')}
"""
    
    results_text += f"""

NARRATIVE:
{narrative}
"""
    
    st.download_button(
        label="📥 Download Results as Text",
        data=results_text,
        file_name="projectY_analysis_results.txt",
        mime="text/plain"
    )

if __name__ == "__main__":
    main() 