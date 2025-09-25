# Technical Context

## Core Technologies

### Phase 1
- **HTML5**: Static interface with modern HTML5 features
- **CSS3**: Clean, responsive styling
- **JavaScript**: Minimal enhancements for quick loading
- **Local File Deployment**: No web server required

### Phase 2
- **n8n**: Workflow automation platform
- **Docker**: Containerized deployment of n8n
- **PostgreSQL**: Database for n8n workflows
- **SSH**: Remote command execution

## File Structure
- `index.html` - Main engineering portal
- `bookmarks.html` - Source data for system links (exported from browser)
- `compose.yml` - n8n Docker configuration
- `.env.sample` - Environment configuration template
- `.env` - Active environment configuration (not in version control)

## Environment Setup
1. **Basic Setup (Phase 1)**
   - Clone repository to each engineering PC
   - Open `index.html` in any web browser
   - No build steps or server required

2. **n8n Setup (Phase 2)**
   - Docker and Docker Compose required
   - Copy `.env.sample` to `.env` and configure
   - Run `docker-compose up -d` to start n8n
   - n8n accessible on configured port (default: 5678)

## Network Requirements
- Local network access to all managed devices
- No internet access required for basic functionality
- n8n server should have SSH access to target systems

## Security Considerations
- No authentication in Phase 1 (physical access security)
- n8n credentials stored in `.env` (not in version control)
- Consider firewall rules to restrict n8n access to authorized IPs
- All passwords and sensitive data must be stored in n8n credentials, not workflows

## Performance Optimizations
- Minimal JavaScript to ensure fastest possible loading
- Static HTML generation from bookmarks
- Preload critical assets
- No external dependencies or CDNs
