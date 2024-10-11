import os
import re

# Function to check and update links with spaces in filenames and change them to hyphens
def check_and_update_links_with_spaces(text):
    # This regex pattern matches markdown links like [text](path/to/file name.md)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    def replace_link(match):
        link_text = match.group(1)
        link_url = match.group(2)

        # If the link URL contains spaces in the filename, replace them with hyphens
        if ' ' in link_url:
            # Replace spaces with hyphens in the file part of the URL (keeping the rest of the path intact)
            updated_link_url = link_url.replace(' ', '-')
            print(f"Updated link: {link_url} -> {updated_link_url}")

            # Return the updated link with hyphenated filenames
            return f"[{link_text}]({updated_link_url})"
        return match.group(0)

    # Use re.sub to replace all markdown links that contain spaces in the filenames
    return re.sub(pattern, replace_link, text)

# Function to recursively find all markdown files in a directory
def find_all_md_files(root_dir):
    md_files = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(subdir, file))
    return md_files

# Function to process each markdown file and check/update links with spaces in filenames
def process_md_files_for_links(root_dir):
    # Find all markdown files
    all_md_files = find_all_md_files(root_dir)
    
    # Process each markdown file
    for md_file in all_md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check and update any links with spaces in filenames
            updated_content = check_and_update_links_with_spaces(content)

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
    
    # Process all markdown files in the directory for updating links with spaces
    process_md_files_for_links(root_directory)
