To automate the conversion of Obsidian-style `[[...]]` links into GitHub-compatible markdown links across all files and subfolders, you can write a Python script that:

1. **Recursively finds all `.md` files** in a given directory and its subdirectories.
2. **Replaces the `[[...]]` links** in each file with the correct GitHub markdown links.
3. **Automatically adjusts the paths** based on where the actual files are located.

Here’s a Python script that achieves this:

### Python Script for Automating Obsidian to GitHub Link Conversion

```python
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
                rel_path = os.path.relpath(md_file, start=os.path.dirname(current_file_path))
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
    root_directory = "path/to/your/obsidian-vault-or-markdown-files"
    
    # Process all markdown files in the root directory
    process_md_files(root_directory)
```

### Explanation:

1. **`convert_obsidian_to_github` function**:
   - This function scans the markdown text for Obsidian-style `[[link]]` patterns using a regular expression.
   - For each `[[...]]` link found, it attempts to find the corresponding markdown file by checking against the list of all `.md` files in the project.
   - Once the file is found, it calculates the relative path from the current file to the linked file and updates the link accordingly.
   
2. **`find_all_md_files` function**:
   - This function recursively searches through the root directory and subdirectories for all markdown files (`.md`) and stores their full paths in a list.
   
3. **`process_md_files` function**:
   - This function reads each markdown file, converts the links if necessary, and overwrites the file with the updated content if any changes were made.
   
4. **Main script**:
   - You set the `root_directory` to point to the root of your Obsidian vault or wherever your markdown files are located.
   - The script then processes each markdown file, updating the links as needed.

### Key Points:
- **Link Conversion**: The script replaces the `[[...]]` links with `[...](path/to/file.md)` links, where `path/to/file.md` is the relative path from the current file.
- **Directory Structure**: It supports converting links across subfolders by adjusting relative paths.
- **File Handling**: It processes each `.md` file one at a time, ensuring each file’s links are correctly updated.

### Steps to Use the Script:

1. **Install Python**: Ensure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

2. **Save the Script**: Copy the script into a file, e.g., `convert_obsidian_links.py`.

3. **Run the Script**:
   - In the script, replace `path/to/your/obsidian-vault-or-markdown-files` with the actual path to your Obsidian vault or directory containing markdown files.
   - Run the script from the command line:
     ```bash
     python convert_obsidian_links.py
     ```

4. **Review Changes**: The script will print out which files had their links updated.

### Example:

- **Before:**
  ```markdown
  Here is a link to [[Common Principles]] and another to [[Another Note]].
  ```

- **After (in GitHub):**
  ```markdown
  Here is a link to [Common Principles](path/to/Common-Principles.md) and another to [Another Note](path/to/Another-Note.md).
  ```

This script ensures that all your Obsidian-style links are correctly converted and compatible with GitHub's markdown format. Would you like to explore any further enhancements?