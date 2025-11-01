# Fintech AI System - Design Specification

**Version:** 1.0
**Last Updated:** November 2025
**Design Philosophy:** Modern Bloomberg Terminal meets Robinhood Minimalism

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Layout System](#layout-system)
3. [Component Hierarchy](#component-hierarchy)
4. [Color Palette](#color-palette)
5. [Typography System](#typography-system)
6. [Spacing System](#spacing-system)
7. [Responsive Breakpoints](#responsive-breakpoints)
8. [Component Specifications](#component-specifications)
9. [Interaction Patterns](#interaction-patterns)
10. [Accessibility Guidelines](#accessibility-guidelines)

---

## Design Philosophy

### Core Principles

**1. Information Density with Clarity**
- Inspired by Bloomberg Terminal's professional information density
- Balanced with Robinhood's clean minimalism
- Data-first approach: charts and metrics take priority
- Progressive disclosure: show essential data first, details on interaction

**2. Dark Theme Optimization**
- Primary dark interface reduces eye strain for extended use
- High contrast for data legibility across multiple monitors
- Color-coded financial data (green = positive, red = negative, orange = neutral/action)
- Optimized for 24/7 market monitoring

**3. Mobile-First, Desktop-Enhanced**
- Responsive from 320px to 4K displays
- Touch-optimized for mobile trading
- Keyboard shortcuts for desktop power users
- Modular card-based layout for flexible arrangements

**4. Real-Time Data Focus**
- Live data updates without page refresh
- Smooth animations for price changes
- Performance-optimized for minimal latency
- Clear visual indicators for data freshness

---

## Layout System

### Grid Architecture

#### Desktop Layout (≥1024px)
```
┌─────────────────────────────────────────────────────┐
│  Header (Fixed)                                     │
│  [Logo] [Navigation] [Search] [User]               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────┬───────────────────────┐   │
│  │                     │                       │   │
│  │  Main Content       │   Sidebar (Optional)  │   │
│  │  (8 cols)          │   (4 cols)           │   │
│  │                     │                       │   │
│  │  ┌──────────────┐   │   ┌──────────────┐   │   │
│  │  │ Stats Cards  │   │   │ Quick Stats  │   │   │
│  │  └──────────────┘   │   └──────────────┘   │   │
│  │                     │                       │   │
│  │  ┌──────────────┐   │   ┌──────────────┐   │   │
│  │  │ Price Chart  │   │   │ Watchlist    │   │   │
│  │  │ (Full Width) │   │   └──────────────┘   │   │
│  │  └──────────────┘   │                       │   │
│  │                     │   ┌──────────────┐   │   │
│  │  ┌──────────────┐   │   │ Recent News  │   │   │
│  │  │ Analysis     │   │   └──────────────┘   │   │
│  │  └──────────────┘   │                       │   │
│  │                     │                       │   │
│  └─────────────────────┴───────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

#### Tablet Layout (768px - 1023px)
```
┌─────────────────────────────────┐
│  Header                         │
├─────────────────────────────────┤
│                                 │
│  ┌───────────────────────────┐  │
│  │  Stats Cards (Grid 2x2)   │  │
│  └───────────────────────────┘  │
│                                 │
│  ┌───────────────────────────┐  │
│  │  Price Chart (Full Width) │  │
│  └───────────────────────────┘  │
│                                 │
│  ┌───────────────────────────┐  │
│  │  Analysis Details         │  │
│  └───────────────────────────┘  │
│                                 │
└─────────────────────────────────┘
```

#### Mobile Layout (<768px)
```
┌─────────────────┐
│  Header         │
├─────────────────┤
│                 │
│  ┌───────────┐  │
│  │ Stats     │  │
│  │ (Stacked) │  │
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │ Chart     │  │
│  │ (Full)    │  │
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │ Analysis  │  │
│  └───────────┘  │
│                 │
└─────────────────┘
```

### Grid System Specification

**12-Column Grid**
- **Gutter:** 24px (desktop), 16px (tablet), 12px (mobile)
- **Max Width:** 1440px (container)
- **Margins:** 32px (desktop), 24px (tablet), 16px (mobile)

**Common Column Layouts:**
- **Full Width:** 12 cols - Hero charts, dashboards
- **2/3 + 1/3:** 8 + 4 cols - Main content + sidebar
- **1/2 + 1/2:** 6 + 6 cols - Side-by-side comparisons
- **1/3 Grid:** 4 + 4 + 4 cols - Stats cards, metrics
- **1/4 Grid:** 3 + 3 + 3 + 3 cols - Dense data displays

---

## Component Hierarchy

### Page-Level Components

```
App
├── Navigation
│   ├── Logo
│   ├── MainNav
│   ├── SearchBar
│   └── UserMenu
│
├── Dashboard (Home)
│   ├── QuickStats
│   ├── MarketOverview
│   ├── TrendingStocks
│   └── RecentActivity
│
├── Analysis Page
│   ├── CompanyHeader
│   ├── QuickStatsBar
│   ├── SentimentCard
│   ├── StockChart
│   ├── MacroRegimeCard
│   ├── TradingRecommendation
│   └── PerformanceBreakdown
│
└── Analytics Page
    ├── AnalyticsHeader
    ├── FilterControls
    ├── AnalysisCards
    └── Pagination
```

### Atomic Design Structure

**Atoms** (Basic building blocks)
- Buttons (Primary, Secondary, Ghost)
- Input fields
- Labels
- Icons
- Badges
- Progress bars

**Molecules** (Simple combinations)
- Search bar (input + icon)
- Stat card (label + value + trend)
- Price ticker (symbol + price + change)
- Time range selector (button group)

**Organisms** (Complex components)
- Navigation bar
- Stock chart with controls
- Sentiment analysis card
- Company overview header

**Templates** (Page layouts)
- Dashboard layout
- Analysis page layout
- Analytics page layout

---

## Color Palette

### Primary Colors

**Background Tones**
```css
--bg-primary:     #000000  /* Pure black - Main background */
--bg-secondary:   #0a0a0a  /* Near black - Card backgrounds */
--bg-tertiary:    #1a1a1a  /* Dark gray - Borders, dividers */
--bg-hover:       #1f1f1f  /* Hover states */
--bg-active:      #2a2a2a  /* Active/pressed states */
```

**Text Colors**
```css
--text-primary:   #f5f5f5  /* White - Primary text */
--text-secondary: #999999  /* Gray - Secondary text */
--text-tertiary:  #666666  /* Dim gray - Disabled/placeholder */
--text-inverse:   #000000  /* Black - Text on light backgrounds */
```

### Semantic Colors

**Trading/Financial Colors**
```css
--color-bullish:       #00c853  /* Green - Positive/gains */
--color-bullish-light: #00e676  /* Light green - Highlights */
--color-bullish-dim:   #004d1f  /* Dim green - Backgrounds */

--color-bearish:       #ff1744  /* Red - Negative/losses */
--color-bearish-light: #ff5252  /* Light red - Highlights */
--color-bearish-dim:   #4d0811  /* Dim red - Backgrounds */

--color-neutral:       #ffc400  /* Yellow - Neutral/warning */
--color-neutral-light: #ffea00  /* Light yellow - Highlights */
```

**Brand/Action Colors**
```css
--color-primary:       #ff6b35  /* Orange - Primary actions, emphasis */
--color-primary-light: #ff8966  /* Light orange - Hover states */
--color-primary-dim:   #4d2010  /* Dim orange - Backgrounds */

--color-secondary:     #1a659e  /* Blue - Secondary actions */
--color-secondary-light: #2196f3 /* Light blue - Highlights */
--color-secondary-dim: #0a2333  /* Dim blue - Backgrounds */
```

**System Colors**
```css
--color-success: #00c853  /* Success states */
--color-warning: #ffc400  /* Warning states */
--color-error:   #ff1744  /* Error states */
--color-info:    #1a659e  /* Info states */
```

### Data Visualization Palette

**Chart Colors (Sequential)**
```css
--chart-1: #ff6b35  /* Primary orange */
--chart-2: #1a659e  /* Blue */
--chart-3: #ffc400  /* Yellow */
--chart-4: #00c853  /* Green */
--chart-5: #9c27b0  /* Purple */
--chart-6: #ff5252  /* Red */
```

**Gradient Overlays**
```css
--gradient-bullish: linear-gradient(135deg, #00c853 0%, #00e676 100%);
--gradient-bearish: linear-gradient(135deg, #ff1744 0%, #ff5252 100%);
--gradient-primary: linear-gradient(135deg, #ff6b35 0%, #ff8966 100%);
--gradient-dark: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.8) 100%);
```

### Color Usage Guidelines

**Do's:**
- Use green for positive values, gains, buy signals
- Use red for negative values, losses, sell signals
- Use orange for primary CTAs, emphasis, warnings
- Use blue for informational elements, links
- Maintain minimum 4.5:1 contrast ratio for text

**Don'ts:**
- Don't use color alone to convey information (add icons/labels)
- Don't use bright colors for large areas (reserve for accents)
- Don't mix multiple accent colors in the same component
- Don't use low contrast colors for critical data

---

## Typography System

### Font Families

**Primary Font: Monospace**
```css
--font-mono: 'Consolas', 'Monaco', 'Courier New', monospace;
```
- Used for: Data, numbers, prices, charts, code
- Rationale: Consistent character width, professional trading aesthetic

**Secondary Font: Sans-serif**
```css
--font-sans: 'Inter', 'system-ui', 'Helvetica', 'Arial', sans-serif;
```
- Used for: Headers, body text, UI labels
- Rationale: Clean, readable, modern

### Type Scale

**Desktop Scale (16px base)**
```css
--text-xs:    0.75rem   /* 12px - Captions, labels */
--text-sm:    0.875rem  /* 14px - Secondary text */
--text-base:  1rem      /* 16px - Body text */
--text-lg:    1.125rem  /* 18px - Large body */
--text-xl:    1.25rem   /* 20px - Small headings */
--text-2xl:   1.5rem    /* 24px - Medium headings */
--text-3xl:   1.875rem  /* 30px - Large headings */
--text-4xl:   2.25rem   /* 36px - Display headings */
--text-5xl:   3rem      /* 48px - Hero text */
```

**Mobile Scale (14px base, 87.5% reduction)**
```css
--text-xs-mobile:    0.656rem   /* 10.5px */
--text-sm-mobile:    0.766rem   /* 12.25px */
--text-base-mobile:  0.875rem   /* 14px */
--text-lg-mobile:    0.984rem   /* 15.75px */
--text-xl-mobile:    1.094rem   /* 17.5px */
--text-2xl-mobile:   1.313rem   /* 21px */
--text-3xl-mobile:   1.641rem   /* 26.25px */
```

### Font Weights

```css
--font-normal:    400  /* Body text, labels */
--font-medium:    500  /* Emphasis */
--font-semibold:  600  /* Subheadings, buttons */
--font-bold:      700  /* Headings, important data */
```

### Line Heights

```css
--leading-none:    1     /* Tight spacing, prices */
--leading-tight:   1.25  /* Headings */
--leading-snug:    1.375 /* Subheadings */
--leading-normal:  1.5   /* Body text */
--leading-relaxed: 1.625 /* Comfortable reading */
--leading-loose:   2     /* Spacious layouts */
```

### Letter Spacing

```css
--tracking-tighter: -0.05em  /* Large headings */
--tracking-tight:   -0.025em /* Regular headings */
--tracking-normal:   0       /* Body text */
--tracking-wide:     0.025em /* Uppercase labels */
--tracking-wider:    0.05em  /* Spaced caps */
```

### Typography Usage

**Numbers/Data**
```css
.price {
  font-family: var(--font-mono);
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-none);
}
```

**Headings**
```css
.h1 { font-size: var(--text-4xl); font-weight: 700; line-height: 1.2; }
.h2 { font-size: var(--text-3xl); font-weight: 700; line-height: 1.25; }
.h3 { font-size: var(--text-2xl); font-weight: 600; line-height: 1.3; }
.h4 { font-size: var(--text-xl);  font-weight: 600; line-height: 1.4; }
```

**Body Text**
```css
.body-lg { font-size: var(--text-lg);   line-height: 1.625; }
.body    { font-size: var(--text-base); line-height: 1.5; }
.body-sm { font-size: var(--text-sm);   line-height: 1.5; }
```

---

## Spacing System

### Base Unit: 4px

**Spacing Scale (8px base increment)**
```css
--space-0:   0       /* 0px */
--space-1:   0.25rem /* 4px  - Micro spacing */
--space-2:   0.5rem  /* 8px  - Compact spacing */
--space-3:   0.75rem /* 12px - Tight spacing */
--space-4:   1rem    /* 16px - Default spacing */
--space-5:   1.25rem /* 20px - Medium spacing */
--space-6:   1.5rem  /* 24px - Large spacing */
--space-8:   2rem    /* 32px - XL spacing */
--space-10:  2.5rem  /* 40px - XXL spacing */
--space-12:  3rem    /* 48px - Section spacing */
--space-16:  4rem    /* 64px - Hero spacing */
--space-20:  5rem    /* 80px - Large sections */
--space-24:  6rem    /* 96px - Page sections */
```

### Component-Specific Spacing

**Cards**
```css
--card-padding-sm:  var(--space-4)  /* 16px - Compact cards */
--card-padding:     var(--space-6)  /* 24px - Standard cards */
--card-padding-lg:  var(--space-8)  /* 32px - Large cards */
--card-gap:         var(--space-6)  /* 24px - Between cards */
```

**Buttons**
```css
--btn-padding-x-sm: var(--space-3)  /* 12px */
--btn-padding-y-sm: var(--space-2)  /* 8px */
--btn-padding-x:    var(--space-6)  /* 24px */
--btn-padding-y:    var(--space-2)  /* 8px */
--btn-padding-x-lg: var(--space-8)  /* 32px */
--btn-padding-y-lg: var(--space-3)  /* 12px */
```

**Form Elements**
```css
--input-padding-x:  var(--space-4)  /* 16px */
--input-padding-y:  var(--space-2)  /* 8px */
--input-gap:        var(--space-4)  /* 16px - Between inputs */
```

**Sections**
```css
--section-gap-sm:  var(--space-8)   /* 32px - Tight sections */
--section-gap:     var(--space-12)  /* 48px - Standard sections */
--section-gap-lg:  var(--space-20)  /* 80px - Large sections */
```

### Layout Spacing Guidelines

**Vertical Rhythm**
- Use multiples of 8px for consistency
- Increase spacing progressively (16px → 24px → 32px → 48px)
- Maintain 1.5x to 2x ratio between related elements

**Horizontal Spacing**
- Grid gutters: 24px (desktop), 16px (mobile)
- Card internal padding: 24px
- Between-element gaps: 16px minimum

---

## Responsive Breakpoints

### Breakpoint System

```css
/* Mobile First Approach */
--breakpoint-xs:   320px   /* Small phones */
--breakpoint-sm:   640px   /* Phones */
--breakpoint-md:   768px   /* Tablets */
--breakpoint-lg:   1024px  /* Small laptops */
--breakpoint-xl:   1280px  /* Desktops */
--breakpoint-2xl:  1536px  /* Large desktops */
--breakpoint-3xl:  1920px  /* Ultra-wide */
```

### Tailwind Configuration

```javascript
module.exports = {
  theme: {
    screens: {
      'xs': '320px',
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
      '3xl': '1920px',
    }
  }
}
```

### Responsive Behavior by Component

**Navigation**
- Mobile (<768px): Hamburger menu, full-screen overlay
- Tablet (768px+): Condensed horizontal nav
- Desktop (1024px+): Full horizontal nav with dropdowns

**Grid Layout**
- Mobile: 1 column, full width
- Tablet: 2 columns, 6+6
- Desktop: 3 columns or 8+4 sidebar layout

**Charts**
- Mobile: Full width, reduced height (300px)
- Tablet: Full width, standard height (400px)
- Desktop: Full width, expanded height (500px+)

**Data Tables**
- Mobile: Card view, stacked rows
- Tablet: Horizontal scroll table
- Desktop: Full table with all columns

---

## Component Specifications

### 1. Buttons

**Primary Button**
```css
.btn-primary {
  background: var(--color-primary);
  color: white;
  padding: var(--space-2) var(--space-6);
  border-radius: 6px;
  font-weight: 600;
  transition: all 200ms ease;
}

.btn-primary:hover {
  background: var(--color-primary-light);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}
```

**Secondary Button**
```css
.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--bg-tertiary);
}
```

**Sizes**
- Small: 8px × 12px, text-sm
- Medium: 8px × 24px, text-base
- Large: 12px × 32px, text-lg

### 2. Cards

**Base Card**
```css
.card {
  background: var(--bg-secondary);
  border: 1px solid var(--bg-tertiary);
  border-radius: 8px;
  padding: var(--space-6);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
```

**Elevated Card (Hover State)**
```css
.card:hover {
  border-color: var(--color-primary);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
  transition: all 200ms ease;
}
```

### 3. Input Fields

```css
.input-field {
  background: var(--bg-secondary);
  border: 1px solid var(--bg-tertiary);
  border-radius: 6px;
  padding: var(--space-2) var(--space-4);
  color: var(--text-primary);
  font-size: var(--text-base);
}

.input-field:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}
```

### 4. Stat Cards

```css
.stat-card {
  background: var(--bg-secondary);
  border: 1px solid var(--bg-tertiary);
  border-radius: 8px;
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.stat-label {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-family: var(--font-mono);
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--text-primary);
}

.stat-change {
  font-size: var(--text-sm);
  font-weight: 600;
}

.stat-change.positive { color: var(--color-bullish); }
.stat-change.negative { color: var(--color-bearish); }
```

### 5. Charts

**Container**
```css
.chart-container {
  background: var(--bg-secondary);
  border: 1px solid var(--bg-tertiary);
  border-radius: 8px;
  padding: var(--space-6);
  min-height: 400px;
}
```

**Chart Elements**
- Grid lines: `var(--bg-tertiary)` (#1a1a1a)
- Axis text: `var(--text-secondary)` (#999999)
- Tooltips: Dark background with white text
- Candlestick colors: Green (bullish), Red (bearish)

### 6. Badges

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-success {
  background: rgba(0, 200, 83, 0.1);
  color: var(--color-bullish);
  border: 1px solid rgba(0, 200, 83, 0.3);
}

.badge-error {
  background: rgba(255, 23, 68, 0.1);
  color: var(--color-bearish);
  border: 1px solid rgba(255, 23, 68, 0.3);
}
```

---

## Interaction Patterns

### Hover States

**Default Behavior**
- Subtle color shift (5-10% lighter)
- Slight elevation (2-4px translateY)
- Shadow increase
- Transition: 200ms ease

**Interactive Elements**
```css
.interactive {
  cursor: pointer;
  transition: all 200ms ease;
}

.interactive:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
```

### Focus States

**Keyboard Navigation**
```css
.focusable:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

### Loading States

**Skeleton Screens**
```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--bg-secondary) 25%,
    var(--bg-tertiary) 50%,
    var(--bg-secondary) 75%
  );
  background-size: 200% 100%;
  animation: loading 1.5s ease-in-out infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

**Spinners**
- Primary spinner: Orange ring, white background
- Size: 16px (small), 24px (medium), 48px (large)
- Animation: 0.8s linear infinite rotation

### Animations

**Fade In**
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}
```

**Slide In**
```css
@keyframes slideIn {
  from {
    transform: translateX(-20px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
```

### Micro-interactions

**Price Changes**
- Flash green on increase
- Flash red on decrease
- Duration: 300ms
- Easing: ease-out

**Data Updates**
- Subtle pulse animation
- Color highlight for 1 second
- Return to normal state smoothly

---

## Accessibility Guidelines

### Color Contrast

**WCAG AA Compliance (Minimum)**
- Normal text: 4.5:1 contrast ratio
- Large text (18pt+): 3:1 contrast ratio
- UI components: 3:1 contrast ratio

**Current Palette Compliance**
✅ White (#f5f5f5) on Black (#000000): 19.5:1
✅ Gray (#999999) on Black (#000000): 6.4:1
✅ Orange (#ff6b35) on Black (#000000): 5.2:1
✅ Green (#00c853) on Black (#000000): 4.6:1
✅ Red (#ff1744) on Black (#000000): 4.8:1

### Keyboard Navigation

**Tab Order**
- Logical flow: top to bottom, left to right
- Skip links for main content
- All interactive elements keyboard accessible

**Shortcuts**
- `Cmd/Ctrl + K`: Global search
- `Escape`: Close modals/overlays
- Arrow keys: Navigate charts/data tables
- `/`: Focus search

### Screen Reader Support

**Semantic HTML**
- Use proper heading hierarchy (h1 → h6)
- ARIA labels for interactive elements
- Alt text for all images and charts
- Live regions for real-time data updates

**ARIA Attributes**
```html
<div role="region" aria-label="Stock price chart">
  <svg aria-hidden="true">...</svg>
  <div class="sr-only">Chart showing AAPL stock price...</div>
</div>
```

### Focus Management

**Focus Indicators**
- Visible focus ring on all interactive elements
- High contrast focus states
- Never remove focus outlines without replacement

**Focus Trapping**
- Modal dialogs trap focus
- Return focus to trigger element on close

### Color Blindness Considerations

**Deuteranopia/Protanopia (Red-Green)**
- Don't rely on red/green alone
- Use icons + color (✓ green, ✗ red)
- Add patterns to charts

**Solutions**
- Combine color with text labels
- Use icons alongside color coding
- Provide alternative visualizations

---

## Implementation Notes

### Tailwind CSS Configuration

Extend the existing `tailwind.config.js` to match this design system:

```javascript
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'terminal': {
          'bg': '#000000',
          'bg-light': '#0a0a0a',
          'border': '#1a1a1a',
          'text': '#f5f5f5',
          'text-dim': '#999999',
          'orange': '#ff6b35',
          'orange-light': '#ff8966',
          'blue': '#004e89',
          'blue-light': '#1a659e',
          'green': '#00c853',
          'green-light': '#00e676',
          'red': '#ff1744',
          'red-light': '#ff5252',
          'yellow': '#ffc400',
          'yellow-light': '#ffea00',
        }
      },
      fontFamily: {
        'mono': ['Consolas', 'Monaco', 'Courier New', 'monospace'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      borderRadius: {
        'card': '8px',
      },
      boxShadow: {
        'card': '0 2px 8px rgba(0, 0, 0, 0.2)',
        'card-hover': '0 4px 16px rgba(0, 0, 0, 0.3)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
}
```

### CSS Custom Properties

Create a `variables.css` file:

```css
:root {
  /* Colors */
  --bg-primary: #000000;
  --bg-secondary: #0a0a0a;
  --bg-tertiary: #1a1a1a;

  /* Spacing */
  --space-unit: 0.25rem;

  /* Typography */
  --font-mono: 'Consolas', 'Monaco', 'Courier New', monospace;
  --font-sans: 'Inter', 'system-ui', sans-serif;

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}
```

---

## Design Tokens Export

For design handoff to developers, export tokens in JSON format:

```json
{
  "color": {
    "background": {
      "primary": "#000000",
      "secondary": "#0a0a0a",
      "tertiary": "#1a1a1a"
    },
    "text": {
      "primary": "#f5f5f5",
      "secondary": "#999999",
      "tertiary": "#666666"
    },
    "brand": {
      "primary": "#ff6b35",
      "secondary": "#1a659e"
    },
    "semantic": {
      "success": "#00c853",
      "error": "#ff1744",
      "warning": "#ffc400"
    }
  },
  "typography": {
    "fontFamily": {
      "mono": "Consolas, Monaco, Courier New, monospace",
      "sans": "Inter, system-ui, sans-serif"
    },
    "fontSize": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem"
    },
    "fontWeight": {
      "normal": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700
    }
  },
  "spacing": {
    "1": "0.25rem",
    "2": "0.5rem",
    "3": "0.75rem",
    "4": "1rem",
    "6": "1.5rem",
    "8": "2rem",
    "12": "3rem"
  }
}
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 2025 | Initial design system specification |

---

## References

- [Bloomberg Terminal UX Design](https://www.bloomberg.com/company/stories/how-bloomberg-terminal-ux-designers-conceal-complexity/)
- [Robinhood Visual Identity](https://newsroom.aboutrobinhood.com/a-new-visual-identity/)
- [Tailwind CSS Design System](https://tailwindcss.com/docs)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

**Maintained by:** Fintech AI Design Team
**Questions?** Open an issue in the repository
