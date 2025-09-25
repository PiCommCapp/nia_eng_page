/**
 * NIA Engineering Portal - Bookmarks Parser
 *
 * This script parses the bookmarks.html file and extracts all links and categories.
 * It then organizes them into a structured format for use in the main interface.
 */

class BookmarksParser {
    constructor() {
        this.bookmarksData = null;
        this.categories = [];
    }

    /**
     * Load and parse bookmarks from the HTML file
     * @param {string} filePath - Path to the bookmarks.html file
     * @returns {Promise} - Promise that resolves when parsing is complete
     */
    async loadBookmarks(filePath = 'bookmarks.html') {
        try {
            const response = await fetch(filePath);
            if (!response.ok) {
                throw new Error(`Failed to load bookmarks: ${response.status} ${response.statusText}`);
            }

            const html = await response.text();
            this.parseBookmarksHtml(html);
            return this.categories;
        } catch (error) {
            console.error('Error loading bookmarks:', error);
            throw error;
        }
    }

    /**
     * Parse bookmarks HTML content
     * @param {string} html - HTML content from bookmarks file
     */
    parseBookmarksHtml(html) {
        // Create a DOM parser
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');

        // Find all DL elements (bookmark folders)
        const bookmarksBar = Array.from(doc.querySelectorAll('DL > p')).find(p => {
            const h3 = p.previousElementSibling;
            return h3 && h3.textContent.includes('Bookmarks bar');
        });

        if (!bookmarksBar) {
            console.error('Could not find Bookmarks bar');
            return;
        }

        // Get parent DL element
        const topLevelDL = bookmarksBar.parentElement;

        // Parse the structure
        this.parseBookmarkFolder(topLevelDL);
    }

    /**
     * Parse a bookmark folder
     * @param {Element} folderElement - The DL element representing a folder
     * @param {string} parentCategory - Parent category name
     */
    parseBookmarkFolder(folderElement, parentCategory = null) {
        // Get all direct children of the folder
        const children = folderElement.children;

        let currentCategory = parentCategory;

        // Iterate through children
        for (let i = 0; i < children.length; i++) {
            const child = children[i];

            // Skip non-element nodes
            if (child.nodeType !== Node.ELEMENT_NODE) continue;

            // If it's a DT element
            if (child.tagName === 'DT') {
                // Check for folder (H3)
                const h3 = child.querySelector('H3');
                if (h3) {
                    const folderName = h3.textContent.trim();
                    const folderDL = child.querySelector('DL');

                    if (folderDL) {
                        // Create a new category
                        const category = {
                            name: folderName,
                            links: [],
                            subcategories: []
                        };

                        // If we have a parent, add it as a subcategory
                        if (parentCategory) {
                            const parent = this.findCategory(parentCategory);
                            if (parent) {
                                parent.subcategories.push(category);
                            }
                        } else {
                            // Top level category
                            this.categories.push(category);
                        }

                        // Parse the folder recursively
                        this.parseBookmarkFolder(folderDL, folderName);
                    }
                } else {
                    // Check for link (A)
                    const a = child.querySelector('A');
                    if (a && currentCategory) {
                        const link = {
                            title: a.textContent.trim(),
                            url: a.href,
                            icon: a.getAttribute('ICON'),
                            dateAdded: a.getAttribute('ADD_DATE')
                        };

                        // Add link to the current category
                        const category = this.findCategory(currentCategory);
                        if (category) {
                            category.links.push(link);
                        }
                    }
                }
            }
        }
    }

    /**
     * Find a category by name
     * @param {string} name - Category name to find
     * @param {Array} categories - Categories to search in (defaults to top level)
     * @returns {Object|null} - Found category or null
     */
    findCategory(name, categories = this.categories) {
        // Search in provided categories
        for (const category of categories) {
            if (category.name === name) {
                return category;
            }

            // Search in subcategories
            if (category.subcategories && category.subcategories.length > 0) {
                const found = this.findCategory(name, category.subcategories);
                if (found) return found;
            }
        }

        return null;
    }

    /**
     * Get all categories as a flat array
     * @returns {Array} - All categories
     */
    getAllCategories() {
        const result = [];

        const flattenCategories = (categories, depth = 0) => {
            for (const category of categories) {
                result.push({
                    ...category,
                    depth
                });

                if (category.subcategories && category.subcategories.length > 0) {
                    flattenCategories(category.subcategories, depth + 1);
                }
            }
        };

        flattenCategories(this.categories);
        return result;
    }

    /**
     * Search for links matching a query
     * @param {string} query - Search query
     * @returns {Array} - Matching links with their categories
     */
    search(query) {
        const results = [];
        const normalizedQuery = query.toLowerCase();

        const searchInCategory = (category, breadcrumb = []) => {
            // Current path to this category
            const path = [...breadcrumb, category.name];

            // Search in links
            for (const link of category.links) {
                if (link.title.toLowerCase().includes(normalizedQuery) ||
                    link.url.toLowerCase().includes(normalizedQuery)) {
                    results.push({
                        link,
                        category: category.name,
                        path
                    });
                }
            }

            // Search in subcategories
            for (const subcategory of category.subcategories) {
                searchInCategory(subcategory, path);
            }
        };

        // Start search from top-level categories
        for (const category of this.categories) {
            searchInCategory(category);
        }

        return results;
    }
}

// Export the class
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BookmarksParser;
} else {
    window.BookmarksParser = BookmarksParser;
}
