from adaptive_card_builder import AdaptiveCardBuilder

card = AdaptiveCardBuilder()
card.add_text_block("📊 System Health Report", size="medium", weight="bolder")
card.add_table(
    ["Component", "Status", "Last Check"],
    [
        ["DB", "✅ OK", "2025-06-16"],
        ["API", "❌ Error", "2025-06-16"],
    ]
)

# Your webhook URL (from Teams connector)
teams_webhook = "https://prod-146.westeurope.logic.azure.com:443/workflows/a40b44de67d24d1cb936d5c13d294d6c/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=6I2k0685AdkABDerXYwrcwBTnFU_UdECRsDZ5-9b8Zc"

# Send it!
card.send_to_teams(teams_webhook)