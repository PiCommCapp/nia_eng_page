# NIA Engineering Page

A lightning-fast, mission-critical engineering portal for broadcast/AV infrastructure access.

## Overview

When seconds matter during system failures, engineers need instant access to device interfaces across complex infrastructure. This portal provides a clean, intuitive interface to all engineering systems without distraction.

## Features

- **Instant Access**: Static HTML interface loads immediately
- **Intuitive Navigation**: Clean categorization of all systems
- **Local Deployment**: Works offline, no external dependencies
- **System Automation**: n8n integration for remote commands (Phase 2)
- **Zero Training**: Engineers can use it immediately

## Quick Start

1. Clone this repository to each engineering PC
2. Open `index.html` in any web browser
3. Access all systems instantly

## System Categories

- **KVM Switches**: AIM Main/Reserve access
- **Network Infrastructure**: Firewalls, Dante audio, control systems
- **Control Rooms**: CAR2, B23 committee rooms
- **Gallery Screens**: PDU management interfaces
- **Support Systems**: Busby admin, documentation

## Architecture

### Phase 1 (Current)
- Static HTML interface derived from `bookmarks.html`
- Local file deployment
- Zero dependencies

### Phase 2 (Planned)
- n8n automation platform
- SSH command automation
- System health monitoring
- Webhook-triggered operations

## Deployment

This is designed for local network deployment:
- No FQDN required
- n8n runs on single PC only
- All other PCs use static HTML interface
- Graceful degradation if n8n unavailable

## Development

- **Speed First**: Every millisecond counts
- **Simplicity**: No complex frameworks
- **Reliability**: Must work during failures
- **Local Focus**: Built for engineering team, not wider audience

## Files

- `index.html` - Main engineering portal
- `bookmarks.html` - Source data for system links
- `compose.yml` - n8n Docker configuration
- `.env.sample` - Environment configuration template

## Philosophy

> "They'll never notice it... until they need it, then it saves the day."

This portal is designed to be invisible during normal operations but indispensable during critical moments.
