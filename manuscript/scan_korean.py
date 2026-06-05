import os
import re

def find_korean_in_listings(directory):
    # Regex to find lstlisting blocks
    listing_regex = re.compile(r'\\begin\{lstlisting\}(.*?)\\end\{lstlisting\}', re.DOTALL)
    # Regex to detect Korean characters (Hangul Syllables, Jamo, etc.)
    korean_regex = re.compile(r'[\uac00-\ud7af\u1100-\u11ff\u3130-\u318f\ua960-\ua97f\ud7b0-\ud7ff]')

    matches = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.tex'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    listings = listing_regex.finditer(content)
                    for i, listing in enumerate(listings):
                        listing_content = listing.group(1)
                        if korean_regex.search(listing_content):
                            # Find line number (approximate)
                            line_no = content.count('\n', 0, listing.start()) + 1
                            matches.append({
                                'file': file_path,
                                'line': line_no,
                                'content': listing_content.strip()[:200] + "..." # Snippet
                            })
    
    return matches

if __name__ == "__main__":
    results = find_korean_in_listings('/home/babelai/personal-dev/latex-book/chapters')
    if results:
        print(f"Found {len(results)} listings with Korean characters:")
        for res in results:
            print(f"--- File: {res['file']} (Line: {res['line']}) ---")
            print(res['content'])
            print()
    else:
        print("No Korean characters found in lstlisting blocks.")
