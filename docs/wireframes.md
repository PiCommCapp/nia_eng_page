# NIA Engineering Portal Wireframes

## Desktop Layout

```
+---------------------------------------------------------------+
|  LOGO   NIA ENGINEERING PORTAL                [ONLINE STATUS] |
+---------------------------------------------------------------+
|  [Search systems...]                                          |
+---------------------------------------------------------------+
|                                                               |
|  +-------------------+  +-------------------+  +------------+ |
|  | CATEGORY 1        |  | CATEGORY 2        |  | CATEGORY 3 | |
|  |                   |  |                   |  |            | |
|  | [System 1]        |  | [System 4]        |  | [System 7] | |
|  | [System 2]        |  | [System 5]        |  | [System 8] | |
|  | [System 3]        |  | [System 6]        |  | [System 9] | |
|  |                   |  |                   |  |            | |
|  +-------------------+  +-------------------+  +------------+ |
|                                                               |
|  +-------------------+  +-------------------+                 |
|  | CATEGORY 4        |  | CATEGORY 5        |                 |
|  |                   |  |                   |                 |
|  | [System 10]       |  | [System 13]       |                 |
|  | [System 11]       |  | [System 14]       |                 |
|  | [System 12]       |  | [System 15]       |                 |
|  |                   |  |                   |                 |
|  +-------------------+  +-------------------+                 |
|                                                               |
+---------------------------------------------------------------+
|  Press ? for keyboard shortcuts                               |
+---------------------------------------------------------------+
```

## Mobile Layout

```
+------------------------+
| NIA ENGINEERING PORTAL |
+------------------------+
| [Search systems...]    |
+------------------------+
| CATEGORY 1           > |
+------------------------+
| CATEGORY 2           > |
+------------------------+
| CATEGORY 3           > |
+------------------------+
| CATEGORY 4           > |
+------------------------+
| CATEGORY 5           > |
+------------------------+
```

### Mobile Category View

```
+------------------------+
| < BACK    CATEGORY 1   |
+------------------------+
| [System 1]             |
|  10.63.81.10           |
|  KVM                   |
+------------------------+
| [System 2]             |
|  10.63.81.11           |
|  KVM                   |
+------------------------+
| [System 3]             |
|  10.63.81.12           |
|  Network               |
+------------------------+
```

## System Card Component

```
+------------------------+
| System Name            |
| IP: 10.63.81.10        |
| Type: KVM              |
+------------------------+
```

## Search Results

```
+---------------------------------------------------------------+
|  LOGO   NIA ENGINEERING PORTAL                [ONLINE STATUS] |
+---------------------------------------------------------------+
|  [kvm] X                                                      |
+---------------------------------------------------------------+
|                                                               |
|  SEARCH RESULTS                                               |
|                                                               |
|  +-------------------+  +-------------------+                 |
|  | AIM Main          |  | AIM Reserve       |                 |
|  | 10.63.81.10       |  | 10.63.81.11       |                 |
|  | KVM               |  | KVM               |                 |
|  | Category: KVM     |  | Category: KVM     |                 |
|  +-------------------+  +-------------------+                 |
|                                                               |
+---------------------------------------------------------------+
```

## Loading State

```
+---------------------------------------------------------------+
|  LOGO   NIA ENGINEERING PORTAL                [OFFLINE]       |
+---------------------------------------------------------------+
|  [Search systems...]                                          |
+---------------------------------------------------------------+
|                                                               |
|              Loading system categories...                     |
|              [Progress Indicator]                             |
|                                                               |
+---------------------------------------------------------------+
```

## Error State

```
+---------------------------------------------------------------+
|  LOGO   NIA ENGINEERING PORTAL                [OFFLINE]       |
+---------------------------------------------------------------+
|  [Search systems...]                                          |
+---------------------------------------------------------------+
|                                                               |
|  /!\  Error loading systems                                   |
|                                                               |
|  Could not load bookmarks data.                               |
|  [Retry]                                                      |
|                                                               |
+---------------------------------------------------------------+
```

## Keyboard Shortcuts Help

```
+---------------------------------------------------------------+
|  LOGO   NIA ENGINEERING PORTAL                [ONLINE]        |
+---------------------------------------------------------------+
|  [Search systems...]                                          |
+---------------------------------------------------------------+
|                                                               |
|  KEYBOARD SHORTCUTS                                           |
|                                                               |
|  / - Focus search                                             |
|  ESC - Clear search                                           |
|  ? - Show/hide shortcuts help                                 |
|  1-9 - Jump to category                                       |
|                                                               |
|  [Close]                                                      |
|                                                               |
+---------------------------------------------------------------+
```

## Design Notes

1. **Priorities:**

   - Fast loading (critical CSS inline)
   - Clear categorization
   - Prominent search
   - Offline indicator
   - Minimal UI elements

2. **Color Scheme:**

   - Primary: Dark blue/navy (#2c3e50)
   - Secondary: Blue (#3498db)
   - Background: Light gray (#f4f5f7)
   - Text: Dark gray (#333)
   - Status colors:
     - Online: Green (#27ae60)
     - Offline: Red (#e74c3c)

3. **Typography:**

   - System fonts for speed
   - Font stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
   - Base font size: 16px
   - Line height: 1.5

4. **Component Details:**

   - Cards: White background, subtle shadow, rounded corners
   - Search: Full width, prominent placement
   - Status indicator: Color-coded, concise text

5. **Responsive Breakpoints:**
   - Mobile: Up to 768px
   - Tablet: 769px - 1023px
   - Desktop: 1024px and above
