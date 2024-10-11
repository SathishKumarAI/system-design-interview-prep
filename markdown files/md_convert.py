import os
import re

# Function to convert Obsidian-style links to GitHub markdown links
def convert_obsidian_to_github(text, repo_url, current_file_path, all_md_files):
    pattern = r'\[\[([^\]]+)\]\]'  # Matches Obsidian-style [[link]]
    
    def replace_link(match):
        note_name = match.group(1)
        note_file_variations = [
            note_name.replace(' ', '-') + ".md",  # Replace spaces with hyphens
            note_name.replace(' ', '_') + ".md",  # Replace spaces with underscores
            note_name + ".md"  # Keep spaces if any
        ]
        
        # Debug: Print possible filename variations
        print(f"Possible filenames for note '{note_name}': {note_file_variations}")
        
        # Search for the corresponding markdown file
        for md_file in all_md_files:
            if any(md_file.endswith(variation) for variation in note_file_variations):
                # Convert local path to GitHub URL
                rel_path = os.path.relpath(md_file, start=os.path.dirname(current_file_path))
                rel_path = rel_path.replace("\\", "/")  # Ensure URL uses forward slashes
                github_link = f"{repo_url}/{rel_path}"
                
                print(f"Converted link for '{note_name}': [{note_name}]({github_link})")
                return f"[{note_name}]({github_link})"
        
        # If no matching file is found, return the original link (to avoid broken links)
        print(f"No matching file found for note: {note_name}")
        return f"[[{note_name}]]"
    
    # Replace all [[...]] links with GitHub links
    return re.sub(pattern, replace_link, text)

# Function to recursively find all markdown files in a directory
def find_all_md_files(root_dir):
    md_files = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(subdir, file))
    # Debug: Print all found markdown files
    print(f"Found markdown files: {md_files}")
    return md_files

# Function to process each markdown file and update content
def process_md_files(root_dir, repo_url):
    # Find all markdown files
    all_md_files = find_all_md_files(root_dir)
    
    # Process each markdown file
    for md_file in all_md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Convert the content for GitHub links
            updated_content = convert_obsidian_to_github(content, repo_url, md_file, all_md_files)

            # If content has been updated, write it back to the file
            if updated_content != content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"Updated links in {md_file}")
            else:
                print(f"No changes needed in {md_file}")
        
        except Exception as e:
            # Print error message and continue with other files
            print(f"Error processing file {md_file}: {e}")

# Main function to run the script
if __name__ == "__main__":
    # Set the root directory to the location of your local markdown files
    root_directory = r"C:\Users\devil\Downloads\ubuntu_backup\system_design_interview_prep"
    
    # Set the base URL of your GitHub repository (ensure it points to the correct branch for markdown files)
    github_repo_url = r"https://github.com/SathishKumar9866/system-design-interview-prep/blob/backlinks_test"
    
    # Process all markdown files in the directory
    process_md_files(root_directory, github_repo_url)
