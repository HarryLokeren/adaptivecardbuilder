import json
import requests
from datetime import datetime

class AdaptiveCardBuilder:
    def __init__(self, version="1.2"):
        self.card = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "type": "AdaptiveCard",
                        "body": [],
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": version
                    }
                }
            ]
        }
        self.body = self.card["attachments"][0]["content"]["body"]

    def add_text_block(self, text, size="default", weight="default", color="default", wrap=True, spacing=None):
        block = {
            "type": "TextBlock",
            "text": text,
            "wrap": wrap
        }
        if size != "default":
            block["size"] = size
        if weight != "default":
            block["weight"] = weight
        if color != "default":
            block["color"] = color
        if spacing:
            block["spacing"] = spacing
        self.body.append(block)

    def add_image(self, url, size="medium", alignment="center"):
        block = {
            "type": "Image",
            "url": url,
            "size": size,
            "horizontalAlignment": alignment
        }
        self.body.append(block)

    def add_table(self, headers, rows):
        # Add header row
        header_columns = []
        for header in headers:
            header_columns.append({
                "type": "Column",
                "items": [{
                    "type": "TextBlock",
                    "text": f"**{header}**",
                    "weight": "bolder",
                    "wrap": True
                }],
                "width": "stretch"
            })
        self.body.append({
            "type": "ColumnSet",
            "columns": header_columns
        })

        # Add data rows
        for row in rows:
            row_columns = []
            for cell in row:
                row_columns.append({
                    "type": "Column",
                    "items": [{
                        "type": "TextBlock",
                        "text": str(cell),
                        "wrap": True
                    }],
                    "width": "stretch"
                })
            self.body.append({
                "type": "ColumnSet",
                "columns": row_columns
            })

    def add_item(self, name, size_kb=None, status=None, date_modified=None, type_=None, source=None, date_downloaded=False):
        """Dynamically add a row of data based on provided fields."""
        if not name:
            raise ValueError("Name is required")

        # Determine which columns to show
        columns = {"Name": name}

        if size_kb is not None:
            columns["Size (kB)"] = size_kb
        if status is not None:
            columns["Status"] = status
        if date_modified is not None:
            columns["Date Modified"] = date_modified
        if type_ is not None:
            columns["Type"] = type_
        if source is not None:
            columns["Source"] = source
        if date_downloaded:
            columns["Date Downloaded"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Insert headers once per structure (based on column keys)
        if not hasattr(self, "_column_headers") or self._column_headers != list(columns.keys()):
            self._column_headers = list(columns.keys())
            header_columns = [
                {
                    "type": "Column",
                    "items": [{
                        "type": "TextBlock",
                        "text": f"**{key}**",
                        "weight": "bolder",
                        "wrap": True
                    }],
                    "width": "stretch"
                }
                for key in columns
            ]
            self.body.append({
                "type": "ColumnSet",
                "columns": header_columns
            })

        # Now add the actual values
        row_columns = [
            {
                "type": "Column",
                "items": [{
                    "type": "TextBlock",
                    "text": str(value),
                    "wrap": True
                }],
                "width": "stretch"
            }
            for value in columns.values()
        ]

        self.body.append({
            "type": "ColumnSet",
            "columns": row_columns
        })

    def send_to_teams(self, webhook_url):
        headers = {
            "Content-Type": "application/json"
        }

        # Teams expects just the card body, not the outer "message" wrapper
        payload = {
            "type": "message",
            "attachments": self.card["attachments"]
        }

        response = requests.post(webhook_url, headers=headers, json=payload)

        if response.status_code == 200 or response.status_code == 202:
            print("✅ Card sent to Teams successfully.")
        else:
            print(f"❌ Failed to send card to Teams. Status: {response.status_code}, Response: {response.text}")

    def get_card(self):
        return self.card

    def to_json(self, indent=4):
        return json.dumps(self.card, indent=indent)