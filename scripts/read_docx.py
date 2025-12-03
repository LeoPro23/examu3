import zipfile
import re
import sys
import os

def get_docx_text(path):
    try:
        if not os.path.exists(path):
            return f"File not found: {path}"
            
        with zipfile.ZipFile(path) as document:
            xml_content = document.read('word/document.xml').decode('utf-8')
            # Find paragraphs
            paragraphs = re.findall(r'<w:p.*?>(.*?)</w:p>', xml_content)
            text_lines = []
            for p in paragraphs:
                # Find text in paragraph
                texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', p)
                if texts:
                    text_lines.append(''.join(texts))
            return '\n'.join(text_lines)
    except Exception as e:
        return f"Error reading docx: {e}"

if __name__ == "__main__":
    if len(sys.argv) > 2:
        # Join all arguments except the last one to handle spaces in input filename
        input_filename = " ".join(sys.argv[1:-1])
        output_filename = sys.argv[-1]
        
        # Remove quotes if present
        input_filename = input_filename.strip('"')
        
        text = get_docx_text(input_filename)
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Successfully wrote to {output_filename}")
    else:
        print("Usage: python read_docx.py <input_docx> <output_txt>")
