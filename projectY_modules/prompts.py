
#CHATGPT CREATED PROMPT
extract_predictions_prompt = """
    You are analyzing a conversation transcript. 
    
    {intro}

    Your goal is to extract **clear, concrete predictions about future OUTCOMES**, 
    avoiding scheduled events, facts, or uncertain statements.

    **What counts as a PREDICTION?**
    - Statements that predict **WHO WILL WIN, WHAT WILL HAPPEN, or WHAT THE OUTCOME WILL BE**
    - Statements about **uncertain future results** that could go either way
    - Example phrases: "will win," "will lose," "will happen," "is expected to succeed," "is likely to fail," "will reach," "will achieve"

    **What to IGNORE (these are NOT predictions):**
    - **Scheduled events** (e.g., "Fenerbahce is going to play a game next Tuesday" - this is a fact)
    - **Past events** or historical information
    - **General opinions** without specific outcomes
    - **Vague statements** (e.g., "it's not over," "maybe," "we will see")
    - **Aspirational goals** without specific predictions

    **Key Distinction:**
    - "Fenerbahce is going to play a game next Tuesday" = SCHEDULED EVENT (fact)
    - "Fenerbahce will win the game next Tuesday" = PREDICTION (outcome)
    - "The meeting is scheduled for 3 PM" = SCHEDULED EVENT (fact)
    - "The meeting will be productive" = PREDICTION (outcome)
    - "The election is on November 5th" = SCHEDULED EVENT (fact)
    - "Candidate X will win the election" = PREDICTION (outcome)
    - "My burthday will be next week" = SCHEDULED EVENT (fact)
    - "I will receive a lego set for my birthday" = PREDICTION (outcome)
    

    **Transcript:**
    {transcript}

    **Task:**
    - Extract **up to 10 of the most important predictions about OUTCOMES** in a numbered list.
    - Focus on predictions about **WHO will win, WHAT will happen, or WHAT the result will be**.
    - Ignore scheduled events, facts, or general statements.
    - If no predictions are found, respond with: "No clear predictions about outcomes were made in this conversation."

    **Response Format Example:**
    1. Fenerbahce will win the Champions League game next Tuesday.
    2. Inflation will decrease by 2% next quarter.
    3. AI adoption in healthcare will grow significantly in the next five years.
    4. The player will score at least 20 goals this season.
    5. Scientists will achieve a major breakthrough in battery technology by 2030.
    """

#ANTHROPIC CREATED PROMPT
# extract_predictions_prompt = """"
#     # Prediction Extraction Prompt

#     Analyze the provided transcript and extract verifiable predictions. A verifiable prediction is a specific claim about a future event or outcome that can be objectively determined to have occurred or not occurred.

#     ## Instructions:
#     1. Identify explicit predictions made in the transcript.
#     2. Only include predictions that are:
#     - Specific and clear
#     - Objectively verifiable
#     - About future events or outcomes
#     3. Exclude statements that are:
#     - Opinions or subjective judgments
#     - Too vague to verify
#     - General trends without specific metrics
#     - Aspirational goals without concrete metrics

#     ## Output Format:
#     - If predictions are found, list up to 10 of the most clear and verifiable predictions
#     - For each prediction, include:
#     - The exact prediction
#     - The timeframe (if specified)
#     - Any specific metrics or conditions mentioned
#     - If no verifiable predictions are found, state: "No verifiable predictions were identified in this transcript."

#     ## Examples of verifiable predictions:
#     - "Company X's stock will reach $500 by December 2023"
#     - "Inflation will rise to 2.5% by Q2 2024"
#     - "Team A will defeat Team B in next month's championship game"
#     - "The new product will generate $10M in revenue within its first year"

#     ## Examples of non-verifiable statements (do not include):
#     - "Our company will be the industry leader"
#     - "The economy will perform well"
#     - "This will be the most exciting season ever"
#     - "The quality of our service will improve"

# """



generate_search_query_prompt = """
You are an expert at transforming predictions into precise Google search queries to verify if the prediction came true.

Your goal is to generate a search query that will return clear, factual information about whether the prediction has already happened and what the result was.

**Prediction:** "{prediction}"

**Instructions:**
- Reformulate the prediction into a fact-checking query.
- Focus on results, outcomes, or confirmations.
- If it's a sports prediction, ask for the final score or who won.
- If it's a political or business event, ask if the event occurred or what the outcome was.
- Use natural phrasing, but make sure it's concise and specific.

**Example Conversions:**
- Prediction: "Portugal is predicted to win Euro 2024"
  → Search Query: "Did Portugal win Euro 2024" OR "Portugal Euro 2024 final result"

- Prediction: "Bitcoin will reach $100,000 in 2024"
  → Search Query: "Bitcoin price March 2024" OR "Has Bitcoin reached $100,000 in 2024"

**Return only the optimized search query. No explanation needed.**
"""

verify_prediction_prompt = """
You are verifying whether a prediction has come true using real-time Google search results.

**Prediction:** "{prediction}"

**Search Results:**
{search_snippets}

**Your Task:**
1. Summarize what actually happened based on the search results. Include details that help confirm or refute the prediction.
2. Use the evidence to classify the prediction as one of the following:

   - TRUE: The event clearly occurred as predicted.
   - FALSE: The event clearly did NOT happen or the outcome was the opposite of predicted.
   - NOT YET: The event is scheduled or expected in the future, and has not happened yet.
   - UNCLEAR: The results are inconclusive, incomplete, or only partially address the prediction.

If the search results mention a future date or say the event is upcoming, classify as NOT YET.

If there is no useful information at all, say "No clear result found" and classify as UNCLEAR.

**Response Format Example:**
Actual Result: "Portugal has not yet played the Euro 2024 final. The tournament ends July 14, 2024."
Rating: NOT YET
"""
verify_prediction_prompt_perplexity = """
I am verifying a prediction. Based on the most current available web information, please classify this prediction.

Prediction: "{prediction}"

Classify the prediction as one of the following:
- TRUE → It happened as predicted.
- FALSE → It did not happen.
- NOT YET → The event is in the future and hasn't occurred yet.
- UNCLEAR → Not enough evidence, or conflicting sources.

Respond with a brief summary of the current status, then the classification like this:

Actual Result: [summary]
Rating: TRUE/FALSE/NOT YET/UNCLEAR
"""

generate_narrative_prompt = """
You are a podcast host summarizing a YouTube video that contains a number of predictions. 
Your goal is to walk the audience through each prediction, what actually happened, and whether it came true — 
all in a tone that’s fun, conversational, and informative, but always respectful.

**Video Title**: {video_title}
**Intro Context**: {intro_text}
**Predictions and Ratings**:
{predictions_block}

**Format your response like this**:
Intro:
[Brief, engaging intro. Mention the video, speaker (if known), and what the audience is about to hear.]

Prediction 1:
[Explain the prediction, what happened, and whether it came true or not. Keep it natural, as if you're talking to a podcast audience.]

...

Conclusion:
[Wrap it all up. Give a quick summary of how many predictions were right or wrong, and end on a note of curiosity or reflection.]

**Style Guidelines**:
- Use natural language like you’re hosting a podcast.
- You may say things like “Let’s dive in,” or “Here’s how that turned out.”
- Refer to the speaker by name/title/context if provided in the intro.
- Be brief but vivid — aim for 60–90 seconds per prediction if read aloud.

Do not include markdown formatting or a numbered list. Just clearly mark the sections: Intro:, Prediction 1:, Prediction 2:, etc., Conclusion:
"""
