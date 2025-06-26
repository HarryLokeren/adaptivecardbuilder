# adaptivecardbuilder

Tiny helper for building and sending Adaptive Cards to Microsoft Teams — including dynamic rows, styled error messages, and emoji support.

---

## 📦 Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/HarryLokeren/adaptivecardbuilder.git

from adaptivecardbuilder import AdaptiveCardBuilder

card = AdaptiveCardBuilder()

# Add a simple text block
card.add_text_block("✅ AdaptiveCardBuilder is working!")

# Add a styled error block
card.add_error_block("❌ File upload failed: permission denied.")

# Add rows with dynamic columns — only provided fields are shown
card.add_item(
    name="report.csv",
    size_kb="432kb",
    status="Uploaded",
    source="SharePoint",
    date_downloaded=True
)

card.add_item(name="logfile.txt", status="Skipped")
card.add_item(name="readme.md")

# Send the card to Microsoft Teams
card.send_to_teams("https://outlook.office.com/webhook/...")

print(AdaptiveCardBuilder.emoji["success"])  # ✅
print(AdaptiveCardBuilder.emoji["failure"])  # ❌
print(AdaptiveCardBuilder.emoji["file"])     # 📄

---


