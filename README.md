# adaptivecardbuilder

Tiny helper for building and sending Adaptive Cards to Microsoft Teams.

```python
from adaptivecard import AdaptiveCardBuilder

card = AdaptiveCardBuilder()
card.add_text_block("✅ Works from Git!")
card.send_to_teams("https://outlook.office.com/webhook/...")
