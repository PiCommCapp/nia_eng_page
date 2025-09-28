# Bookmarks Conversion Plan

## Overview

Converting the existing `bookmarks.html` file to a more manageable markdown format will allow for easier editing, version control, and generation of the engineering portal interface.

## Conversion Process

### 1. Extract Structure from HTML

- Parse the existing bookmarks.html file using our BookmarksParser
- Identify all categories, subcategories, and links
- Extract metadata (URLs, titles, icons, etc.)

### 2. Define Markdown Format

We'll use the following format for our bookmark markdown:

```markdown
# Category Name

## Subcategory Name

### [System Name](https://system-url.com)

- **IP/Hostname:** system-hostname
- **Type:** System Type
- **Notes:** Additional information

### [Another System](https://another-system.com)

- **IP/Hostname:** another-hostname
- **Type:** Another Type
```

### 3. Create Conversion Script

Create a Node.js script to:

- Read bookmarks.html
- Parse using BookmarksParser
- Transform the data into markdown format
- Write output to a bookmarks.md file

### 4. Add Metadata Enrichment

Enhance the bookmark data with:

- System type categorization
- IP/hostname extraction
- Priority level
- Additional notes field for maintenance info

### 5. Validation

- Ensure all links are preserved
- Validate URLs are correct
- Check that the hierarchy is maintained
- Compare counts of links and categories with original

## Example Conversion

### HTML Source (simplified)

```html
<DT><H3>KVM</H3>
<DL><p>
  <DT><A HREF="http://10.63.81.10/login.php">AIM Main</A>
  <DT><A HREF="http://10.63.81.11/">AIM Reserve</A>
</DL><p>
```

### Markdown Output

```markdown
# KVM

### [AIM Main](http://10.63.81.10/login.php)

- **IP/Hostname:** 10.63.81.10
- **Type:** KVM
- **Category:** Critical Infrastructure

### [AIM Reserve](http://10.63.81.11/)

- **IP/Hostname:** 10.63.81.11
- **Type:** KVM
- **Category:** Critical Infrastructure
```

## Benefits

1. **Easier Editing:** Non-technical staff can edit markdown
2. **Version Control:** Changes tracked in Git
3. **Automation:** Generate HTML from markdown
4. **Extensibility:** Easily add metadata fields
5. **Documentation:** Serves as system documentation

## Implementation Steps

1. Create the conversion script (parser.js)
2. Run initial conversion
3. Review output for accuracy
4. Enhance with additional metadata
5. Create process for future updates
6. Document maintenance procedures

## Maintenance Process

1. Edit the markdown file when systems change
2. Run the build script to generate the HTML interface
3. Test locally before deployment
4. Push changes to the repository
5. Deploy updated files
