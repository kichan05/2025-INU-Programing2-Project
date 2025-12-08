import json
import time
from google import genai
from env import GEMINI_API_KEY


def get_analysis_for_game_stats(stats_data: dict) -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt_template = """
    You are a professional game coach analyzing a player's reaction speed game data.
    The player's name is '{player_name}'.

    Here are their statistics:
    {stats_str}

    Based on this data, provide a friendly, insightful, and encouraging analysis in 2-3 sentences.
    Focus on their strengths and offer one concrete tip for improvement. Address the player by their name.
    The analysis should be in Korean.
    """

    player_name = stats_data.get("player_name", "Player")
    stats_str = ""
    games_data = stats_data.get("games", {})

    if not games_data:
        return "분석할 데이터가 충분하지 않습니다. 게임을 먼저 플레이해주세요!"

    for game, data in games_data.items():
        stats_str += f"- {game}:\n"
        stats_str += f"  - 평균 반응 속도: {data.get('avg_r_time', 'N/A'):.2f} ms\n"
        stats_str += f"  - 최고 반응 속도: {data.get('best_r_time', 'N/A'):.2f} ms\n"
        stats_str += f"  - 총 라운드: {data.get('total_rounds', 'N/A')}\n"
        stats_str += f"  - 평균 점수: {data.get('avg_score', 'N/A'):.2f}\n\n"

    final_prompt = prompt_template.format(player_name=player_name, stats_str=stats_str)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=final_prompt
        )
        return response.text
    except Exception as e:
        return f"AI 분석 중 예기치 않은 오류가 발생했습니다: {e}"
