
import os
import re

# Function to convert Obsidian-style links to GitHub markdown links
def convert_obsidian_to_github(text, current_file_path, all_md_files):
    # Regex pattern to find Obsidian-style links
    pattern = r'\[\[([^\]]+)\]\]'
    
    def replace_link(match):
        note_name = match.group(1)
        # Normalize file name (replace spaces with hyphens, adjust file case if needed)
        note_file = note_name.replace(' ', '-') + ".md"
        
        # Find the actual file location from the list of all markdown files
        for md_file in all_md_files:
            if md_file.endswith(note_file):
                # Compute the relative path between the current file and the note
                rel_path = os.path.relpath(md_file, start=os.path.join(r"https://SathishKumar9866",
                                                                       os.path.dirname(current_file_path)))
                return f"[{note_name}]({rel_path})"
        
        # If no matching file found, return the original text
        return f"[[{note_name}]]"
    
    # Use the replace function in regex to convert all links
    return re.sub(pattern, replace_link, text)

# Function to recursively find all markdown files in a directory
def find_all_md_files(root_dir):
    md_files = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(subdir, file))
    return md_files

# Function to process each markdown file and update links
def process_md_files(root_dir):
    # Find all markdown files in the root directory and subdirectories
    all_md_files = find_all_md_files(root_dir)
    
    # Process each markdown file
    for md_file in all_md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert the content
        updated_content = convert_obsidian_to_github(content, md_file, all_md_files)
        
        # If the content has changed, overwrite the file
        if updated_content != content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated links in {md_file}")

# Main function to run the script
if __name__ == "__main__":
    # Set the root directory to the location of your Obsidian vault or markdown files
    root_directory = rf"C:\Users\devil\Downloads\ubuntu_backup\system_design_interview_prep"
    
    # Process all markdown files in the root directory
    process_md_files(root_directory)
