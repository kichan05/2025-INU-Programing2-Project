import json
import time
from google import genai
from env import GEMINI_API_KEY


def get_analysis_for_game_stats(stats_data: dict) -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)

    games_data = stats_data.get("games", {})

    if not games_data:
        return "분석할 데이터가 충분하지 않습니다. 게임을 먼저 플레이해주세요!"

    stats_str = ""

    for game, data in games_data.items():
        stats_str += f"- {game}:\n"
        stats_str += f"  - Avg: {data.get('avg_r_time', 'N/A'):.2f} ms\n"
        stats_str += f"  - Best: {data.get('best_r_time', 'N/A'):.2f} ms\n"
        stats_str += f"  - Total round: {data.get('total_rounds', 'N/A')}\n"
        stats_str += f"  - 평균 점수: {data.get('avg_score', 'N/A'):.2f}\n\n"

    prompt_template = f"""
        You are an expert AI in cognitive science and digital healthcare, specifically designed to analyze signs of 'Digital Dementia' (cognitive decline due to technology overuse).

        The player's name is '{stats_data.get("player_name", "Player")}'.

        Please analyze the user's game data based on the following Context and Instructions.

        ### 1. Game Definitions & Standard Benchmarks (Context)
        * **GAME1 (Visual Choice Reaction):**
            * **Description:** Clicking a specific button matching a number displayed on the screen.
            * **Function:** Measures visual processing speed, fine motor skills, and decision-making.
            * **Standard Benchmark:** 400ms - 600ms (Healthy range).
        * **GAME2 (Auditory Reflex - Eye Blink):**
            * **Description:** Blinking eyes rapidly in response to a buzzer sound.
            * **Function:** Measures auditory reflex speed and cranial nerve reaction. Auditory stimuli are typically processed faster than visual ones.
            * **Standard Benchmark:** 200ms - 350ms (Healthy range).
        * **GAME3 (Cognitive Interference / Multi-modal Stroop):**
            * **Description:** Determining if the screen color matches the spoken color name.
            * **Function:** Measures 'Cognitive Inhibition' and 'Selective Attention' (Prefrontal Cortex function). This is crucial for detecting digital dementia (lack of focus).
            * **Standard Benchmark:** 700ms - 900ms (Healthy range).

        ### 2. Player's Statistics (Data)
        {stats_str}

        ### 3. Report Instructions (Output Format)
        Write a professional yet accessible health analysis report in **Korean**.

        **IMPORTANT: Do NOT use any Markdown formatting.**
        - Do not use bold (**text**), italics, or headers (##).
        - Do not use bullet points that require markdown parsing.
        - Provide the output in **Plain Text** only.
        - Use simple line breaks or numbering to distinguish sections.

        The report must include:

        [SECTION 1: 게임별 상세 분석]
        * For each game, describe what it tests (using the definitions above).
        * Compare the player's speed to the Standard Benchmark.
        * *Example:* "게임 3은 전두엽의 인지 억제 능력을 테스트합니다. 플레이어의 속도는 OOms로 평균보다 다소 느립니다."

        [SECTION 2: 디지털 치매 위험도 평가]
        * Analyze the risk level (Low / Moderate / High) based on the data.
        * **Logic:**
            * If GAME3 is significantly slow or has a low score, increase the risk level (indicates poor focus).
            * If GAME1 and GAME2 are slow, it indicates general cognitive fatigue or slow reflexes.
        * Explain *why* based on the specific game results.

        [SECTION 3: 맞춤형 뇌 건강 처방]
        * Provide 2 specific exercises or habits to improve the weak points identified above.

        **Tone:** Medical, Analytical, Objective, yet Warm and Encouraging.
        """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt_template
        )
        return response.text
    except Exception as e:
        return f"AI 분석 중 예기치 않은 오류가 발생했습니다: {e}"
