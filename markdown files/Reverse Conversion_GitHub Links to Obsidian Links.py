# import os
# import re

# # Function to convert GitHub markdown links back to Obsidian-style [[link]]
# def convert_github_to_obsidian(text):
#     # This regex pattern matches GitHub markdown links like [text](https://github.com/.../filename.md)
#     pattern = r'\[([^\]]+)\]\(([^)]+)\)'

#     def replace_link(match):
#         link_text = match.group(1)
#         link_url = match.group(2)

#         # Extract the filename from the URL (remove any path before the filename)
#         file_name_with_extension = os.path.basename(link_url)
#         file_name = os.path.splitext(file_name_with_extension)[0]

#         # Replace hyphens with spaces in the filename for Obsidian-style links
#         obsidian_link = file_name.replace('-', ' ')
        
#         # Return the Obsidian-style link
#         print(f"Converted link: [{link_text}] -> [[{obsidian_link}]]")
#         return f"[[{obsidian_link}]]"

#     # Use re.sub to replace all GitHub markdown links with Obsidian links
#     return re.sub(pattern, replace_link, text)

# # Function to recursively find all markdown files in a directory
# def find_all_md_files(root_dir):
#     md_files = []
#     for subdir, _, files in os.walk(root_dir):
#         for file in files:
#             if file.endswith(".md"):
#                 md_files.append(os.path.join(subdir, file))
#     # Debug: Print all found markdown files
#     print(f"Found markdown files: {md_files}")
#     return md_files

# # Function to process each markdown file and convert GitHub links back to Obsidian-style links
# def process_md_files_for_obsidian_links(root_dir):
#     # Find all markdown files
#     all_md_files = find_all_md_files(root_dir)

#     # Process each markdown file
#     for md_file in all_md_files:
#         try:
#             with open(md_file, 'r', encoding='utf-8') as f:
#                 content = f.read()

#             # Convert the GitHub markdown links back to Obsidian-style links
#             updated_content = convert_github_to_obsidian(content)

#             # If content has been updated, write it back to the file
#             if updated_content != content:
#                 with open(md_file, 'w', encoding='utf-8') as f:
#                     f.write(updated_content)
#                 print(f"Updated links in {md_file}")
#             else:
#                 print(f"No changes needed in {md_file}")

#         except Exception as e:
#             # Print error message and continue with other files
#             print(f"Error processing file {md_file}: {e}")

# # Main function to run the script
# if __name__ == "__main__":
#     # Set the root directory to the location of your local markdown files
#     root_directory = r"C:\Users\devil\Downloads\ubuntu_backup\system_design_interview_prep"

#     # Process all markdown files in the directory for converting GitHub links back to Obsidian links
#     process_md_files_for_obsidian_links(root_directory)

import os
import re

# Function to convert GitHub markdown links back to Obsidian-style [[link]]
def convert_github_to_obsidian(text, repo_url):
    # This regex pattern matches GitHub markdown links with your specific URL like [text](https://github.com/.../filename.md)
    pattern = r'\[([^\]]+)\]\(({}[^\)]+)\)'.format(re.escape(repo_url))

    def replace_link(match):
        link_text = match.group(1)
        link_url = match.group(2)

        # Extract the filename from the URL (remove any path before the filename)
        file_name_with_extension = os.path.basename(link_url)
        file_name = os.path.splitext(file_name_with_extension)[0]

        # Replace hyphens with spaces in the filename for Obsidian-style links
        obsidian_link = file_name.replace('-', ' ')

        # Return the Obsidian-style link
        print(f"Converted link: [{link_text}] -> [[{obsidian_link}]]")
        return f"[[{obsidian_link}]]"

    # Use re.sub to replace all GitHub markdown links with Obsidian links
    return re.sub(pattern, replace_link, text)

# Function to process each markdown file and convert GitHub links back to Obsidian-style links
def process_md_files_for_obsidian_links(root_dir, repo_url):
    # Find all markdown files
    all_md_files = find_all_md_files(root_dir)

    # Process each markdown file
    for md_file in all_md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Convert the GitHub markdown links back to Obsidian-style links
            updated_content = convert_github_to_obsidian(content, repo_url)

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

# Function to recursively find all markdown files in a directory
def find_all_md_files(root_dir):
    md_files = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(subdir, file))
    return md_files

# Main function to run the script
if __name__ == "__main__":
    # Set the root directory to the location of your local markdown files
    root_directory = r"C:\Users\devil\Downloads\ubuntu_backup\system_design_interview_prep"

    # Set the base URL of your GitHub repository (only links containing this URL will be converted)
    github_repo_url = r"https://github.com/SathishKumar9866/system-design-interview-prep"

    # Process all markdown files in the directory for converting GitHub links back to Obsidian links
    process_md_files_for_obsidian_links(root_directory, github_repo_url)
