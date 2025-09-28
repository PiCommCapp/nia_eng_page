# NIA Engineering Portal - Technical Documentation

## Project Overview

The NIA Engineering Portal is a fast, offline-capable web application designed to provide quick access to engineering systems during critical operations. The portal is built as a multi-page application with hierarchical navigation optimized for desktop engineering workstations.

## Architecture

### Site Structure

The portal follows a hierarchical navigation structure:

```
pages/
├── index.html (main landing page)
├── plenary/
│   ├── index.html (plenary main page)
│   ├── operator.html
│   └── engineer.html
├── committees/
│   ├── index.html (committee selection)
│   ├── cr21/
│   │   ├── index.html (CR21 main page)
│   │   ├── operator.html
│   │   └── engineer.html
│   ├── cr29/
│   │   ├── index.html (CR29 main page)
│   │   ├── operator.html
│   │   └── engineer.html
│   ├── cr30/
│   │   ├── index.html (CR30 main page)
│   │   ├── operator.html
│   │   └── engineer.html
│   └── senate/
│       ├── index.html (Senate main page)
│       ├── operator.html
│       └── engineer.html
└── engineering/
    ├── index.html
    └── [other engineering pages]
```

### Navigation Flow

1. **Index Page**: Main landing with navigation to all sections
2. **Committee Selection**: Choose between Plenary, Committees, Engineering
3. **Room Selection**: Choose specific committee room (CR21, CR29, CR30, Senate)
4. **Role Selection**: Choose Engineer or Operator role
5. **Role Page**: Access to all systems for that specific role

### Design Principles

- **Functionality First**: Quick access in critical situations
- **Visual Clarity**: Large, clearly marked buttons
- **Color Coding**: Category-based identification
- **Desktop Optimization**: No mobile considerations needed
- **Simplicity**: Manual HTML maintenance for speed

## Implementation Status

### Completed Features

- ✅ Multi-page architecture with hierarchical navigation
- ✅ Role-based access (Operator/Engineer)
- ✅ Committee room organization (CR21, CR29, CR30, Senate)
- ✅ Responsive CSS layout
- ✅ JavaScript functionality for navigation
- ✅ Service worker for offline capabilities
- ✅ Search functionality
- ✅ Bookmark parsing and organization

### Current Implementation

The portal is currently implemented with:

- **HTML**: Semantic structure with accessibility features
- **CSS**: Responsive design with desktop optimization
- **JavaScript**: Vanilla JS for navigation and search
- **Service Worker**: Offline caching and functionality
- **Data Source**: `pages.md` as primary content source

## Technical Specifications

### Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ features with appropriate fallbacks
- Service Worker support for offline functionality

### Performance Requirements

- Page load times under 2 seconds
- Smooth navigation transitions
- Efficient memory usage
- Offline functionality after initial load

### Accessibility

- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support

## Development Environment

### Setup

```bash
# Install dependencies
npm install

# Start development server
npm start

# Convert bookmarks (if needed)
npm run convert
```

### File Organization

- `pages/`: Main application files
- `docs/`: Documentation and planning
- `scripts/`: Utility scripts
- `css/`: Stylesheets
- `js/`: JavaScript files

## Data Management

### Content Source

The portal uses `pages.md` as the primary data source for:

- System links and organization
- Committee room structure
- Role-based content filtering
- Navigation hierarchy

### Maintenance Process

1. Update `pages.md` with new systems or changes
2. Manually update HTML files as needed
3. Test changes locally
4. Deploy updated files

## Future Development

### Phase 2: Automation

- n8n workflow integration
- Automated system monitoring
- Status updates and alerts
- Command execution framework

### Desktop Application

- System tray integration
- Background service
- Auto-start functionality
- Cross-platform support

## Security Considerations

- Local file access only
- No external dependencies
- Offline-first design
- Minimal attack surface

## Troubleshooting

### Common Issues

1. **Service Worker Issues**: Clear browser cache and reload
2. **Navigation Problems**: Check JavaScript console for errors
3. **Offline Functionality**: Ensure service worker is registered
4. **Search Issues**: Verify bookmark data is loaded correctly

### Debug Mode

Enable debug mode by adding `?debug=1` to any URL to see:

- Console logging
- Service worker status
- Data loading information
- Performance metrics

## Performance Optimization

### Implemented Optimizations

- Critical CSS inlined
- Lazy loading for non-essential content
- Efficient DOM manipulation
- Minimal JavaScript footprint
- Service worker caching

### Monitoring

- First contentful paint tracking
- Navigation performance metrics
- Offline functionality testing
- User interaction analytics

## Maintenance Guidelines

### Regular Tasks

- Review and update system links
- Test offline functionality
- Validate accessibility compliance
- Update documentation as needed

### Content Updates

- Add new systems to appropriate committee room pages
- Update role-specific content as needed
- Maintain consistent navigation structure
- Test all links regularly

## Support

For technical support or questions:

- Check this documentation first
- Review the troubleshooting section
- Test in different browsers
- Verify offline functionality

---

_Last Updated: Current Session_
_Version: 1.0_
