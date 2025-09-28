# NIA Engineering Portal - Project Context

## Project Overview

The NIA Engineering Portal is a critical access point for broadcast engineers who need immediate access to infrastructure systems during live operations. When systems fail or need adjustment, every second counts. This portal ensures that engineers can access any required system with minimal clicks and zero delay.

## Core Purpose

The portal serves as a fast, offline-capable web application designed to provide quick access to engineering systems during critical operations. It's built as a multi-page application with hierarchical navigation optimized for desktop engineering workstations.

## User Scenarios

### Scenario 1: Live Broadcast Emergency

During a live broadcast, a gallery monitor displays a "No Signal" error. The engineer needs to:

1. Check the SDI router status
2. Verify KVM connection to affected system
3. Access PDU to power cycle equipment if necessary
4. Access backup systems if primary fails

Without the engineering page, this could take several minutes of navigation through bookmarks, remembering IPs, or consulting documentation. With the engineering page, all required systems are accessible within seconds.

### Scenario 2: Pre-Event Configuration

Before a major broadcast event, engineers need to:

1. Verify all critical systems are online
2. Configure backup routes
3. Ensure redundant systems are in standby
4. Test all gallery displays and control interfaces

The engineering page facilitates this process by grouping related systems together and providing quick access to each component.

### Scenario 3: Remote Support

When on-call engineers are contacted about issues:

1. They need immediate access to systems from their laptops
2. May need to execute common remediation tasks
3. Must verify system status quickly
4. May need to escalate to physical intervention

Phase 2 n8n integration will allow common support tasks to be automated and executed with a single click.

## Success Metrics

### Primary Metrics

- **Time to Access**: How quickly can an engineer access a specific system? (Target: < 3 seconds)
- **Completeness**: What percentage of required systems are accessible? (Target: 100%)
- **Reliability**: Is the portal always available when needed? (Target: 100%)

### Secondary Metrics

- **Usability**: Can new engineers navigate without training? (Target: Yes)
- **Maintenance**: How much effort is required to keep the portal updated? (Target: < 1 hour/month)
- **Automation**: How many routine tasks are automated? (Phase 2 metric)

## Stakeholders

### Primary

- Broadcast engineers
- Technical operations staff
- On-call support staff

### Secondary

- IT support team
- Broadcast management
- Production staff (indirect users)

## Technical Context

### Core Technologies

#### Phase 1 (Current)

- **HTML5**: Static interface with modern HTML5 features
- **CSS3**: Clean, responsive styling
- **JavaScript**: Minimal enhancements for quick loading
- **Local File Deployment**: No web server required

#### Phase 2 (Future)

- **n8n**: Workflow automation platform
- **Docker**: Containerized deployment of n8n
- **PostgreSQL**: Database for n8n workflows
- **SSH**: Remote command execution

### Design Principles

#### Speed-First Architecture

- Prioritize speed over aesthetics
- Minimize HTTP requests
- Inline critical CSS
- Defer non-essential scripts
- Use browser caching

#### Intuitive UX

- Categorize by engineering function
- Use consistent color-coding
- Clear, large click targets
- Minimal hover states
- Search functionality

#### Fail-Safe Design

- Works without server components
- No external dependencies
- Local caching when possible
- Clear error states

## Current Implementation Status

### Completed Features

- ✅ Multi-page architecture with hierarchical navigation
- ✅ Role-based access (Operator/Engineer)
- ✅ Committee room organization (CR21, CR29, CR30, Senate)
- ✅ Responsive CSS layout
- ✅ JavaScript functionality for navigation
- ✅ Service worker for offline capabilities
- ✅ Search functionality
- ✅ Bookmark parsing and organization

### Current Phase

**Phase 1**: Static HTML interface with local deployment

### Key Resources

- `pages/`: Main application files
- `pages.md`: Primary data source for content
- `docs/`: Documentation and planning
- `scripts/`: Utility scripts

## Constraints

### Technical

- Must work offline/locally
- Must function during network degradation
- No external dependencies
- Minimal resource usage

### Operational

- Must be easily updateable by non-developers
- Changes must be quickly deployable to all workstations
- Must accommodate rapid evolution of infrastructure

## Network Requirements

- Local network access to all managed devices
- No internet access required for basic functionality
- n8n server should have SSH access to target systems (Phase 2)

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

---

_Last Updated: Current Session_
_Version: 1.0_
