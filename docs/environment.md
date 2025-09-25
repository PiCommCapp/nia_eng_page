# Environment Setup Guide

## Phase 1: Static HTML Development

### Prerequisites
- Git for version control
- Web browser (Chrome, Firefox, Edge, or Safari)
- Text editor or IDE (VSCode recommended)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/nia_eng_page.git
   cd nia_eng_page
   ```

2. Open `index.html` directly in your browser:
   ```bash
   # On Linux
   xdg-open index.html
   
   # On macOS
   open index.html
   
   # On Windows
   start index.html
   ```

3. For development, consider using a simple local server:
   ```bash
   # Using Python
   python3 -m http.server
   
   # Using Node.js
   npx serve
   ```

### Development Workflow
1. Edit HTML, CSS, and JavaScript files directly
2. Refresh browser to see changes
3. Commit changes to Git repository
4. Push to central repository for deployment

## Phase 2: n8n Development

### Prerequisites
- Docker and Docker Compose
- Git for version control
- Terminal access with appropriate permissions

### Docker Setup

1. Install Docker and Docker Compose:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install docker.io docker-compose
   
   # Fedora/RHEL
   sudo dnf install docker docker-compose
   
   # macOS/Windows
   # Download from https://www.docker.com/products/docker-desktop
   ```

2. Configure environment:
   ```bash
   # Copy example configuration
   cp .env.sample .env
   
   # Edit configuration with your settings
   nano .env
   ```

3. Start the Docker containers:
   ```bash
   # Start in detached mode
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   ```

4. Access n8n:
   - Open browser to `http://localhost:5678` (or configured port)
   - Set up initial n8n account
   - Begin creating workflows

### Important Directories and Files

- `compose.yml`: Docker Compose configuration
- `.env`: Environment variables (not in version control)
- `.env.sample`: Example environment variables
- `conf/`: Configuration files for services
- `index.html`: Main entry point for the static interface

### Security Notes

1. Never commit `.env` file to version control
2. Use strong passwords for database and n8n
3. Consider restricting network access to n8n service
4. Store sensitive credentials only in n8n credential store
5. Regularly update Docker images for security patches

### Backup and Maintenance

1. Backup n8n data:
   ```bash
   # Export n8n workflows and credentials
   docker-compose exec n8n n8n export:workflow --all --output=/backups/workflows.json
   ```

2. Update containers:
   ```bash
   # Pull latest images and restart
   docker-compose pull
   docker-compose down
   docker-compose up -d
   ```

3. Troubleshooting:
   ```bash
   # View logs
   docker-compose logs -f
   
   # Restart services
   docker-compose restart
   
   # Check container status
   docker-compose ps
   ```
