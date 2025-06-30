import json
import requests
from datetime import datetime

class AdaptiveCardBuilder:
    emoji = {
        "success": "✅",
        "failure": "❌",
        "warning": "⚠️",
        "info": "ℹ️",
        "download": "⬇️",
        "upload": "📤",
        "clock": "🕒",
        "file": "📄",
        "folder": "📁",
        "check": "✔️",
        "cross": "❎",
        "rocket": "🚀",
        "bug": "🐞",
        "lock": "🔒",
        "unlocked": "🔓",
        "search": "🔍",
        "fire": "🔥",
        "bell": "🔔",
        "gear": "⚙️",
    }
    
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
        self._tables = {}

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

    def add_item(self, name,tablename=None, size_kb=None, status=None, date_modified=None, type_=None, source=None, date_downloaded=False):
        """
        Add a row to a table.

        If `tablename` is provided:
            - Creates a new titled table with headers if not already started.
            - Otherwise appends a row to that table.

        If `tablename` is not provided:
            - Assumes one unnamed table (no title).
            - Ensures consistent structure across all rows.
        """
        if not name:
            raise ValueError("Name is required")

        # Build row data
        row = {"Name": name}
        if size_kb is not None:
            row["Size (kB)"] = size_kb
        if status is not None:
            row["Status"] = status
        if date_modified is not None:
            row["Date Modified"] = date_modified
        if type_ is not None:
            row["Type"] = type_
        if source is not None:
            row["Source"] = source
        if date_downloaded:
            row["Date Downloaded"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        column_keys = list(row.keys())

        # Handle named table
        if tablename:
            if not hasattr(self, "_tables"):
                self._tables = {}

            if tablename not in self._tables:
                self._tables[tablename] = column_keys

                # Add table title
                self.add_text_block(tablename, size="medium", weight="bolder", spacing="large")

                # Add headers
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
                    for key in column_keys
                ]
                self.body.append({
                    "type": "ColumnSet",
                    "columns": header_columns
                })
            else:
                if self._tables[tablename] != column_keys:
                    raise ValueError(
                        f"Table '{tablename}' has different columns.\nExpected: {self._tables[tablename]}\nGot: {column_keys}"
                    )
        else:
            # Anonymous table support
            if not hasattr(self, "_default_table_headers"):
                self._default_table_headers = column_keys

                # No title, but add headers
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
                    for key in column_keys
                ]
                self.body.append({
                    "type": "ColumnSet",
                    "columns": header_columns
                })
            else:
                if self._default_table_headers != column_keys:
                    raise ValueError(
                        "Default table already initialized with different columns.\n"
                        f"Expected: {self._default_table_headers}\nGot: {column_keys}"
                    )

        # Add row
        row_columns = [
            {
                "type": "Column",
                "items": [{
                    "type": "TextBlock",
                    "text": str(val),
                    "wrap": True
                }],
                "width": "stretch"
            }
            for val in row.values()
        ]
        self.body.append({
            "type": "ColumnSet",
            "columns": row_columns
        })


    def add_error_block(self, text):
        """Add a styled error block with dark red background and white text."""
        error_block = {
            "type": "Container",
            "style": "attention",  # built-in red background style
            "items": [
                {
                    "type": "TextBlock",
                    "text": text,
                    "wrap": True,
                    "weight": "bolder",
                    "color": "light",  # white text
                    "spacing": "medium"
                }
            ],
            "bleed": True,
            "spacing": "medium"
        }
        self.body.append(error_block)
        
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