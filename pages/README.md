# NIA Engineering Portal - Pages

This directory contains all the HTML pages and CSS for the NIA Engineering Portal.

## Structure

```
pages/
├── index.html          # Main landing page
├── plenary.html        # Plenary operations
├── committees.html     # Committee room selection
├── cr21.html          # Committee Room 21
├── engineering.html   # Engineering systems
├── css/
│   └── main.css       # Main stylesheet
├── js/
│   ├── bookmarks-parser.js      # Data extraction from pages.md
│   ├── service-worker.js        # Offline capability
│   └── service-worker-register.js # Service worker registration
└── README.md          # This file
```

## Navigation

- **index.html** - Main entry point with navigation to all sections
- **plenary.html** - Plenary operations with Operator/Engineer role selection
- **committees.html** - Committee room selection (CR21, CR29, CR30, Senate)
- **cr21.html** - Committee Room 21 with role-specific content
- **engineering.html** - Technical systems and infrastructure

## Design Principles

- **Speed First**: Minimal JavaScript, inline CSS for critical rendering
- **Crisis-Ready**: Intuitive navigation during high-stress situations
- **Role-Based**: Content filtered by Operator/Engineer roles
- **Offline Capable**: Works without internet connection
- **Mobile Responsive**: Adapts to different screen sizes

## Maintenance

Pages are manually maintained using `pages.md` as the source of truth. Each page contains:

- Role selection interfaces
- System-specific links and cameras
- Breadcrumb navigation
- Online/offline status indicators

## CSS

The `css/main.css` file contains all shared styles using CSS custom properties for consistent theming across all pages.
