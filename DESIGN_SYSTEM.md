# Design System - CattySmoothy/Raichuu

This document outlines the design system implemented for the CattySmoothy/Raichuu platform, based on the Figma Beta design.

## Overview

The design system provides a consistent, modern, and responsive foundation for the entire application. It includes:

- **Design Tokens**: Colors, typography, spacing, and other design constants
- **Component Library**: Reusable UI components
- **Responsive Design**: Mobile-first approach with breakpoints
- **Accessibility**: WCAG compliant design patterns

## Files Structure

```
static/css/
├── design-system.css    # Core design tokens and utilities
└── style.css           # Component styles and layout
```

## Design Tokens

### Colors
- **Primary**: `#667eea` (Blue gradient start)
- **Secondary**: `#764ba2` (Purple gradient end)
- **Accent**: `#f093fb` (Pink accent)
- **Neutral Scale**: Gray-50 to Gray-900

### Typography
- **Primary Font**: Inter (body text)
- **Secondary Font**: Poppins (headings)
- **Scale**: 12px to 48px (text-xs to text-5xl)

### Spacing
- **Scale**: 4px to 80px (space-1 to space-20)
- **Consistent**: 4px base unit system

### Border Radius
- **Scale**: 4px to 24px (radius-sm to radius-2xl)
- **Special**: radius-full for circular elements

## Components

### Buttons
- `.btn` - Base button class
- `.btn-primary` - Primary action button
- `.btn-secondary` - Secondary action button
- `.btn-ghost` - Minimal button style

### Cards
- `.card` - Base card container
- `.card-header` - Card header section
- `.card-body` - Card content section
- `.card-footer` - Card footer section

### Layout
- `.container` - Responsive container
- `.grid` - CSS Grid system
- `.flex` - Flexbox utilities

## Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## Usage Examples

### Creating a Button
```html
<a href="#" class="btn btn-primary">Join for free</a>
```

### Creating a Card
```html
<div class="card">
    <div class="card-body">
        <h3>Card Title</h3>
        <p>Card content goes here.</p>
    </div>
</div>
```

### Using the Grid System
```html
<div class="grid grid-cols-2">
    <div class="card">Content 1</div>
    <div class="card">Content 2</div>
</div>
```

## Customization

To customize the design system:

1. **Colors**: Update CSS custom properties in `:root`
2. **Typography**: Modify font imports and variables
3. **Spacing**: Adjust the spacing scale
4. **Components**: Extend existing classes or create new ones

## Figma Integration

The design system is based on the Figma Beta design exports:
- `Desktop.png` - Desktop layout reference
- `Tablet.png` - Tablet layout reference  
- `Mobile.png` - Mobile layout reference

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- CSS Grid and Flexbox support required
- CSS Custom Properties (CSS Variables) support required

## Performance

- Optimized CSS with minimal redundancy
- Efficient selectors and specificity
- Minimal external dependencies (only Google Fonts)
