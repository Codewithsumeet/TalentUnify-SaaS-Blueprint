# TalentFlow AI — UI/UX Design Specification
> **Version 1.0 — Hackathon Final Edition**  
> Component sources: [21st.dev](https://21st.dev/community/components) · [shadcn/ui](https://ui.shadcn.com) · [Magic UI](https://magicui.design) · [motion-primitives](https://motion-primitives.com)  
> Stack: Next.js 14 · TypeScript · Tailwind CSS · shadcn/ui · Framer Motion · cmdk

---

## Table of Contents

1. [Design System Foundation](#1-design-system-foundation)
2. [Global Layout & Navigation](#2-global-layout--navigation)
3. [Command Palette (Cmd+K)](#3-command-palette-cmdk)
4. [Screen 1 — Dashboard](#4-screen-1--dashboard)
5. [Screen 2 — Candidate Search](#5-screen-2--candidate-search)
6. [Screen 3 — Candidate Profile](#6-screen-3--candidate-profile)
7. [Screen 4 — Pipeline Kanban](#7-screen-4--pipeline-kanban)
8. [Screen 5 — Integrations](#8-screen-5--integrations)
9. [Resume Upload Flow](#9-resume-upload-flow)
10. [Async Parsing States](#10-async-parsing-states)
11. [Micro-interactions Master List](#11-micro-interactions-master-list)
12. [Component Installation Commands](#12-component-installation-commands)
13. [Dark Mode Tokens](#13-dark-mode-tokens)
14. [Accessibility Checklist](#14-accessibility-checklist)

---

## 1. Design System Foundation

### 1.1 Color Tokens

```css
/* globals.css — CSS custom properties */
:root {
  /* Brand */
  --color-navy:        #1A1A2E;   /* primary backgrounds, headings */
  --color-violet:      #6C63FF;   /* primary accent, CTAs, active states */
  --color-teal:        #00D4AA;   /* success, AI score high, confirmed merges */
  --color-coral:       #FF6B6B;   /* destructive, rejected, error states */
  --color-amber:       #F59E0B;   /* warning, pending, suggested merge */
  --color-orange:      #F97316;   /* processing, in-progress states */

  /* Neutrals */
  --color-bg:          #FAFAFA;   /* page background (light mode) */
  --color-surface:     #FFFFFF;   /* card backgrounds */
  --color-surface-2:   #F5F5F7;   /* subtle card variant */
  --color-border:      #E5E7EB;   /* all borders */
  --color-text:        #1E1E2E;   /* body text */
  --color-text-muted:  #6B7280;   /* secondary text */

  /* Semantic */
  --color-score-high:  #00D4AA;   /* 80-100 */
  --color-score-mid:   #F59E0B;   /* 50-79  */
  --color-score-low:   #FF6B6B;   /* 0-49   */

  /* Source Badge Colors */
  --source-email:      #3B82F6;
  --source-upload:     #6C63FF;
  --source-linkedin:   #0A66C2;
  --source-referral:   #F97316;
  --source-hrms:       #059669;
}

.dark {
  --color-bg:          #0D0D1A;
  --color-surface:     #1A1A2E;
  --color-surface-2:   #1E1E32;
  --color-border:      #2D2D4A;
  --color-text:        #F0F0FF;
  --color-text-muted:  #8B8BA8;
}
```

### 1.2 Typography Scale

```css
/* Use Inter variable font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300..800&family=JetBrains+Mono:wght@400;600&display=swap');

/* tailwind.config.ts */
fontFamily: {
  sans: ['Inter', 'system-ui', 'sans-serif'],
  mono: ['JetBrains Mono', 'Menlo', 'monospace'],
}

/* Type scale */
--text-xs:   0.75rem  / 1rem      /* badges, labels */
--text-sm:   0.875rem / 1.25rem   /* secondary body, table cells */
--text-base: 1rem     / 1.5rem    /* primary body */
--text-lg:   1.125rem / 1.75rem   /* card titles */
--text-xl:   1.25rem  / 1.75rem   /* section headers */
--text-2xl:  1.5rem   / 2rem      /* page titles */
--text-3xl:  1.875rem / 2.25rem   /* hero numbers */
--text-5xl:  3rem     / 1         /* AI score gauge number */
```

### 1.3 Spacing & Radius

```
Spacing system (4px base):  4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64 / 80 / 96
Border radius:
  --radius-sm:   6px    /* badges, chips, tooltips */
  --radius-md:   10px   /* buttons, inputs, popovers */
  --radius-lg:   14px   /* cards */
  --radius-xl:   20px   /* modals, large panels */
  --radius-full: 9999px /* avatars, status dots */
```

### 1.4 Shadow Tokens

```css
--shadow-card:   0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(108,99,255,0.04);
--shadow-hover:  0 4px 16px rgba(108,99,255,0.12), 0 1px 4px rgba(0,0,0,0.08);
--shadow-panel:  0 20px 60px rgba(0,0,0,0.15);
--shadow-popover:0 8px 32px rgba(0,0,0,0.12);
```

### 1.5 Motion Tokens (Framer Motion)

```ts
// motion.config.ts
export const transitions = {
  instant:   { duration: 0.1, ease: 'easeOut' },
  fast:      { duration: 0.2, ease: 'easeOut' },
  base:      { duration: 0.3, ease: 'easeOut' },
  slow:      { duration: 0.5, ease: 'easeOut' },
  spring:    { type: 'spring', stiffness: 400, damping: 30 },
  springSlow:{ type: 'spring', stiffness: 200, damping: 25 },
}

export const variants = {
  fadeIn:    { hidden: { opacity: 0 }, visible: { opacity: 1 } },
  slideUp:   { hidden: { opacity: 0, y: 12 }, visible: { opacity: 1, y: 0 } },
  slideIn:   { hidden: { opacity: 0, x: 24 }, visible: { opacity: 1, x: 0 } },
  scaleIn:   { hidden: { opacity: 0, scale: 0.95 }, visible: { opacity: 1, scale: 1 } },
  stagger:   { visible: { transition: { staggerChildren: 0.05 } } },
}
```

---

## 2. Global Layout & Navigation

### 2.1 App Shell

```
┌─────────────────────────────────────────────────────────┐
│  SIDEBAR (240px, collapsible to 56px icon rail)         │
│  ┌──────────────────┐  ┌──────────────────────────────┐ │
│  │ TalentFlow AI    │  │ TOPBAR                       │ │
│  │ logo + wordmark  │  │ Breadcrumb | Search | Avatar │ │
│  ├──────────────────┤  ├──────────────────────────────┤ │
│  │ Nav Items        │  │                              │ │
│  │ • Dashboard      │  │    MAIN CONTENT AREA         │ │
│  │ • Search         │  │    (fluid, max-w-7xl)        │ │
│  │ • Pipeline       │  │                              │ │
│  │ • Integrations   │  │                              │ │
│  │ • Settings       │  │                              │ │
│  ├──────────────────┤  │                              │ │
│  │ ⌘K hint          │  │                              │ │
│  │ User avatar      │  │                              │ │
│  └──────────────────┘  └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Sidebar Component

**Source**: `21st.dev` → `sidebar` category  
**Install**: `npx shadcn@latest add sidebar`

```tsx
// components/layout/Sidebar.tsx
import { Sidebar, SidebarContent, SidebarHeader,
         SidebarMenu, SidebarMenuItem, SidebarMenuButton,
         SidebarFooter, useSidebar } from "@/components/ui/sidebar"

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard",   href: "/" },
  { icon: Search,          label: "Search",      href: "/search", badge: null },
  { icon: Kanban,          label: "Pipeline",    href: "/pipeline" },
  { icon: Plug,            label: "Integrations",href: "/integrations" },
  { icon: Settings,        label: "Settings",    href: "/settings" },
]
```

**Design details:**
- **Logo area**: Gradient icon (`bg-gradient-to-br from-violet-500 to-teal-400`) + "TalentFlow AI" wordmark in `font-semibold`
- **Active state**: Violet left border (3px) + `bg-violet-50 dark:bg-violet-950/30` background + bold label
- **Hover state**: `bg-gray-100 dark:bg-white/5` with 150ms transition
- **Collapsed state**: Only icons at 56px width. Tooltip on hover shows label.
- **Footer**: User avatar + name + role. Kebab menu on hover (Logout, Profile).
- **Keyboard shortcut hint**: Small `⌘K` pill badge near the bottom of nav

### 2.3 Topbar

```tsx
// components/layout/Topbar.tsx
// Left: Breadcrumb (e.g., "Dashboard / Search Results")
// Center: Empty or contextual title
// Right: [Notifications Bell] [Theme Toggle] [Avatar Dropdown]
```

- **Notification bell**: Dot badge (red, animated pulse) when new candidates arrive via email
- **Theme toggle**: Sun/Moon icon, `useTheme()` from `next-themes`
- **Avatar dropdown** (shadcn/ui `DropdownMenu`): Profile, Settings, Keyboard shortcuts, Logout

---

## 3. Command Palette (Cmd+K)

**Source**: `cmdk` by Radix UI + 21st.dev command components  
**Install**: `npm install cmdk`

```tsx
// components/CommandPalette.tsx
import { Command } from 'cmdk'
```

### 3.1 Visual Design

```
┌────────────────────────────────────────────────┐
│  🔍  Search commands or candidates...           │
├────────────────────────────────────────────────┤
│  NAVIGATION                                    │
│  ⌂  Go to Dashboard              ↵             │
│  🔍  Search Candidates            ↵             │
│  📋  Open Pipeline                ↵             │
│  🔌  Integrations                 ↵             │
├────────────────────────────────────────────────┤
│  ACTIONS                                       │
│  ⬆  Upload Resumes               ↵             │
│  ➕  Add Candidate Manually        ↵             │
│  🔀  Review Suggested Merges       ↵             │
├────────────────────────────────────────────────┤
│  APPEARANCE                                    │
│  ☀  Toggle Light Mode             ↵             │
└────────────────────────────────────────────────┘
```

### 3.2 Styling Spec

```css
/* Command palette overlay */
.cmdk-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 9999;
}

/* Dialog */
.cmdk-dialog {
  position: fixed;
  top: 20vh;
  left: 50%;
  transform: translateX(-50%);
  width: min(640px, calc(100vw - 32px));
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-panel);
  overflow: hidden;
}

/* Input */
.cmdk-input {
  font-size: 1rem;
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border);
  background: transparent;
}

/* Items */
.cmdk-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 150ms;
}
.cmdk-item[aria-selected="true"] {
  background: var(--color-violet)/10;
  color: var(--color-violet);
}
```

### 3.3 Animation

```tsx
// Framer Motion wrapper — scale + opacity on open
<AnimatePresence>
  {open && (
    <motion.div
      initial={{ opacity: 0, scale: 0.96, y: -8 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.96, y: -8 }}
      transition={{ duration: 0.15, ease: 'easeOut' }}
    >
      <Command.Dialog />
    </motion.div>
  )}
</AnimatePresence>
```

---

## 4. Screen 1 — Dashboard

### 4.1 Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Welcome back, Priya 👋  |  [Upload Resumes] [AI Search]    │
├──────────┬──────────┬──────────┬──────────────────────────  │
│ Stat     │ Stat     │ Stat     │ Stat                       │
│ Card     │ Card     │ Card     │ Card                       │
├──────────┴──────────┴──────────┴──────────────────────────  │
│                                                             │
│  ┌──────────────────────────────┐  ┌─────────────────────┐ │
│  │  RECENT ACTIVITY FEED         │  │  SOURCE BREAKDOWN   │ │
│  │  (live-updating list)         │  │  (Donut chart)      │ │
│  │                              │  │                     │ │
│  └──────────────────────────────┘  └─────────────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  PIPELINE HEALTH (mini-kanban strip)                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Stat Cards (Number Ticker)

**Source**: `21st.dev` → `number-ticker` / `magic-ui/number-ticker`  
**Install**: `npx shadcn@latest add "https://magicui.design/r/number-ticker"`

```tsx
// 4 stat cards in a grid
const stats = [
  { label: "Total Candidates", value: 1284, icon: Users,     color: "violet", delta: "+23 this week" },
  { label: "Pending Review",   value: 47,   icon: Clock,     color: "amber",  delta: "12 urgent" },
  { label: "Shortlisted",      value: 89,   icon: Star,      color: "teal",   delta: "+8 today" },
  { label: "Open Roles",       value: 6,    icon: Briefcase, color: "coral",  delta: "2 closing soon" },
]
```

**Card anatomy:**
```
┌──────────────────────────────┐
│  [Icon]        [↑ delta tag] │
│                              │
│  1,284                       │  ← NumberTicker animates 0→1284
│  Total Candidates            │
│  ──────────────────────────  │  ← thin gradient bottom border
│  +23 new this week           │
└──────────────────────────────┘
```

**Styling:**
```css
.stat-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-card);
  transition: box-shadow 200ms, transform 200ms;
}
.stat-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-2px);
}
/* Colored bottom accent bar */
.stat-card::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0; height: 3px;
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
  background: var(--accent-gradient);
}
```

### 4.3 Recent Activity Feed

**Source**: `21st.dev` → `timeline` / `activity-feed` components

```tsx
const activities = [
  { type: 'email',    text: 'New resume received from priya.mehta@gmail.com', time: '2 min ago', icon: Mail },
  { type: 'parse',    text: 'AI parsed 5 resumes from batch upload', time: '8 min ago', icon: Sparkles },
  { type: 'merge',    text: 'Duplicate detected: Rahul S. — Review suggested merge', time: '15 min ago', icon: GitMerge },
  { type: 'pipeline', text: 'Ankit Verma moved to Interview Scheduled', time: '1 hr ago', icon: ArrowRight },
  { type: 'shortlist',text: 'Neha Joshi shortlisted for Product Designer role', time: '2 hr ago', icon: Star },
]
```

**Visual spec:**
- Left timeline line: 2px dashed `var(--color-border)`
- Activity dot: 10px circle, color-coded by type (email=blue, parse=violet, merge=amber, pipeline=teal)
- Text: `text-sm text-gray-700`, time: `text-xs text-gray-400`
- Hover: subtle background highlight + "View →" action appears on right
- New activities: slide in from top with `motion.div` `y: -12 → 0`

### 4.4 Source Breakdown Chart

**Component**: Recharts `PieChart` with custom legend  
**Install**: `npm install recharts`

```tsx
const sourceData = [
  { name: 'Email',    value: 34, color: '#3B82F6' },
  { name: 'Upload',  value: 28, color: '#6C63FF' },
  { name: 'LinkedIn',value: 22, color: '#0A66C2' },
  { name: 'Referral',value: 16, color: '#F97316' },
]
// Donut chart: innerRadius=60, outerRadius=90
// Center label: "284\nTotal"
// Custom legend: horizontal pills with colored dots
```

### 4.5 Pipeline Health Strip

**Source**: Mini kanban — custom component using shadcn/ui `Badge`

```tsx
// Compact horizontal pipeline showing counts per stage per role
// Color coding: green=healthy, amber=stalled(>5 days), red=urgent(>10 days)

const pipelineHealth = [
  { role: 'Senior Backend Eng.', applied: 24, screening: 8, interview: 3, offer: 1 },
  { role: 'Product Designer',    applied: 12, screening: 5, interview: 2, offer: 0 },
  { role: 'ML Engineer',         applied: 31, screening: 3, interview: 1, offer: 0 },
]
```

---

## 5. Screen 2 — Candidate Search

> **This is the hero screen. Maximum design investment goes here.**

### 5.1 Layout

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│         SEARCH BAR  (full-width, centered prominence)      │
│         with animated typewriter placeholder               │
│                                                            │
├─────────────────┬──────────────────────────────────────────┤
│  FILTER SIDEBAR │  SEARCH RESULTS GRID                     │
│  (280px)        │                                          │
│                 │  [12 candidate cards, 3-col grid]        │
│  Experience     │                                          │
│  Location       │  [Load more / pagination]                │
│  Skills         │                                          │
│  Source         │                                          │
│  Date Added     │                                          │
└─────────────────┴──────────────────────────────────────────┘
```

### 5.2 Hero Search Bar

**Source**: `21st.dev` → Heros → AI Input / Search components  
Typewriter placeholder: `21st.dev/hextaui/typewriter-text` or `motion-primitives` text shimmer

```tsx
// The search bar is the centerpiece
// Dimensions: full width up to 860px, 56px height, 14px border-radius
// Left icon: sparkle/AI icon (animated shimmer)
// Placeholder text cycles with typewriter effect:

const placeholders = [
  "Find React engineers in Pune with 4+ years...",
  "Show senior designers open to remote...",
  "Backend engineers with AWS + startup exp...",
  "Freshers with Python graduating 2024...",
  "Find candidates similar to our best hire...",
]
```

**Styling:**
```css
.search-bar {
  width: 100%;
  max-width: 860px;
  height: 56px;
  background: var(--color-surface);
  border: 2px solid var(--color-border);
  border-radius: 14px;
  padding: 0 20px 0 52px;   /* left padding for icon */
  font-size: 1rem;
  box-shadow: 0 4px 24px rgba(108,99,255,0.08);
  transition: border-color 200ms, box-shadow 200ms;
}
.search-bar:focus {
  border-color: var(--color-violet);
  box-shadow: 0 0 0 4px rgba(108,99,255,0.12),
              0 4px 24px rgba(108,99,255,0.08);
  outline: none;
}
/* Sparkle icon — animated shimmer when idle */
.search-icon {
  background: linear-gradient(135deg, #6C63FF, #00D4AA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer 3s ease-in-out infinite;
}
```

**Below search bar**: Two rows of quick-filter chips
```tsx
const quickFilters = [
  "React",  "Python", "Remote", "Senior", "Bangalore", "AWS", "Fresher", "ML"
]
// Clicking a chip appends it to the search query
// Active chips: filled violet background
// Inactive: outlined, gray text
```

### 5.3 Filter Sidebar

**Source**: `21st.dev` → sidebar components + shadcn/ui `Slider`, `Checkbox`, `Select`

```
FILTERS                          [Clear All]
─────────────────────────────────────────────
Experience Level
  ●──────────────○  0 – 10+ yrs
  [Fresher] [Mid] [Senior] [Principal]

Location
  [Bengaluru, KA ×] [Remote ×]
  + Add location...

Skills
  [React ×] [Python ×] [AWS ×]
  + Add skill...

Source
  ☑ Email Inbox
  ☑ Resume Upload
  ☑ LinkedIn
  ☑ Referral
  ☑ HRMS

Date Added
  ○ Any time
  ● Last 7 days
  ○ Last 30 days
  ○ Custom range
─────────────────────────────────────────────
[Apply Filters]        12 results
```

**Styling:**
- Sidebar has `sticky top-24` positioning so it stays visible while scrolling results
- Each filter section has a collapsible accordion (shadcn `Accordion`)
- Active filter count badge on the sidebar header: "Filters (3)"
- Chips use `variant="outline"` with an X button; active = `bg-violet-100 border-violet-300`

### 5.4 Candidate Result Card

> Each card is the most visually important recurring element in the app.

```
┌────────────────────────────────────────────────────────┐
│  ┌──────┐  Rahul Sharma              [Score: 87]       │
│  │  RS  │  Senior Backend Engineer                     │
│  │ #6C63 │  Zepto · Bengaluru, KA                      │
│  └──────┘                                              │
│                                                        │
│  [Python] [FastAPI] [AWS] [PostgreSQL] +3 more         │
│                                                        │
│  ● Email  ● Upload   Added Mar 12                      │
│           ─────────────────────────────────────────    │
│  [Shortlist]  [View Profile]  [Why this match? ↗]      │
└────────────────────────────────────────────────────────┘
```

**Component details:**

```tsx
// Avatar: initials with deterministic color from name hash
function getAvatarColor(name: string): string {
  const colors = [
    'from-violet-500 to-purple-600',
    'from-teal-400 to-cyan-500',
    'from-orange-400 to-red-500',
    'from-blue-500 to-indigo-600',
    'from-green-400 to-emerald-500',
    'from-pink-500 to-rose-600',
  ]
  const hash = name.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0)
  return colors[hash % colors.length]
}

// AI Score: radial gauge SVG that animates on mount
// Score colors: 80-100=teal, 50-79=amber, 0-49=coral
```

**Score Gauge (SVG radial):**
```tsx
// SVG arc gauge — animates sweep from 0° to score angle
// Use Framer Motion `animate` on pathLength
<motion.circle
  cx="24" cy="24" r="20"
  stroke={scoreColor}
  strokeWidth="3"
  strokeDasharray="126"
  strokeLinecap="round"
  fill="none"
  initial={{ strokeDashoffset: 126 }}
  animate={{ strokeDashoffset: 126 - (score / 100) * 126 }}
  transition={{ duration: 0.8, ease: 'easeOut', delay: index * 0.05 }}
/>
```

**Skill chips:**
```tsx
// Show first 4 skills, then "+N more" overflow badge
// Chip hover: tooltip "Found in resume 3 times"
<TooltipProvider>
  <Tooltip>
    <TooltipTrigger>
      <Badge variant="secondary" className="skill-chip">{skill}</Badge>
    </TooltipTrigger>
    <TooltipContent>Found in {count} sections of the resume</TooltipContent>
  </Tooltip>
</TooltipProvider>
```

**Source badges:**
```tsx
// Small colored dots with label
const SourceBadge = ({ source }) => (
  <span className="inline-flex items-center gap-1 text-xs text-muted">
    <span className={`w-2 h-2 rounded-full bg-[${SOURCE_COLORS[source]}]`} />
    {source}
  </span>
)
```

**Card hover state:**
```css
.candidate-card {
  transition: transform 200ms, box-shadow 200ms;
  cursor: pointer;
}
.candidate-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-hover);
  border-color: rgba(108, 99, 255, 0.3);
}
```

**Card entrance animation:**
```tsx
// Staggered fade-up on search results load
<motion.div
  variants={variants.stagger}
  initial="hidden"
  animate="visible"
>
  {results.map((candidate, i) => (
    <motion.div
      key={candidate.id}
      variants={variants.slideUp}
      transition={{ ...transitions.base, delay: i * 0.04 }}
    >
      <CandidateCard candidate={candidate} />
    </motion.div>
  ))}
</motion.div>
```

### 5.5 "Why This Match?" Popover

**Source**: shadcn/ui `Popover` + custom breakdown component

```
┌──────────────────────────────────────────────┐
│  Match Breakdown                        [×]  │
│  ─────────────────────────────────────────── │
│         87                                   │
│        ────     Strong Match                 │
│        /100                                  │
│  ─────────────────────────────────────────── │
│  Skills Match                                │
│  ✓ Python  ✓ FastAPI  ✓ AWS  ✗ React         │
│                                              │
│  Experience                                  │
│  Senior (6 yrs) · 1 yr above requirement    │
│                                              │
│  Location                                   │
│  📍 Bengaluru · 100% match                   │
│                                              │
│  AI Summary                                  │
│  "Strong backend engineer with prod AWS      │
│   experience. No React but has Angular —     │
│   transferable frontend exposure."           │
└──────────────────────────────────────────────┘
```

**Styling details:**
- Popover: 380px wide, `border-radius: 16px`, subtle violet top border (3px)
- Score: Large `text-5xl font-bold` centered, colored by range
- Matched skills: Green check + skill chip. Missing: Gray strikethrough chip
- AI Summary: `font-italic text-sm text-muted` with sparkle icon prefix
- Animation: `scale: 0.95 → 1, opacity: 0 → 1` in 180ms

### 5.6 Right-Side Detail Panel (Slide-in)

Clicking a candidate card opens a `Sheet` panel from the right — no full navigation.

```tsx
// shadcn/ui Sheet component
import { Sheet, SheetContent, SheetHeader } from "@/components/ui/sheet"

<Sheet open={selectedCandidate !== null} onOpenChange={() => setSelected(null)}>
  <SheetContent side="right" className="w-[560px] sm:max-w-[560px]">
    <CandidateDetailPanel candidate={selectedCandidate} />
  </SheetContent>
</Sheet>
```

**Animation spec:**
```css
/* shadcn Sheet already has slide-in animation */
/* Customize: 300ms spring, slides from x=560 to x=0 */
[data-state="open"] {
  animation: slideInRight 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## 6. Screen 3 — Candidate Profile

### 6.1 Layout

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back to Search                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  HERO SECTION                                          │ │
│  │  [Avatar 80px]  Name · Role · Company · Location       │ │
│  │  [Source badges]  [AI Score gauge]  [Action buttons]   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────┐  ┌───────────────────────┐ │
│  │  SKILLS (tag cloud)         │  │  CONTACT INFO         │ │
│  └─────────────────────────────┘  └───────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  EXPERIENCE TIMELINE                                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────┐  ┌─────────────────────────────┐ │
│  │  EDUCATION             │  │  ACTIVITY LOG              │ │
│  └────────────────────────┘  └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Hero Section

```tsx
// Gradient background behind hero
<div className="relative rounded-2xl overflow-hidden p-8"
     style={{ background: 'linear-gradient(135deg, #1A1A2E 0%, #2D1B69 100%)' }}>
  {/* Subtle noise texture overlay */}
  <div className="absolute inset-0 opacity-5"
       style={{ backgroundImage: 'url(/noise.png)' }} />

  <div className="relative flex items-start gap-6">
    <Avatar size="xl" name={candidate.name} />
    <div className="flex-1">
      <h1 className="text-3xl font-bold text-white">{candidate.name}</h1>
      <p className="text-violet-300">{candidate.currentRole} · {candidate.currentCompany}</p>
      <p className="text-gray-400 flex items-center gap-1">
        <MapPin size={14} /> {candidate.location}
      </p>
      <div className="mt-3 flex gap-2">
        {candidate.sources.map(s => <SourceBadge key={s} source={s} />)}
        {candidate.suggestedMerge && <MergeAlert candidate={candidate} />}
      </div>
    </div>
    <AIScoreGauge score={candidate.score} size="lg" />
  </div>

  {/* Action buttons */}
  <div className="relative mt-6 flex gap-3">
    <Button variant="teal">⭐ Shortlist</Button>
    <Button variant="outline-white">✉ Send Email</Button>
    <Button variant="outline-white">📝 Add Note</Button>
    <Button variant="destructive-ghost">✗ Reject</Button>
  </div>
</div>
```

### 6.3 Skills Section

**Source**: Custom tag cloud with confidence visualization

```tsx
// Two types of chips:
// CONFIRMED (found in 2+ resume sections): filled background
// MENTIONED (found once): outlined border only

const SkillChip = ({ skill, confidence, count }) => (
  <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.97 }}>
    <Tooltip>
      <TooltipTrigger>
        <Badge
          variant={count >= 2 ? "filled" : "outline"}
          className={count >= 2 ? "bg-violet-100 text-violet-700 border-violet-200" : ""}
        >
          {skill}
          {confidence < 70 && <span className="ml-1 text-amber-500">~</span>}
        </Badge>
      </TooltipTrigger>
      <TooltipContent>
        Found in {count} section{count > 1 ? 's' : ''} · {confidence}% confidence
      </TooltipContent>
    </Tooltip>
  </motion.div>
)
```

### 6.4 Experience Timeline

**Source**: `21st.dev` → timeline components  
**Reference**: `motion-primitives` timeline

```
│
●  Senior Backend Engineer                    Jan 2022 – Present (2y 3m)
│  Zepto · Bengaluru, KA                              [Current]
│  Built payment microservices handling 2M+ daily txns.
│  Led migration from monolith to k8s, reducing infra costs 40%.
│
●  Software Engineer                          Jun 2019 – Dec 2021 (2y 6m)
│  Razorpay · Bengaluru, KA
│  Developed core payment gateway APIs in Python/FastAPI.
│  Owned fraud detection pipeline serving 500K req/day.
│
●  Junior Developer                           Jan 2018 – May 2019 (1y 4m)
   Infosys · Pune, MH
   Maintained Java Spring Boot services for banking client.
```

**Timeline styling:**
```css
.timeline-line {
  width: 2px;
  background: linear-gradient(to bottom, var(--color-violet), var(--color-teal));
}
.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-violet);
  border: 2px solid var(--color-surface);
  box-shadow: 0 0 0 4px rgba(108,99,255,0.15);
}
.timeline-dot.current {
  background: var(--color-teal);
  animation: pulse-teal 2s infinite;
}
```

### 6.5 Suggested Merge Alert

```tsx
// Only shown when dedup engine flags this profile
<motion.div
  initial={{ opacity: 0, y: -8 }}
  animate={{ opacity: 1, y: 0 }}
  className="rounded-xl border border-amber-200 bg-amber-50 p-4 flex items-start gap-3"
>
  <GitMerge className="text-amber-500 mt-0.5" size={18} />
  <div className="flex-1">
    <p className="font-medium text-amber-800">Possible duplicate detected</p>
    <p className="text-sm text-amber-600">
      Matches Rahul S. (rahul.sharma@outlook.com) by name + city
    </p>
  </div>
  <Button size="sm" variant="amber">Review Side-by-Side →</Button>
  <Button size="icon" variant="ghost"><X size={16} /></Button>
</motion.div>
```

---

## 7. Screen 4 — Pipeline Kanban

### 7.1 Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Pipeline  |  [Filter by Role ▼]  [View: Kanban | List]  [Export]   │
├──────────┬────────────┬────────────┬──────────────┬─────────────────┤
│ APPLIED  │ SCREENING  │ INTERVIEW  │   OFFER      │ HIRED/ARCHIVED  │
│  (24)    │    (8)     │    (3)     │    (1)       │    (12/67)      │
├──────────┼────────────┼────────────┼──────────────┼─────────────────┤
│ [Card]   │ [Card]     │ [Card]     │ [Card]       │ [Card]          │
│ [Card]   │ [Card]     │ [Card]     │              │                 │
│ [Card]   │ [Card]     │            │              │                 │
│ [Card]   │            │            │              │                 │
│ ...      │            │            │              │                 │
└──────────┴────────────┴────────────┴──────────────┴─────────────────┘
```

### 7.2 Kanban Implementation

**Source**: `21st.dev` → awesome-shadcn-ui → Kanban with `dnd-kit`  
**Install**: `npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities`

```tsx
import { DndContext, DragOverlay, closestCenter } from '@dnd-kit/core'
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable'

// Column colors
const STAGE_COLORS = {
  applied:    { bg: '#EFF6FF', border: '#3B82F6', dot: '#3B82F6' },
  screening:  { bg: '#F5F3FF', border: '#6C63FF', dot: '#6C63FF' },
  interview:  { bg: '#FFFBEB', border: '#F59E0B', dot: '#F59E0B' },
  offer:      { bg: '#F0FDF4', border: '#00D4AA', dot: '#00D4AA' },
  hired:      { bg: '#F0FDF4', border: '#059669', dot: '#059669' },
  archived:   { bg: '#F9FAFB', border: '#9CA3AF', dot: '#9CA3AF' },
}
```

### 7.3 Kanban Column Header

```tsx
<div className="kanban-column-header">
  <div className="flex items-center gap-2">
    <span className={`w-2.5 h-2.5 rounded-full bg-[${stage.dot}]`} />
    <h3 className="font-semibold text-sm">{stage.label}</h3>
    <Badge variant="secondary">{count}</Badge>
  </div>
  <div className="text-xs text-muted mt-1">
    Avg {avgDays}d in stage
    {avgDays > 7 && <span className="text-amber-500 ml-1">⚠ Slowing</span>}
  </div>
</div>
```

### 7.4 Kanban Card

```
┌────────────────────────────────────┐
│  [☐] [RS avatar]  Rahul Sharma     │  ← checkbox on hover
│        Senior Backend Eng.         │
│        Applied: Backend Role       │
│                                    │
│  [Score 87] [🔴 Day 9]  [···]      │  ← day badge red if > 7
└────────────────────────────────────┘
```

**Drag visual:**
```tsx
// While dragging: card gets elevated shadow + 5° tilt
// Drop target column: glows with column accent color
// On drop: spring snap animation

const DraggingCard = ({ candidate }) => (
  <motion.div
    style={{ rotate: 3 }}
    animate={{ scale: 1.03, boxShadow: '0 20px 40px rgba(0,0,0,0.2)' }}
    className="kanban-card dragging"
  >
    <CandidateKanbanCard candidate={candidate} />
  </motion.div>
)

// Drop confirmation: green border flash
const onDropSuccess = (cardId) => {
  setFlashCard(cardId)
  setTimeout(() => setFlashCard(null), 400)
}
```

### 7.5 Bulk Selection

```tsx
// When any card is checkbox-selected, a floating bulk action bar appears
<AnimatePresence>
  {selectedCards.length > 0 && (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 24 }}
      className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50
                 flex items-center gap-3 bg-gray-900 text-white
                 rounded-2xl px-6 py-3 shadow-2xl"
    >
      <span className="text-sm font-medium">{selectedCards.length} selected</span>
      <Separator orientation="vertical" className="h-4 bg-gray-600" />
      <Button size="sm" variant="ghost-white">Move Stage</Button>
      <Button size="sm" variant="ghost-white">Export CSV</Button>
      <Button size="sm" variant="ghost-white" className="text-red-400">Reject All</Button>
      <Button size="icon" variant="ghost-white" onClick={clearSelection}><X size={14} /></Button>
    </motion.div>
  )}
</AnimatePresence>
```

---

## 8. Screen 5 — Integrations

### 8.1 Layout

```
┌────────────────────────────────────────────────────────────┐
│  Integrations                                              │
│  Connect your candidate sources to TalentFlow AI           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Testmail.app │  │ Gmail        │  │ LinkedIn     │    │
│  │ ● Connected  │  │ ○ Disconnected│  │ ~ Simulation │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐                       │
│  │ Zoho Recruit │  │ Referral Form│                       │
│  │ ○ Disconnected│  │ ● Active     │                       │
│  └──────────────┘  └──────────────┘                       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 8.2 Integration Card

```tsx
const IntegrationCard = ({ integration }) => (
  <div className="rounded-2xl border border-border p-6 bg-surface hover:border-violet-200 transition-colors">
    
    {/* Header */}
    <div className="flex items-start justify-between mb-4">
      <div className="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center">
        <integration.Icon size={24} />
      </div>
      <StatusPill status={integration.status} />
    </div>

    {/* Info */}
    <h3 className="font-semibold mb-1">{integration.name}</h3>
    <p className="text-sm text-muted mb-4">{integration.description}</p>

    {/* Stats (when connected) */}
    {integration.connected && (
      <div className="grid grid-cols-2 gap-3 mb-4">
        <Stat label="Processed" value={integration.processedCount} />
        <Stat label="Last Sync"  value={integration.lastSync} />
      </div>
    )}

    {/* Action */}
    <Button
      variant={integration.connected ? "outline" : "default"}
      className="w-full"
      onClick={integration.connected ? integration.onDisconnect : integration.onConnect}
    >
      {integration.connected ? 'Manage Connection' : 'Connect'}
    </Button>
  </div>
)
```

### 8.3 Status Pill

```tsx
const STATUS_STYLES = {
  connected:    'bg-teal-100 text-teal-700 border-teal-200',
  disconnected: 'bg-gray-100 text-gray-500 border-gray-200',
  simulation:   'bg-amber-100 text-amber-700 border-amber-200',
  error:        'bg-red-100 text-red-600 border-red-200',
}

const StatusPill = ({ status }) => (
  <span className={`inline-flex items-center gap-1.5 text-xs font-medium
                    px-2.5 py-1 rounded-full border ${STATUS_STYLES[status]}`}>
    <span className={`w-1.5 h-1.5 rounded-full ${
      status === 'connected' ? 'bg-teal-500 animate-pulse' : ''
    }`} />
    {STATUS_LABELS[status]}
  </span>
)
```

---

## 9. Resume Upload Flow

### 9.1 Upload Zone Component

**Source**: `21st.dev` → file upload / dropzone components

```tsx
// Drag-and-drop zone with visual feedback states

const UploadZone = () => {
  const [state, setState] = useState<'idle' | 'hover' | 'uploading'>('idle')

  return (
    <motion.div
      onDragEnter={() => setState('hover')}
      onDragLeave={() => setState('idle')}
      onDrop={handleDrop}
      animate={{
        borderColor: state === 'hover' ? '#00D4AA' : '#E5E7EB',
        backgroundColor: state === 'hover' ? 'rgba(0,212,170,0.05)' : 'transparent',
        scale: state === 'hover' ? 1.01 : 1,
      }}
      className="relative rounded-2xl border-2 border-dashed p-16
                 flex flex-col items-center gap-4 cursor-pointer"
    >
      <motion.div
        animate={{ y: state === 'hover' ? -4 : 0 }}
        transition={transitions.spring}
      >
        <Upload size={40} className="text-violet-400" />
      </motion.div>

      <div className="text-center">
        <p className="font-semibold">Drop resumes here or click to browse</p>
        <p className="text-sm text-muted mt-1">PDF, DOCX up to 10MB · Batch upload supported</p>
      </div>

      <div className="flex gap-2">
        <Badge variant="outline">PDF</Badge>
        <Badge variant="outline">DOCX</Badge>
        <Badge variant="outline">Up to 20 files</Badge>
      </div>

      {/* Hidden file input */}
      <input type="file" multiple accept=".pdf,.docx" className="hidden" ref={fileInputRef} />
    </motion.div>
  )
}
```

### 9.2 Upload Queue

After drop, files appear as processing items:

```tsx
// Each file gets a queue item:
const UploadQueueItem = ({ file, status }) => (
  <motion.div
    layout
    initial={{ opacity: 0, x: -20 }}
    animate={{ opacity: 1, x: 0 }}
    exit={{ opacity: 0, x: 20 }}
    className="flex items-center gap-3 p-3 rounded-xl bg-surface border"
  >
    <FileText size={20} className="text-violet-400 shrink-0" />
    
    <div className="flex-1 min-w-0">
      <p className="text-sm font-medium truncate">{file.name}</p>
      <p className="text-xs text-muted">{formatBytes(file.size)}</p>
    </div>

    {status === 'uploading' && <Spinner size="sm" className="text-violet-400" />}
    {status === 'parsing'   && <Shimmer className="w-16 h-2 rounded" />}
    {status === 'complete'  && <CheckCircle size={18} className="text-teal-500" />}
    {status === 'error'     && (
      <div className="flex items-center gap-2">
        <AlertCircle size={18} className="text-red-400" />
        <Button size="xs" variant="ghost">Retry</Button>
      </div>
    )}
  </motion.div>
)
```

---

## 10. Async Parsing States

### 10.1 Skeleton Loader Card

**Source**: `21st.dev` → skeleton / shimmer components  
**Install**: `npx shadcn@latest add skeleton`

```tsx
// While LlamaParse is processing — shown immediately on upload
const CandidateCardSkeleton = () => (
  <div className="rounded-2xl border border-border p-5 space-y-3">
    <div className="flex gap-3">
      <Skeleton className="w-12 h-12 rounded-xl" />
      <div className="space-y-2 flex-1">
        <Skeleton className="h-4 w-48" />
        <Skeleton className="h-3 w-32" />
      </div>
      <Skeleton className="w-12 h-12 rounded-full" />
    </div>
    <div className="flex gap-2">
      <Skeleton className="h-6 w-16 rounded-full" />
      <Skeleton className="h-6 w-20 rounded-full" />
      <Skeleton className="h-6 w-14 rounded-full" />
    </div>
    <Skeleton className="h-3 w-full" />
    <Skeleton className="h-3 w-3/4" />
  </div>
)

// Add animated shimmer via CSS:
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}
.skeleton {
  background: linear-gradient(90deg,
    #f0f0f0 25%,
    #e0e0f0 50%,
    #f0f0f0 75%
  );
  background-size: 200%;
  animation: shimmer 1.5s infinite;
}
```

### 10.2 State Transition

```tsx
// Skeleton → Real card transition
// When parse completes, skeleton fades out and real card fades in

<AnimatePresence mode="wait">
  {candidate.status === 'parsing' ? (
    <motion.div key="skeleton" exit={{ opacity: 0 }}>
      <CandidateCardSkeleton />
    </motion.div>
  ) : (
    <motion.div
      key="card"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      // Green border flash on arrival
      onAnimationComplete={() => triggerSuccessFlash(candidate.id)}
    >
      <CandidateCard candidate={candidate} />
    </motion.div>
  )}
</AnimatePresence>
```

### 10.3 Processing Status Banner

```tsx
// Appears at top of search results when uploads are in queue
{parsingQueue.length > 0 && (
  <motion.div
    initial={{ opacity: 0, y: -16 }}
    animate={{ opacity: 1, y: 0 }}
    className="rounded-xl bg-violet-50 border border-violet-200 p-3
               flex items-center gap-3 mb-4"
  >
    <Loader2 className="animate-spin text-violet-500" size={18} />
    <span className="text-sm text-violet-700 font-medium">
      Parsing {parsingQueue.length} resume{parsingQueue.length > 1 ? 's' : ''}...
    </span>
    <div className="ml-auto flex gap-2">
      {parsingQueue.map(f => (
        <span key={f.id} className="text-xs bg-violet-100 rounded px-2 py-0.5 truncate max-w-[120px]">
          {f.name}
        </span>
      ))}
    </div>
  </motion.div>
)}
```

---

## 11. Micro-interactions Master List

| Element | Interaction | Animation | Duration |
|---|---|---|---|
| Candidate card | Hover | `translateY(-3px)` + shadow deepens | 200ms ease |
| Candidate card | Click | Scale `0.98` tap then navigate | 100ms spring |
| AI Score gauge | Mount | Arc sweeps from 0 to score | 800ms ease-out |
| Number ticker | Mount | Counts from 0 to value | 600ms ease-out |
| Search bar | Focus | Border glows violet, shadow expands | 200ms ease |
| Skill chip | Hover | Scale `1.05`, tooltip appears | 150ms ease |
| Upload zone | Drag-over | Border → teal, bg tint, scale `1.01` | 150ms spring |
| File drop | Drop | Confirmation ripple effect | 300ms |
| Kanban card | Drag start | Scale `1.03`, rotate `3deg`, shadow | 200ms spring |
| Kanban card | Drop | Snap to position, green flash border | 300ms spring |
| Stage change | Move | Card slides to new column | 400ms spring |
| Parsing complete | Transition | Skeleton → card fade, green border flash | 300ms |
| Duplicate toast | Appear | Slide in from bottom-right | 300ms spring |
| Duplicate toast | Dismiss | Slide out + fade | 200ms ease |
| Sheet panel | Open | `x: 560 → 0` + spring | 300ms spring |
| Sheet panel | Close | `x: 0 → 560` + fade | 250ms ease-in |
| Command palette | Open | Scale `0.95→1` + fade-in + backdrop blur | 150ms ease |
| Button | Click | Scale `0.97` | 100ms spring |
| Navigation | Active | Left border slides in | 200ms ease |
| Status dot | Connected | Pulse animation loop | 2s infinite |
| Empty state SVG | Mount | Illustration fades + floats gently | 600ms ease |

---

## 12. Component Installation Commands

```bash
# 1. Core UI framework
npx shadcn@latest init

# 2. shadcn/ui components used in TalentFlow AI
npx shadcn@latest add sidebar          # Global navigation
npx shadcn@latest add card             # Candidate cards, stat cards
npx shadcn@latest add badge            # Skill chips, status pills, source tags
npx shadcn@latest add button           # All CTAs
npx shadcn@latest add input            # Search bar, form inputs
npx shadcn@latest add sheet            # Candidate detail slide-in panel
npx shadcn@latest add dialog           # Merge confirmation, bulk actions
npx shadcn@latest add popover          # Why-this-match breakdown
npx shadcn@latest add tooltip          # Skill chip hover, shortcut hints
npx shadcn@latest add toast            # Duplicate detected, parse complete
npx shadcn@latest add avatar           # Candidate initials
npx shadcn@latest add skeleton         # Parsing loading states
npx shadcn@latest add tabs             # Profile tabs, view switchers
npx shadcn@latest add accordion        # Filter sidebar sections
npx shadcn@latest add slider           # Experience range filter
npx shadcn@latest add checkbox         # Source filter, bulk select
npx shadcn@latest add select           # Role filter, sorting
npx shadcn@latest add separator        # Visual dividers
npx shadcn@latest add progress         # Upload progress bar
npx shadcn@latest add dropdown-menu    # User menu, card action menus

# 3. Animation libraries
npm install framer-motion              # All animations + spring physics
npm install cmdk                       # Command palette (Cmd+K)

# 4. Charts
npm install recharts                   # Source donut chart, pipeline charts

# 5. Drag-and-drop (Kanban)
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities

# 6. Magic UI components (copy from magicui.design)
# NumberTicker — animated stat counters
npx shadcn@latest add "https://magicui.design/r/number-ticker"
# Shimmer Button — CTA buttons with shimmer effect
npx shadcn@latest add "https://magicui.design/r/shimmer-button"
# Animated Gradient Text — for headings
npx shadcn@latest add "https://magicui.design/r/animated-gradient-text"
# Bento Grid — dashboard stats layout
npx shadcn@latest add "https://magicui.design/r/bento-grid"

# 7. Fonts
npm install @fontsource-variable/inter   # Inter variable font
```

---

## 13. Dark Mode Tokens

```tsx
// tailwind.config.ts
theme: {
  extend: {
    colors: {
      // All colors reference CSS variables so dark mode works automatically
      background:    'var(--color-bg)',
      surface:       'var(--color-surface)',
      'surface-2':   'var(--color-surface-2)',
      border:        'var(--color-border)',
      foreground:    'var(--color-text)',
      muted:         'var(--color-text-muted)',
      violet:        { DEFAULT: '#6C63FF', light: '#8B84FF', dark: '#5B52E8' },
      teal:          { DEFAULT: '#00D4AA', light: '#1ADDB4', dark: '#00B893' },
      coral:         { DEFAULT: '#FF6B6B', light: '#FF8585', dark: '#E85555' },
    }
  }
}

// next-themes setup in layout.tsx
<ThemeProvider attribute="class" defaultTheme="light" enableSystem>
  {children}
</ThemeProvider>
```

**Dark mode card appearance:**
```css
.dark .candidate-card {
  background: #1A1A2E;
  border-color: #2D2D4A;
}
.dark .candidate-card:hover {
  border-color: rgba(108, 99, 255, 0.4);
  box-shadow: 0 4px 16px rgba(108, 99, 255, 0.15);
}
.dark .search-bar {
  background: #1A1A2E;
  border-color: #2D2D4A;
  color: #F0F0FF;
}
.dark .search-bar:focus {
  border-color: #6C63FF;
  box-shadow: 0 0 0 4px rgba(108,99,255,0.2);
}
```

---

## 14. Accessibility Checklist

- [ ] All interactive elements reachable via `Tab` key
- [ ] Focus rings visible (2px violet outline, not removed)
- [ ] Color is never the only means of conveying information (badges have icons + text)
- [ ] AI Score gauge has `aria-label="AI match score: 87 out of 100"`
- [ ] Kanban drag-and-drop has keyboard alternative (click card → arrows to move stage)
- [ ] Skeleton loaders have `aria-busy="true"` and `aria-label="Loading candidate"`
- [ ] Command palette traps focus correctly, closes on Escape
- [ ] All images/icons have `alt` text or `aria-hidden="true"` if decorative
- [ ] Toast notifications use `role="status"` or `role="alert"`
- [ ] Color contrast ratio ≥ 4.5:1 for all body text
- [ ] Sheet/Dialog returns focus to trigger element on close
- [ ] Form inputs have associated `<label>` elements
- [ ] Error states are announced to screen readers via `aria-live="polite"`

---

## Appendix: Screen Flow Diagram

```
┌────────────┐     upload resumes     ┌──────────────────┐
│  Dashboard │ ───────────────────▶  │  Upload Modal     │
│            │                       │  (drag & drop)    │
│  [Upload]  │                       └────────┬─────────┘
│  [Search]  │                                │ parsing...
└──────┬─────┘                       ┌────────▼─────────┐
       │                             │  Candidate added  │
       │ click Search                │  to database      │
       ▼                             └──────────────────┘
┌─────────────────┐
│  Search Screen  │◀──── Cmd+K → "Search candidates"
│  [NL Search bar]│
│  [Filters]      │
│  [Result cards] │
└───────┬─────────┘
        │ click card or "View Profile"
        ▼
┌──────────────────────┐     review merge?    ┌────────────────┐
│  Candidate Profile   │ ──────────────────▶ │  Merge Review  │
│  (slide-in panel OR  │                     │  (side-by-side)│
│   full page)         │                     └────────────────┘
│  [Shortlist] [Reject]│
└──────────┬───────────┘
           │ shortlist
           ▼
┌──────────────────────┐
│  Pipeline Kanban     │
│  [Drag-drop stages]  │
│  [Bulk actions]      │
└──────────────────────┘
```

---

*End of UI/UX Specification — TalentFlow AI v1.0*  
*Questions? Every design decision in this doc has a reason. Build in this order: Design tokens → Layout shell → Candidate card → Search screen → Everything else.*