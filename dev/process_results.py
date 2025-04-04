import re
import pandas as pd
import json
import argparse

def parse_authors(author_string):
    author_string = author_string.strip()
    
    if '(' not in author_string:
        return [x.strip() for x in author_string.split(',') if x.strip()]
    
    authors = []
    
    parts = re.split(r'\)[\s,]*', author_string)
    
    for part in parts:
        part = part.strip()
        if part:
            if '(' in part and ')' not in part:
                part = part + ')'
            authors.append(part)
    
    return authors

def xlsx_to_json(xlsx_file, json_file):
    
    refused = []

    df = pd.read_excel(xlsx_file)
    
    data = df.astype(str).to_dict(orient='records')
    
    refined_data = []

    for entry in data:
        
        if (entry["Do you consent to us storing your video and responses for use on the Diploma video platform (to show other students in your year group)"] == 'No'):
            refused.append(entry['ID'] + ' | ' + entry['Group Members and roles [Format: Murad (Theorist), Irti (Designer), Jen (Maker)]'])
            continue

        entry.pop("Start time", None)
        entry.pop("Email", None)
        entry.pop("Last modified time", None)
        entry.pop('Name', None)

        entry['final-proposition'] = entry["Describe your final proposition (i.e. what you produced to respond to the concept/hypothesis\u00a0"]
        entry['insights'] = entry["Describe any insights gained from your experiment"]

        entry['title'] = entry["Describe your concept/hypothesis (max 100 words)"]
        entry['authors'] = entry['Group Members and roles [Format: Murad (Theorist), Irti (Designer), Jen (Maker)]']
        entry['authors-array'] = parse_authors(entry['authors'])
        entry['videoURL'] = re.sub(r'.*/', '/videos/compressed_', entry['Submit your final video presentation (Only submit a PDF if you are linking to your video in an external cloud folder - e.g. Google Drive, OneDrive or Dropbox)'])
        entry['videoURL'] = re.sub(r'%20', '_', entry['videoURL'])
        entry['videoURL'] = re.sub(r'\.\w+$', '.mp4', entry['videoURL'])  # Ensure .mp4 extension
        entry['thumbURL'] = re.sub(r'.*/compressed_', '/thumbs/thumb_', entry['videoURL']) + '.jpg'

        refined_data.append(entry)

    with open(json_file, 'w') as f:
        json.dump(refined_data, f, indent=4)

    print(f"Refused: {refused}")
    print(f"Data written to {json_file}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Convert XLSX to JSON')
  parser.add_argument('--input', required=True, help='Path to the input XLSX file')
  parser.add_argument('--output', required=True, help='Path to the output JSON file')
  
  args = parser.parse_args()
  
  xlsx_to_json(args.input, args.output)