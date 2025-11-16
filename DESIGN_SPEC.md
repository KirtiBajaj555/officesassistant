# 🎨 Office Assistant - Design Specification

## Visual Design Language

### Color Palette

```
Primary Colors:
├─ Deep Blue      #2563EB    ████████  - Main actions, buttons
├─ Deep Purple    #8B5CF6    ████████  - Accents, highlights
└─ Hot Pink       #EC4899    ████████  - Special emphasis

Neutrals:
├─ Light Gray     #F8FAFC    ████████  - Background
├─ Medium Gray    #64748B    ████████  - Secondary text
├─ Dark Gray      #1E293B    ████████  - Primary text
└─ White          #FFFFFF    ████████  - Cards, surfaces

Status Colors:
├─ Success Green  #10B981    ████████  - Confirmations
├─ Warning Orange #F59E0B    ████████  - Warnings
└─ Error Red      #EF4444    ████████  - Errors
```

### Gradients

**Primary Gradient** (Buttons, Headers)
```
Linear: #2563EB → #8B5CF6
Direction: Top-left to Bottom-right
```

**Accent Gradient** (Special elements)
```
Linear: #8B5CF6 → #EC4899
Direction: Top-left to Bottom-right
```

**Background Gradient** (Main screen)
```
Linear: #F8FAFC → #EEF2FF → #FCF7FF
Direction: Top to Bottom
```

### Typography

**Font Family**: Inter (via Google Fonts)

**Text Styles**:
```
Display Large:    32px, Bold, -0.5 letter-spacing
Display Medium:   24px, SemiBold
Title Large:      20px, SemiBold
Body Large:       16px, Regular, 1.5 line-height
Body Medium:      14px, Regular, 1.5 line-height
Label Large:      14px, SemiBold
```

### Spacing System

```
XS:   4px   - Tight spacing
S:    8px   - Small gaps
M:    12px  - Default spacing
L:    16px  - Card padding
XL:   24px  - Section spacing
2XL:  32px  - Large sections
3XL:  48px  - Major dividers
```

### Border Radius

```
Small:     8px   - Small buttons, tags
Medium:    12px  - Icons, small cards
Default:   16px  - Buttons, inputs
Large:     20px  - Messages, large cards
XLarge:    24px  - Modals, sheets
Circular:  50%   - Avatar, round buttons
```

### Shadows

**Soft Shadow** (Cards, subtle elevation)
```
Offset: 0, 4px
Blur: 20px
Color: #1E293B @ 5% opacity
```

**Medium Shadow** (Elevated elements)
```
Offset: 0, 8px
Blur: 30px
Color: #1E293B @ 10% opacity
```

**Glow Shadow** (Primary actions)
```
Offset: 0, 4px
Blur: 20px
Color: #2563EB @ 30% opacity
```

## Component Design

### 1. App Bar (Header)

```
Height: 68px
Background: White
Shadow: Soft shadow
Padding: 16px horizontal, 12px vertical

Layout:
[Logo/Icon] [Title + Subtitle] [Actions]
  44x44        Flexible          48px
```

**Logo/Icon**:
- Size: 44x44px
- Shape: Rounded square (12px radius)
- Style: Gradient background (#2563EB → #8B5CF6)
- Icon: Assistant symbol, white, 24px

**Title**:
- "Office Assistant" - Title Large, Bold
- "Always here to help" - Body Small, Gray

### 2. Message Bubbles

**User Message** (Right-aligned):
```
Background: Primary gradient
Text: White, 15px
Padding: 16px horizontal, 12px vertical
Border Radius: 20px (top), 4px (bottom-right)
Max Width: Screen width - 60px (left margin)
Shadow: Soft shadow
```

**Assistant Message** (Left-aligned):
```
Background: White
Text: Dark Gray, 15px
Padding: 16px horizontal, 12px vertical
Border Radius: 20px (top), 4px (bottom-left)
Max Width: Screen width - 60px (right margin)
Shadow: Soft shadow

Header:
  [Avatar] "Assistant"
   24px    12px, SemiBold, Gray
   
Avatar: Gradient circle with robot icon
```

**System Message** (Full-width):
```
Background: Light gray
Border: 1px Light Gray
Padding: 16px
Border Radius: 16px
Icon: Info icon in gradient box
Layout: [Icon] [Message Text]
```

### 3. Chat Input

```
Height: Auto (min 52px, max 120px)
Background: White
Shadow: Soft shadow (top)
Padding: 16px

Layout:
[+ Button] [Text Input] [Send Button]
  44px        Flexible      44px
```

**Add Button**:
- Size: 44x44px
- Background: Light background
- Icon: Plus circle, Primary blue, 26px
- Border Radius: 12px

**Text Input**:
- Background: Light background (#F8FAFC)
- Border: None
- Border Radius: 24px
- Padding: 12px horizontal
- Placeholder: "Ask me anything..."
- Font: 15px, Dark text
- Max Height: 120px (scrollable)

**Send Button**:
- Size: 44x44px
- Background: Gradient (when active), Light gray (disabled)
- Icon: Send arrow, White, 22px
- Border Radius: 12px
- Glow: Active state has glow shadow
- Transition: 200ms smooth

### 4. Typing Indicator

```
Background: White
Padding: 16px horizontal, 12px vertical
Border Radius: 20px (top), 4px (bottom-left)
Shadow: Soft shadow
Margin: Same as assistant message

Layout:
[Avatar] [Dot][Dot][Dot]
 24px     8px  8px  8px

Dots:
- Size: 8px circle
- Color: Gray with opacity animation
- Animation: Fade in/out, 1.5s, infinite
- Delay: 0.2s between each dot
```

### 5. Bottom Sheet (Options Menu)

```
Background: White
Border Radius: 24px (top corners)
Padding: 24px vertical
Shadow: Medium shadow

Handle:
- Width: 40px
- Height: 4px
- Color: Light gray
- Border Radius: 2px
- Position: Top center

Options:
Each option: ListTile with gradient icon
Icon: 48x48px gradient box, 12px radius
Text: Title (SemiBold) + Subtitle (Gray, 13px)
```

### 6. Dialog (Alerts)

```
Background: White
Border Radius: 20px
Max Width: 320px
Padding: 24px
Shadow: Medium shadow

Title: 
- Title Large style
- Icon optional (if present, shown in gradient box)

Content:
- Body Large, 1.5 line-height
- Gray text

Actions:
- Right-aligned
- TextButton (Cancel) + ElevatedButton (Confirm)
- 8px gap between buttons
```

## Animations & Interactions

### 1. Message Entry
```
Animation: Slide up + Fade in
Duration: 300ms
Easing: ease-out
```

### 2. Button Press
```
Animation: Scale down (0.95)
Duration: 100ms
Feedback: Haptic (mobile)
```

### 3. Send Button Active
```
Animation: Scale + Glow
Duration: 200ms
Glow: Shadow intensifies
```

### 4. Typing Indicator
```
Animation: Sequential fade
Duration: 1500ms
Loop: Infinite
Pattern: Dot 1 → Dot 2 → Dot 3 → Repeat
```

### 5. Bottom Sheet
```
Animation: Slide up + Fade in
Duration: 250ms
Easing: ease-out
Background dim: 50% black
```

### 6. Page Transitions
```
Animation: Fade in
Duration: 500ms
Easing: ease-in
```

## Responsive Behavior

### Mobile (< 600px)
- Single column chat
- Full-width messages (with margins)
- Bottom sheet for menus
- Portrait orientation locked

### Tablet (600-1200px)
- Centered chat (max 800px)
- Larger margins
- Modal dialogs instead of sheets
- Orientation flexible

### Desktop (> 1200px)
- Centered chat (max 900px)
- Keyboard shortcuts enabled
- Hover states for buttons
- Right-click context menus

## Accessibility

### Color Contrast
- Text on background: 7:1 minimum
- Buttons: 4.5:1 minimum
- WCAG AAA compliant

### Touch Targets
- Minimum: 44x44px
- Recommended: 48x48px

### Screen Readers
- All icons have labels
- Message timestamps included
- Status updates announced

### Keyboard Navigation
- Tab through interactive elements
- Enter to send message
- Esc to close dialogs

## Icon System

**Material Icons** (Default set)

Primary Icons:
- Assistant: `assistant_rounded`
- Send: `send_rounded`
- Add: `add_circle_outline`
- Phone: `phone`
- Email: `email`
- Calendar: `calendar_today`
- File: `attach_file`
- Image: `image`
- More: `more_vert`
- Delete: `delete_outline`
- Info: `info_outline`

## Loading States

### Initial Load
- Gradient background visible
- Centered spinner with logo
- "Loading..." text below

### Message Sending
- Small spinner in message bubble
- Gray color for pending
- Checkmark when delivered

### Error States
- Red bubble for errors
- Error icon
- Retry option

## Empty States

### No Messages
```
Icon: Large assistant icon (64px) in gradient circle
Title: "Your Office Assistant"
Subtitle: "I'm here to help you with calls, emails,
           scheduling, and much more!"
Center-aligned
Vertical spacing: 24px between elements
```

## Best Practices

1. **Consistent Spacing**: Use the 4px spacing system
2. **Shadow Depth**: More important = stronger shadow
3. **Color Purpose**: Blue for actions, Gray for information
4. **Animation Speed**: Keep under 300ms for responsiveness
5. **Touch Friendly**: 48px minimum for mobile targets
6. **Loading Feedback**: Always show progress indicators
7. **Error Handling**: Clear, friendly error messages
8. **Accessibility**: Test with screen readers and keyboard

---

**This design creates a modern, professional, and delightful user experience** ✨

