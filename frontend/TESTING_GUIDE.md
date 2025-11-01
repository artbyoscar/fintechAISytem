# Testing Guide - New Layout Implementation

## Overview

This guide provides step-by-step instructions for testing the new AnalysisResultsNew layout before full deployment.

---

## Quick Start

### 1. Start Development Server

```bash
cd frontend
npm run dev
```

Server will start on [http://localhost:3001](http://localhost:3001)

### 2. Access Test Page

Add the test page to your app routing or create a temporary route:

**Option A: Add to main App.jsx**
```jsx
import TestNewLayout from './TestNewLayout'

// In your router or component:
<Route path="/test-layout" element={<TestNewLayout />} />
```

**Option B: Temporary direct render**
```jsx
// In App.jsx, temporarily replace main content:
import TestNewLayout from './TestNewLayout'

function App() {
  return <TestNewLayout />
}
```

### 3. Navigate to Test Page

Open browser to: `http://localhost:3001/test-layout`

---

## Testing Scenarios

### Scenario 1: Visual Layout Inspection

**Goal**: Verify the new layout looks correct and matches design specs

**Steps**:
1. Open test page
2. Toggle to "New Layout (70/30)"
3. Verify:
   - ✅ Sticky header at top
   - ✅ Chart takes ~70% of width
   - ✅ Sidebar takes ~30% of width
   - ✅ All cards have subtle borders
   - ✅ Colors match palette (green/red/orange)
   - ✅ Spacing feels balanced

**Expected Result**: Layout matches REDESIGN_SUMMARY.md specifications

---

### Scenario 2: Side-by-Side Comparison

**Goal**: Compare old vs new layout with same data

**Steps**:
1. View "New Layout (70/30)"
2. Note chart prominence, information density
3. Toggle to "Old Layout"
4. Note differences in:
   - Chart size and position
   - Information layout
   - Scrolling required
5. Toggle back and forth several times

**Expected Result**: New layout feels more modern and chart-focused

---

### Scenario 3: Responsive Behavior

**Goal**: Verify layout works at all screen sizes

**Steps**:
1. Open test page on desktop
2. Open browser DevTools (F12)
3. Click "Toggle Device Toolbar" (Ctrl+Shift+M)
4. Test these sizes:
   - **Desktop**: 1920x1080 → Chart 70%, sidebar 30%
   - **Laptop**: 1366x768 → Still 70/30 split
   - **Tablet**: 768x1024 → Adjusts or stacks
   - **Mobile**: 375x667 → Fully stacked
5. Verify no horizontal scrolling at any size
6. Check header remains sticky

**Expected Result**: Smooth responsive behavior, no broken layouts

---

### Scenario 4: Component Rendering

**Goal**: Verify all components display correctly with data

**Steps**:
1. View new layout
2. Check each component:

**StatsCard (Sidebar Top)**:
- [ ] Shows 4 stats (Sentiment, Macro, Recommendation, Time)
- [ ] Colors match data (green/red/orange)
- [ ] Confidence percentages visible

**SentimentCardCompact (Sidebar)**:
- [ ] Shows sentiment icon (↑ for positive)
- [ ] Shows "POSITIVE" label
- [ ] Shows confidence (87%)
- [ ] Gauge slider at correct position
- [ ] Top 3 scores with bars

**MacroRegimeCardCompact (Sidebar)**:
- [ ] Shows bull emoji (🐂)
- [ ] Shows "BULL" label
- [ ] Shows confidence (78%)
- [ ] Shows 3 indicators with +/- values
- [ ] Shows "FAVORABLE" action

**StockChart (Main)**:
- [ ] Chart renders and fills 70% width
- [ ] Timeframe selector works
- [ ] Can switch timeframes
- [ ] Cached indicators show after prefetch

**Trading Recommendation (Main)**:
- [ ] Orange border visible
- [ ] Shows "FAVORABLE" with checkmark
- [ ] Shows rationale text
- [ ] Shows 4 suggested actions
- [ ] Risk level badge shows "Medium risk"

**Performance Breakdown (Main)**:
- [ ] Shows 4 timing metrics
- [ ] Values in seconds (e.g., "0.876s")
- [ ] Orange color on numbers

**About This Analysis (Sidebar Bottom)**:
- [ ] Shows 3 info rows
- [ ] Total time in orange

**Expected Result**: All components render without errors

---

### Scenario 5: Browser Compatibility

**Goal**: Verify layout works in all major browsers

**Browsers to Test**:
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (macOS/iOS if available)

**For Each Browser**:
1. Open test page
2. Check layout renders correctly
3. Open DevTools console
4. Verify no errors
5. Test timeframe switching
6. Test responsive behavior

**Expected Result**: Consistent behavior across browsers

---

### Scenario 6: Performance Testing

**Goal**: Verify layout performs well

**Steps**:
1. Open test page
2. Open DevTools → Performance tab
3. Record while:
   - Toggling between old/new layout
   - Switching timeframes on chart
   - Scrolling page
4. Check metrics:
   - Initial render: <100ms
   - Layout shift: Minimal
   - Timeframe switch: <50ms (cached)
   - No memory leaks

**Expected Result**: Smooth performance, no janky animations

---

### Scenario 7: Console Error Check

**Goal**: Ensure no errors or warnings

**Steps**:
1. Open test page
2. Open DevTools Console (F12)
3. Clear console
4. Toggle layouts several times
5. Switch timeframes
6. Check for:
   - ❌ Red errors
   - ⚠️ Yellow warnings
   - Missing prop warnings
   - Failed network requests

**Expected Result**: Clean console, no errors

---

## Integration Testing with Real Data

### Test with Live Analysis

**Steps**:
1. Navigate to main app analysis page
2. Run analysis for a real ticker (e.g., AAPL)
3. Temporarily swap components:

```jsx
// In your analysis page:
import AnalysisResultsNew from './components/AnalysisResultsNew'

// Replace:
// <AnalysisResults result={data} />

// With:
<AnalysisResultsNew result={data} />
```

4. Verify:
   - Real data populates correctly
   - All values display
   - No "undefined" or "NaN"
   - Performance timings accurate
   - Timestamp shows correctly

**Expected Result**: Real data renders perfectly

---

## Edge Cases to Test

### Missing Data Scenarios

Test with modified mock data:

**No Company Name**:
```jsx
const mockResult = { ...mockData, company: undefined }
```
Expected: Header still renders, just no company shown

**No Recommendation**:
```jsx
const mockResult = { ...mockData, recommendation: null }
```
Expected: Recommendation card hidden, no errors

**No Performance Data**:
```jsx
const mockResult = { ...mockData, performance: null }
```
Expected: Performance card hidden

**Empty Indicators**:
```jsx
const mockResult = {
  ...mockData,
  macro_regime: { ...mockData.macro_regime, indicators: {} }
}
```
Expected: Indicators section hidden or shows "N/A"

---

## Accessibility Testing

### Keyboard Navigation

**Steps**:
1. Tab through page
2. Verify:
   - All buttons focusable
   - Logical tab order
   - Focus visible (outline/ring)
   - Can activate with Enter/Space

### Screen Reader

**Steps** (if available):
1. Enable screen reader (NVDA/JAWS/VoiceOver)
2. Navigate page
3. Verify:
   - Headers announced correctly
   - Values have context
   - Not just "green" or "positive" without context

### Color Contrast

**Steps**:
1. Use browser extension (e.g., WAVE, axe DevTools)
2. Check contrast ratios:
   - White on dark: ✅ Should pass AAA
   - Colors on dark: ✅ Should pass AA minimum

---

## Rollout Plan

### Phase 1: Internal Testing (Current)
- [ ] Complete all test scenarios above
- [ ] Document any issues found
- [ ] Fix critical bugs
- [ ] Get team approval

### Phase 2: A/B Testing (Optional)
- [ ] Deploy both layouts to production
- [ ] Randomly show 50% users new layout
- [ ] Collect metrics:
  - Time on page
  - Scroll depth
  - Click-through rate
  - User feedback
- [ ] Analyze results after 1-2 weeks

### Phase 3: Full Deployment
- [ ] If testing successful, swap files:
  ```bash
  mv src/components/AnalysisResults.jsx src/components/AnalysisResultsOld.jsx
  mv src/components/AnalysisResultsNew.jsx src/components/AnalysisResults.jsx
  ```
- [ ] Update imports in parent components
- [ ] Deploy to production
- [ ] Monitor for issues

### Phase 4: Cleanup
- [ ] After 2-4 weeks of stable new layout
- [ ] Archive old components:
  ```bash
  mkdir src/components/archive
  mv src/components/AnalysisResultsOld.jsx src/components/archive/
  ```
- [ ] Remove TestNewLayout.jsx
- [ ] Update documentation

---

## Troubleshooting

### Issue: Layout Looks Broken

**Symptoms**: Cards overlapping, misaligned

**Fix**:
1. Check Tailwind config has fintech colors
2. Clear browser cache (Ctrl+Shift+R)
3. Restart dev server
4. Check console for CSS errors

### Issue: Chart Not Displaying

**Symptoms**: Blank space where chart should be

**Fix**:
1. Check StockChart.jsx is importing correctly
2. Verify ticker prop is passed
3. Check console for API errors
4. Verify market data endpoint is running (port 8001)

### Issue: Colors Wrong

**Symptoms**: Gray instead of green/red/orange

**Fix**:
1. Check tailwind.config.js has fintech colors:
   ```js
   colors: {
     'fintech': {
       'bg': '#0D1117',
       'card': '#161B22',
       // ... etc
     }
   }
   ```
2. Rebuild Tailwind: `npm run dev` (restart)
3. Clear browser cache

### Issue: Responsive Not Working

**Symptoms**: Layout doesn't stack on mobile

**Fix**:
1. Check flex classes on columns:
   - Chart: `flex-[7]` on desktop
   - Sidebar: `flex-[3]` on desktop
2. Add mobile breakpoints: `sm:flex-1`
3. Test with real mobile device, not just DevTools

### Issue: Sticky Header Not Sticky

**Symptoms**: Header scrolls away

**Fix**:
1. Check header has `sticky top-0 z-10`
2. Parent container doesn't have `overflow-hidden`
3. Try adding `position: sticky` in inline styles if needed

---

## Metrics to Track

### Before Deployment

| Metric | Target | Actual |
|--------|--------|--------|
| Initial Render | <100ms | ___ |
| Cached Chart Switch | <50ms | ___ |
| Layout Shift (CLS) | <0.1 | ___ |
| First Contentful Paint | <1s | ___ |
| Console Errors | 0 | ___ |
| Accessibility Score | >90 | ___ |

### After Deployment (If A/B Testing)

| Metric | Old Layout | New Layout | Change |
|--------|-----------|-----------|--------|
| Avg Time on Page | ___ | ___ | ___ |
| Scroll Depth | ___ | ___ | ___ |
| Chart Interactions | ___ | ___ | ___ |
| User Satisfaction | ___ | ___ | ___ |

---

## Sign-Off

### Testing Complete

- [ ] All visual tests passed
- [ ] All functional tests passed
- [ ] All responsive tests passed
- [ ] All browser tests passed
- [ ] All accessibility tests passed
- [ ] Performance benchmarks met
- [ ] No critical bugs found
- [ ] Documentation complete

**Tested By**: ________________
**Date**: ________________
**Approved By**: ________________
**Deployment Date**: ________________

---

## Additional Resources

- **Design Specs**: [REDESIGN_SUMMARY.md](./REDESIGN_SUMMARY.md)
- **Integration Checklist**: [INTEGRATION_TEST_CHECKLIST.md](./INTEGRATION_TEST_CHECKLIST.md)
- **Performance Docs**: [PERFORMANCE_TEST.md](./PERFORMANCE_TEST.md)
- **Component Code**: [src/components/AnalysisResultsNew.jsx](./src/components/AnalysisResultsNew.jsx)

---

**Last Updated**: 2025-11-01
**Version**: 1.0
**Status**: Ready for Testing ✅
