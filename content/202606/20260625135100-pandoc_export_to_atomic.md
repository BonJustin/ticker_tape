---
title: Pandoc Bash - Export To Atomic HTML
keywords: [copypasta, computer reference, pandoc, html]
---

In order to generate the same format that I am using for my static website using Pandoc, but in a portable HTML (with embedded font/js/images) for easy sharing, I copied assets (CSS and KaTeX), Pandoc defaults YAML, and Pandoc HTML template to appropriate directories in `~/.local/share/pandoc/`. I tailored the YAML file appropriately.

Now I can use Pandoc from the command line to generate atomic HTML files.

*bash*

```bash
pandoc --defaults \
embedded_html.yaml \
/path/to/markdown_file.md \
-o /path/to/html_output_file.html
```
