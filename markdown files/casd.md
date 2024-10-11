### Reverse Conversion: GitHub Links to Obsidian Links

To reverse the process of converting GitHub links back to Obsidian-style `[[...]]` links, we can modify the script to:

1. **Identify GitHub markdown links** like `[[filename]]`.
2. **Extract the filename from the URL**.
3. **Convert the filename back to the Obsidian link format** `[[filename]]`.

Here's the code that reverses GitHub links to Obsidian links:

```python
import os
import re

# Function to convert GitHub markdown links back to Obsidian-style [[link]]
def convert_github_to_obsidian(text):
    # This regex pattern matches GitHub markdown links like [[filename]]
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'

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
def process_md_files_for_obsidian_links(root_dir):
    # Find all markdown files
    all_md_files = find_all_md_files(root_dir)

    # Process each markdown file
    for md_file in all_md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Convert the GitHub markdown links back to Obsidian-style links
            updated_content = convert_github_to_obsidian(content)

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

    # Process all markdown files in the directory for converting GitHub links back to Obsidian links
    process_md_files_for_obsidian_links(root_directory)
```

### How This Works:

1. **`convert_github_to_obsidian`**:
   - This function scans the markdown text for GitHub markdown links and converts them back into Obsidian-style `[[filename]]` links.
   - It extracts the filename from the GitHub URL and formats it for Obsidian by replacing hyphens (`-`) with spaces.

2. **`process_md_files_for_obsidian_links`**:
   - This function processes all markdown files in the given directory and applies the conversion to each file, saving the changes back.

### Example:

#### Before:

```markdown
Here is a link to [Common-Principles](https://github.com/SathishKumar9866/system-design-interview-prep/blob/backlinks_test/../basic/prep/Common-Principles.md).
```

#### After:

```markdown
Here is a link to [Common-Principles](https://github.com/SathishKumar9866/system-design-interview-prep/blob/backlinks_test/../basic/prep/Common-Principles.md).
```

---

## File Naming Conventions and Software Principles for Maintenance

### Overview

Maintaining a large-scale software project requires adherence to certain principles and best practices to ensure clarity, consistency, and long-term sustainability. The following guidelines cover **file naming conventions**, **formatting rules**, and **ethical principles** for code maintenance, with a focus on scalability and collaboration.

### 1. **File Naming Conventions**

#### a. **Use Hyphens for Separators**
- **File names** should use hyphens (`-`) to separate words, instead of spaces or underscores.
- This makes file paths URL-friendly and consistent across systems.
- **Example**:  
  - `Common-Principles.md` (correct)  
  - `Common Principles.md` (incorrect)

#### b. **Be Descriptive and Concise**
- File names should be **clear** and **descriptive** to reflect the content accurately, while avoiding unnecessary verbosity.
- Avoid using generic names like `doc1.md` or `notes.md`.
- **Example**:  
  - `API-Integration-Guide.md` (correct)  
  - `guide.md` (too vague)

#### c. **Consistent Case Usage**
- Use **lowercase letters** with hyphens for multi-word file names.
- Avoid mixing cases, as it can lead to inconsistencies on case-sensitive file systems (e.g., Linux).
- **Example**:  
  - `data-processing-overview.md` (correct)  
  - `DataProcessingOverview.md` (inconsistent)

#### d. **Avoid Special Characters**
- Do not use special characters (e.g., `&`, `%`, `@`, etc.) in file names.
- Stick to **alphanumeric characters** and hyphens.

---

### 2. **Link Formatting**

#### a. **Internal Links (Obsidian)**
- Use Obsidian-style `[[...]]` links for internal references within markdown files.
- Ensure that all internal links use the hyphenated file names and follow the correct case.
- **Example**:  
  - `[[API-Integration-Guide]]`

#### b. **External Links (GitHub)**
- When linking to files from GitHub, use the full GitHub URL in markdown format:
- **Example**:  
  - `[[API Integration Guide]]`

---

### 3. **Version Control and Collaboration**

#### a. **Commit Messages**
- Write **meaningful** commit messages that explain the purpose of the change.
- Follow this format: `category: description`.
  - **Categories**: `feat` (feature), `fix` (bug fix), `docs` (documentation), `refactor` (code restructuring), etc.
- **Example**:  
  - `feat: add API integration guide`
  - `fix: correct file paths in the user guide`

#### b. **Branching Strategy**
- Use a **feature branch** workflow to keep the `main` branch stable:
  1. Create a new branch for each feature or bug fix.
  2. Merge the branch into `main` only after review and testing.

---

### 4. **Code Formatting and Structure**

#### a. **Consistent Indentation**
- Use consistent indentation throughout your code, preferably **4 spaces** per indentation level.
- Avoid mixing tabs and spaces in a single project.

#### b. **Modularization**
- Break your code into small, reusable **modules** and **functions**. This enhances readability and makes it easier to test and maintain.

#### c. **Documentation**
- Every file, function, and class should be documented with **clear and concise comments**.
- For functions, include:
  1. **Description** of what the function does.
  2. **Parameters** and their expected types.
  3. **Return values**, if applicable.

---

### 5. **Ethical Principles for Maintenance**

#### a. **Simplicity and Clarity**
- Strive for **simple**, **clean**, and **self-explanatory** code. Code that is easy to read and understand is easier to maintain in the long run.

#### b. **Ownership and Accountability**
- Every developer is accountable for the code they write. Ensure that you understand the code you are working on and take ownership of its quality.

#### c. **Knowledge Sharing**
- Share knowledge with your team, whether through code comments, documentation, or discussions.
- Avoid creating "knowledge silos" where only one person knows how a certain part of the codebase works.

#### d. **Continuous Refactoring**
- As your project grows, **refactor** regularly to improve code structure without changing its external behavior.
- Don't be afraid to make changes that improve readability, performance, or organization.

---

### 6. **Long-term Sustainability**

#### a. **Test Coverage**
- Ensure your code has sufficient test coverage, with a particular focus on critical components.
- Include **unit tests**, **integration tests**, and **end-to-end tests** where applicable.

#### b. **Backward Compatibility**
- Maintain backward compatibility where possible. Ensure that changes do not break existing functionality without good reason.

#### c. **Scalability**
- Always keep scalability in mind. Design your code in a way that it can grow and evolve with the project’s requirements.
  
---

### Conclusion

By adhering to these guidelines, you ensure that your software is maintainable, scalable, and collaborative. Following clear file naming conventions, using consistent formatting, and applying ethical principles to code maintenance will contribute to the long-term success of your project.

---

This document provides a foundation for maintaining large-scale software projects, focusing on file naming conventions, link formatting, and broader principles for code management and collaboration.

Would

 you like to refine or expand any section of this document?