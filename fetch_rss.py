import urllib.request
import xml.etree.ElementTree as ET

# 1. Define your favorite RSS feeds here
FEEDS = {
    "BBC News": "http://bbci.co.uk",
    "Hacker News": "https://ycombinator.com"
}

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>My Personal RSS Feed</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; background: #f9f9f9; color: #333; }
        h1 { border-bottom: 2px solid #eaeaea; padding-bottom: 10px; }
        .feed-section { margin-bottom: 40px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .item { margin-bottom: 15px; }
        a { color: #0066cc; text-decoration: none; font-weight: bold; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>My RSS Dashboard</h1>
"""

for source_name, url in FEEDS.items():
    html_content += f"<div class='feed-section'><h2>{source_name}</h2>"
    try:
        # Fetch and parse the XML content without external dependencies
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        # Extract the first 5 articles from each feed
        items = root.findall('.//item')[:5]
        
        if not items:
            html_content += "<p>No articles found.</p>"
            
        for item in items:
            title = item.find('title').text if item.find('title') is not None else "No Title"
            link = item.find('link').text if item.find('link') is not None else "#"
            html_content += f"<div class='item'><a href='{link}' target='_blank'>{title}</a></div>"
            
    except Exception as e:
        html_content += f"<p style='color:red;'>Error loading feed: {str(e)}</p>"
    
    html_content += "</div>"

html_content += "</body></html>"

# Write the final HTML file to disk
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
