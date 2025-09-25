/**
 * NIA Engineering Portal - Bookmarks Converter
 *
 * This script converts the bookmarks.html file to markdown format
 * for easier editing and management.
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// Paths
const BOOKMARKS_HTML_PATH = path.join(__dirname, '..', 'bookmarks.html');
const BOOKMARKS_MD_PATH = path.join(__dirname, '..', 'bookmarks.md');

/**
 * Extract hostname from URL
 * @param {string} url - URL to extract hostname from
 * @returns {string} - Extracted hostname
 */
function extractHostname(url) {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname;
  } catch (e) {
    // If URL parsing fails, return original URL
    return url;
  }
}

/**
 * Guess system type based on URL and title
 * @param {string} url - System URL
 * @param {string} title - System title
 * @returns {string} - Guessed system type
 */
function guessSystemType(url, title) {
  const urlLower = url.toLowerCase();
  const titleLower = title.toLowerCase();

  if (
    urlLower.includes('aim') ||
    titleLower.includes('aim') ||
    titleLower.includes('kvm')
  ) {
    return 'KVM';
  } else if (
    urlLower.includes('fw') ||
    titleLower.includes('fw') ||
    titleLower.includes('firewall')
  ) {
    return 'Firewall';
  } else if (urlLower.includes('dante') || titleLower.includes('dante')) {
    return 'Audio';
  } else if (urlLower.includes('pdu') || titleLower.includes('pdu')) {
    return 'Power';
  } else if (urlLower.includes('core') || titleLower.includes('core')) {
    return 'Network Core';
  } else if (urlLower.includes('edge') || titleLower.includes('edge')) {
    return 'Network Edge';
  } else if (urlLower.includes('busby') || titleLower.includes('busby')) {
    return 'Admin';
  } else if (
    urlLower.includes('cr') ||
    titleLower.includes('cr') ||
    urlLower.includes('car') ||
    titleLower.includes('car') ||
    urlLower.includes('committee') ||
    titleLower.includes('committee')
  ) {
    return 'Control Room';
  } else {
    return 'Other';
  }
}

/**
 * Determine priority level based on system type and URL
 * @param {string} type - System type
 * @param {string} url - System URL
 * @returns {string} - Priority level
 */
function determinePriority(type, url) {
  if (type === 'KVM' || type === 'Network Core' || url.includes('main')) {
    return 'Critical';
  } else if (type === 'Control Room' || type === 'Network Edge') {
    return 'High';
  } else if (type === 'Power' || type === 'Audio') {
    return 'Medium';
  } else {
    return 'Normal';
  }
}

/**
 * Convert a bookmark folder to markdown
 * @param {Element} folderElement - Folder element (DL)
 * @param {number} level - Heading level
 * @param {string} parentTitle - Title of parent folder
 * @returns {string} - Markdown representation of folder
 */
function folderToMarkdown(folderElement, level = 1, parentTitle = '') {
  let markdown = '';
  const children = Array.from(folderElement.children);

  // Current folder info
  let currentFolderTitle = '';
  let isCategory = false;

  // Process DT elements
  for (let i = 0; i < children.length; i++) {
    const child = children[i];

    // Skip non-element nodes
    if (child.nodeType !== 1) continue;

    // Process DT element
    if (child.tagName === 'DT') {
      // Check if it's a folder (has H3)
      const h3 = child.querySelector('H3');
      if (h3) {
        const folderTitle = h3.textContent.trim();
        currentFolderTitle = folderTitle;
        isCategory = true;

        // Add heading
        markdown += `${'#'.repeat(level)} ${folderTitle}\n\n`;

        // Process nested folder
        const dl = child.querySelector('DL');
        if (dl) {
          markdown += folderToMarkdown(dl, level + 1, folderTitle);
        }
      } else {
        // It's a link
        const a = child.querySelector('A');
        if (a) {
          const linkTitle = a.textContent.trim();
          const linkUrl = a.getAttribute('href');
          const hostname = extractHostname(linkUrl);
          const type = guessSystemType(linkUrl, linkTitle);
          const priority = determinePriority(type, linkUrl);

          // Add link
          markdown += `${'#'.repeat(level + 1)} [${linkTitle}](${linkUrl})\n`;
          markdown += `- **IP/Hostname:** ${hostname}\n`;
          markdown += `- **Type:** ${type}\n`;
          markdown += `- **Priority:** ${priority}\n`;
          markdown += `- **Category:** ${isCategory ? currentFolderTitle : parentTitle}\n\n`;
        }
      }
    }
  }

  return markdown;
}

/**
 * Convert bookmarks HTML to markdown
 * @param {string} html - Bookmarks HTML content
 * @returns {string} - Markdown representation
 */
function convertBookmarksToMarkdown(html) {
  // Parse HTML
  const dom = new JSDOM(html);
  const document = dom.window.document;

  // Find Bookmarks bar
  const h3Elements = Array.from(document.querySelectorAll('H3'));
  const bookmarksBarH3 = h3Elements.find((h3) =>
    h3.textContent.includes('Bookmarks bar'),
  );

  if (!bookmarksBarH3) {
    throw new Error('Could not find Bookmarks bar');
  }

  // Find the parent DT and then its parent DL
  const parentDT = bookmarksBarH3.parentElement;
  const parentDL = parentDT.querySelector('DL');

  if (!parentDL) {
    throw new Error('Could not find bookmarks folder');
  }

  // Generate markdown
  let markdown = '# NIA Engineering Systems\n\n';
  markdown +=
    '_This file is automatically generated from bookmarks.html. Do not edit directly._\n\n';
  markdown += '## Table of Contents\n\n';

  // Get top-level categories for TOC
  const topLevelCategories = Array.from(
    parentDL.querySelectorAll(':scope > DT > H3'),
  ).map((h3) => h3.textContent.trim());

  // Add TOC entries
  topLevelCategories.forEach((category) => {
    markdown += `- [${category}](#${category.toLowerCase().replace(/\s+/g, '-')})\n`;
  });

  markdown += '\n---\n\n';

  // Convert folders to markdown
  markdown += folderToMarkdown(parentDL);

  return markdown;
}

/**
 * Main function
 */
async function main() {
  try {
    console.log(`Reading bookmarks HTML from ${BOOKMARKS_HTML_PATH}`);
    const html = fs.readFileSync(BOOKMARKS_HTML_PATH, 'utf8');

    console.log('Converting to markdown');
    const markdown = convertBookmarksToMarkdown(html);

    console.log(`Writing markdown to ${BOOKMARKS_MD_PATH}`);
    fs.writeFileSync(BOOKMARKS_MD_PATH, markdown, 'utf8');

    console.log('Conversion complete!');
  } catch (error) {
    console.error('Error converting bookmarks:', error);
    process.exit(1);
  }
}

// Run the script
main();
