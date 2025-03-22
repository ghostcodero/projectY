
#CHATGPT CREATED PROMPT
extract_predictions_prompt = """
    You are analyzing a conversation transcript. Your goal is to extract **clear, concrete predictions about the future**, 
    avoiding vague or uncertain statements.

    **What counts as a prediction?**
    - Statements that clearly express **what will happen**, **what is expected**, or **likely future outcomes**.
    - Example phrases: "will happen," "is expected to," "is likely to," "is projected to," "experts predict that," "data suggests that."

    **What to ignore?**
    - Unclear or subjective statements (e.g., "it's not over," "maybe," "we will see").
    - General reflections, opinions, or past events.

    **Transcript:**
    {transcript}

    **Task:**
    - Extract **up to 10 of the most important predictions** in a numbered list.
    - Ensure that each prediction is **specific, meaningful, and clearly about the future**.
    - If no predictions are found, respond with: "No clear predictions were made in this conversation."

    **Response Format Example:**
    1. The team is expected to switch to a defensive strategy in the next game.
    2. Analysts predict that inflation will decrease by 2% next quarter.
    3. AI adoption in healthcare will grow significantly in the next five years.
    4. The player is likely to miss the next match due to injury.
    5. Scientists anticipate a major breakthrough in battery technology by 2030.
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