# System Patterns

## Design Principles

### Speed-First Architecture
- Prioritize speed over aesthetics
- Minimize HTTP requests
- Inline critical CSS
- Defer non-essential scripts
- Use browser caching

### Intuitive UX
- Categorize by engineering function
- Use consistent color-coding
- Clear, large click targets
- Minimal hover states
- Search functionality

### Fail-Safe Design
- Works without server components
- No external dependencies
- Local caching when possible
- Clear error states

## Component Patterns

### Navigation
- Top-level categories with icon + text
- Expandable subcategories
- Recently used section
- Search always available
- Breadcrumb navigation

### Link Display
- Consistent card-based design
- Visual indicators for system type
- Status indicators when available
- Click area covers entire card
- Quick-copy IP address feature

### System Status (Phase 2)
- Color-coded status indicators
- Last checked timestamp
- Manual refresh button
- Automatic background checking

## Code Patterns

### HTML Structure
```html
<section class="category">
  <h2>Category Name</h2>
  <div class="links">
    <a href="url" class="link-card">
      <span class="system-name">System Name</span>
      <span class="system-details">Details</span>
    </a>
    <!-- More link cards -->
  </div>
</section>
```

### CSS Architecture
- Mobile-first design
- CSS custom properties for theming
- BEM naming convention
- Minimal specificity
- Utility classes for common patterns

### JavaScript Patterns
- Vanilla JS, no frameworks
- Event delegation for performance
- Local storage for preferences
- Feature detection, not browser detection
- Error handling with fallbacks

## n8n Workflow Patterns (Phase 2)

### System Checks
- Regular polling of critical systems
- Threshold-based alerting
- Status logging
- Failure recovery automation

### Command Execution
- Template-based SSH commands
- Pre-execution validation
- Execution logging
- Confirmation of success

### Authentication
- Credential storage in n8n
- Role-based access control
- Audit logging
- Session management
