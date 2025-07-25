import json
import os

template = """{{% extends "power-broker/_power-broker-summary-page.html" %}}
{{% block chapter %}}{chapter}{{% endblock %}}
{{% block index %}}{index}{{% endblock %}}
{{% block page %}}{page}{{% endblock %}}
{{% block content %}}
    {content}
{{% endblock %}}
"""

chapter_data = json.load(open("../power-broker-metadata.json", "r"))
if not os.path.exists("html"):
    os.makedirs("html")

for i, chapter in enumerate(chapter_data["chapters"][:-1]):
    chapter_filename = f"chapter_{i}_summary_tmp/final_summary.txt"
    summary = open(chapter_filename, "r").read()
    paragraphs = summary.split("\n\n")
    content = "\n\n".join(f"<p>{p.strip()}</p>" for p in paragraphs if p.strip())
    html_page = template.format(
        chapter=chapter["name"],
        index=i,
        page=chapter["page"],
        content=content
    )
    os.makedirs(f"html/{i}", exist_ok=True)
    with open(f"html/{i}/index.html", "w") as f:
        f.write(html_page)