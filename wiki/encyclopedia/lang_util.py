from markdown2 import Markdown

# Convert markdown syntax to html
def markdownToHtml(content):
    markdowner = Markdown()
    return markdowner.convert(content)
