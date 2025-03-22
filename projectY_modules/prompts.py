
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

verify_prediction_prompt = """
    You are verifying whether a prediction has come true using real-time Google search results.
    
    **Prediction:** "{prediction}"

    **Search Results:**
    {search_snippets}

    **Your Task:**
    1. **Summarize the key event from the search results** that confirms or contradicts the prediction. If the search results don't contain relevant details, say "No clear result found."
    2. **Classify the prediction as:**
       - **TRUE** → The event has definitively happened.
       - **FALSE** → The event did not happen.
       - **UNCLEAR** → There are conflicting sources, partial evidence, or no conclusive proof yet.
       - **NOT YET** → The event is in the future, and there is no evidence that it has happened.

    **Response Format Example:**
    Actual Result: "AZ Alkmaar won the game 1-0, contradicting the prediction."
    Rating: FALSE
    """


generate_search_query_prompt = """
    You are an expert at crafting precise Google search queries.
    Your goal is to transform the given prediction into the **best possible search query** to find real-world results.

    **Prediction:** "{prediction}"

    **Instructions:**
    - Reformulate the prediction into a **high-quality search query** that will return useful information.
    - Focus on getting up-to-date news, results, or analysis relevant to the prediction.
    - Avoid unnecessary words or fluff.
    - if this is a sporting event you can use things like "final score OR match result OR who won" but reword naturally.

    **Example Conversions:**
    - Prediction: "Bitcoin will reach $100,000 in 2024."
      → Search Query: "Bitcoin price update 2024 latest news"
      
    - Prediction: "NASA will launch a manned Mars mission by 2030."
      → Search Query: "NASA Mars mission 2030 latest updates"

    **Return only the search query. No explanation needed.**
    """
