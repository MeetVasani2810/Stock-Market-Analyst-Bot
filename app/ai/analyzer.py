from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a professional technical market analyst.

Rules:
- Use ONLY the provided signals
- Do NOT invent indicators
- Do NOT give financial advice
- Do NOT predict prices
- Explain trend, momentum, and market condition clearly
- Write in a calm, professional tone
"""

def generate_analysis(signal_summary: dict) -> str:
    user_prompt = f"""
Market: {signal_summary['symbol']}
Timeframe: {signal_summary['interval']}

Signals:
- Trend: {signal_summary['trend']}
- RSI: {signal_summary['rsi']['state']} ({signal_summary['rsi']['value']})
- MACD: {signal_summary['macd']['state']}
- Overall Bias: {signal_summary['bias']}

Write a short technical analysis summary similar to a trading desk report.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
