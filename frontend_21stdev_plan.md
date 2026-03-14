# Frontend 21st.dev UI Implementation Plan

This execution plan is designed specifically for the `frontend-agent` CLI to build the TalentUnify application UI following the premium **21st.dev aesthetic**.

## Architecture & Design Tokens
- **Framework:** Next.js 14 (App Router), TypeScript.
- **Styling Libraries:** Tailwind CSS, `shadcn/ui`, `framer-motion`, `lucide-react`, Magic UI.
- **Design Language:** 
  - True Dark Mode (`#09090b` background).
  - Glassmorphism (`.glass-card` utility with `backdrop-filter: blur(12px)` and `rgba(24,24,27,0.6)`).
  - Subtle glowing gradients embedded in the body background.
  - Smooth micro-interactions and springs via Framer Motion.

---

## Step 1: App Shell & Navigation (Priority 1)
**Goal:** Build the persistent Layout, Sidebar, and Topbar.

1. **`app/(app)/layout.tsx`**:
   - Implement the `SidebarProvider` from `shadcn/ui`.
   - Ensure the `globals.css` background gradients persist seamlessly behind the layout.
2. **`components/layout/Sidebar.tsx`**: 
   - Dark theme styling using `sidebar-primary` tokens.
   - Navigation links: Dashboard, Candidates, Search, Compare, Integrations.
   - Active state indicators should have a subtle glowing left border.
3. **`components/layout/Topbar.tsx`**:
   - Sticky header with blurred glassmorphism (`backdrop-filter: blur(12px)`).
   - Include Breadcrumbs, a global Quick Search trigger (`cmd+k`), and a User Avatar.

---

## Step 2: Core Components (Priority 2)
**Goal:** Build the reusable atomic components with the 21st.dev vibe.

1. **`components/ui/CandidateCard.tsx`**: 
   - Apply the `.glass-card` CSS class.
   - Card structure: Header (Avatar + Source Badge) -> Body (Name, Role, Top 3 Skills) -> Footer (Action Buttons).
   - Use `framer-motion` for `whileHover={{ y: -4, scale: 1.01 }}`.
2. **`components/ui/AIScoreGauge.tsx`**:
   - SVG circular progress bar showing the Match Score (0-100%).
   - Colors: >85% Teal (`#00D4AA`), 70-85% Amber, <70% Coral.
3. **`components/ui/SkillChip.tsx`**:
   - Pill-shaped badges.
   - Shared skills in diff views should glow green; unique skills glow amber.
4. **`components/ui/ResumeUploadZone.tsx`**:
   - Drag-and-drop zone using `react-dropzone`.
   - Dashed border with a subtle pulse animation when a file is dragged over.

---

## Step 3: Page Implementations (Priority 3)
**Goal:** Assemble the core application routes.

1. **Dashboard (`app/(app)/dashboard/page.tsx`)**:
   - 4 Top-level StatCards (Total Candidates, Parse Success Rate, etc.) utilizing `Magic UI`'s `NumberTicker`.
   - **ActivityFeed** component summarizing recent parses and searches.
2. **Search Page (`app/(app)/search/page.tsx`)**:
   - Prominent, centered, oversized natural language input field (e.g., "Senior React developer in Bangalore...").
   - Results grid rendering `CandidateCard`s.
3. **Compare Page (`app/(app)/compare/page.tsx`)**:
   - Vertical 50/50 split layout.
   - Side-by-side display rendering Candidate A vs Candidate B, strictly diffing their skills arrays visually.
4. **Integrations (`app/(app)/integrations/page.tsx`)**:
   - Grid of glass-cards representing the 3 sources: Gmail (OAuth), local Mock HRMS, and LinkedIn Simulation.
   - Provide "Sync / Ingest" action buttons with `shimmer` loading states.

---

## Instructions for CLI Agent Execution
Pass this exact prompt to the AI CLI:
> "Read `frontend_21stdev_plan.md`. You are the frontend-agent. Execute Step 1 and Step 2 of this plan. Build the Next.js App Shell (`layout.tsx`, `Sidebar.tsx`, `Topbar.tsx`) and the core `CandidateCard` component using the defined 21st.dev aesthetic features."
