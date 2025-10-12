import os
from docx import Document
import re
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def get_heading_level(paragraph):
    """Determine the heading level based on paragraph style and formatting."""
    if paragraph.style.name.startswith('Heading'):
        return int(paragraph.style.name[-1])
    return 0

def get_text_style(run):
    """Get the text style (bold, italic) for a run."""
    style = []
    if run.bold:
        style.append('**')
    if run.italic:
        style.append('*')
    return style

def convert_docx_to_markdown(docx_path):
    """Convert a DOCX file to Markdown format."""
    doc = Document(docx_path)
    markdown_lines = []
    
    for paragraph in doc.paragraphs:
        if not paragraph.text.strip():
            markdown_lines.append('')
            continue
            
        # Handle headings
        heading_level = get_heading_level(paragraph)
        if heading_level > 0:
            markdown_lines.append(f"{'#' * heading_level} {paragraph.text}")
            continue
            
        # Handle regular paragraphs with formatting
        formatted_text = ''
        for run in paragraph.runs:
            text = run.text
            if not text.strip():
                continue
                
            # Apply text styles
            styles = get_text_style(run)
            if styles:
                text = f"{''.join(styles)}{text}{''.join(styles[::-1])}"
            formatted_text += text
            
        if formatted_text:
            markdown_lines.append(formatted_text)
    
    return '\n'.join(markdown_lines)

def process_all_docx_files(force_overwrite=False):
    """Process all DOCX files in the docx subdirectory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docx_dir = os.path.join(current_dir, 'docx')
    markdown_dir = os.path.join(current_dir, 'markdown')
    
    # Create directories if they don't exist
    os.makedirs(docx_dir, exist_ok=True)
    os.makedirs(markdown_dir, exist_ok=True)
    
    # Process each DOCX file
    for filename in os.listdir(docx_dir):
        if filename.endswith('.docx'):
            docx_path = os.path.join(docx_dir, filename)
            
            # Create markdown filename
            markdown_filename = os.path.splitext(filename)[0] + '.md'
            markdown_path = os.path.join(markdown_dir, markdown_filename)
            
            # Check if markdown file already exists
            if os.path.exists(markdown_path) and not force_overwrite:
                print(f"Skipping {filename} - {markdown_filename} already exists")
                continue
            
            # Convert to markdown
            markdown_content = convert_docx_to_markdown(docx_path)
            
            # Save markdown content
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Converted {filename} to {markdown_filename}")

if __name__ == '__main__':
    process_all_docx_files() 