from app.ai.openai_client import ask_llm

def run_fundamental_analysis(stock_name: str, exchange: str, timeframe: str = "1day"):
    prompt = f"""
Perform a detailed fundamental analysis of {stock_name} listed on {exchange}
Focus on the relevance for a '{timeframe}' trading horizon (if applicable).
using the latest publicly available financial data.

Structure the response with clear headings and bullet points.

Include:
1. Financial Statements Analysis
- Revenue growth (YoY & QoQ)
- Profitability (operating, net margin)
- EPS trends
- Debt & liquidity
- Cash flow strength

2. Valuation Metrics
- P/E, P/B, EV/EBITDA
- Dividend yield (if applicable)
- Comparison to peers

3. Growth & Competitive Position
- Industry outlook
- Competitive moat
- Management quality
- Innovation / AI / R&D

4. Risk Analysis
- Market risks
- Operational risks
- Debt & liquidity risks

5. Recent News & Catalysts
- Earnings
- Deals / M&A
- Regulation
- Product launches

6. Investment Outlook
- Bullish case
- Bearish case
- Short vs long-term view

IMPORTANT:
- Use simple, investor-friendly language
- DO NOT give buy/sell recommendations
- At the end of EACH major section, add source links in brackets

Example source format:
(Source: annual report, screener.in, moneycontrol.com, company filings, investor presentations)

Be factual, cautious, and realistic.
"""

    return ask_llm(prompt)
