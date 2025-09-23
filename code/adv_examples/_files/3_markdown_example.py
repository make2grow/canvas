#!/usr/bin/env python3
"""
Markdown to HTML Demo
Shows how Canvas content looks when converted from Markdown
"""

import markdown

def read_markdown_file(md_file_path):
    try:
        with open(md_file_path, "r", encoding="utf-8") as f:
            syllabus_md = f.read()
            return syllabus_md
    except FileNotFoundError:
        print(f"Error: The file '{md_file_path}' was not found.")
        return None
    except Exception as e:
        print(f"Error reading the file '{md_file_path}': {e}")
        return None

def markdown_to_html(markdown_content):
    """Convert Markdown to HTML with extensions"""
    return markdown.markdown(
        markdown_content, 
        extensions=['extra', 'codehilite', 'toc', 'tables']
    )

def demo_conversion():
    """Demonstrate Markdown to HTML conversion"""
    
    # Example 1: Simple syllabus
    syllabus_md = read_markdown_file("markdown_templates/syllabus_template.md") 
    if syllabus_md:
        syllabus_html = markdown_to_html(syllabus_md)
        print(syllabus_html)


if __name__ == "__main__":
    # Run the demo
    demo_conversion()
    
    print("\n" + "=" * 60)
    print("💡 BENEFITS OF MARKDOWN APPROACH")
    print("=" * 60)
    print("✅ Write content in familiar Markdown syntax")
    print("✅ Store templates as .md files for reuse")  
    print("✅ Version control friendly (clean diffs)")
    print("✅ Automatic HTML conversion for Canvas")
    print("✅ Support for tables, code blocks, and more")
    print("\n🚀 Ready to use with Canvas API!")
