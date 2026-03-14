# TALENTFLOW AI — SYSTEM PROMPT
## Feed this to your CLI agent FIRST before any other file.

---

## MISSION

You are building **TalentFlow AI**, a production-grade AI-powered recruitment SaaS platform for a 48-hour hackathon (Breach 2026). Build quality and demo-readiness are the top priorities.

You will build:
1. A public **landing page** at `/`
2. A protected **web app** at `/dashboard` and child routes

**Primary visual inspiration**: 21st.dev component categories — Heros, Features, Buttons, CTAs, Text Components, AI Chat, Testimonials, Shaders. All components from this source should be referenced as design patterns.

---

## STACK

```
Next.js 14 (App Router) · TypeScript · Tailwind CSS · shadcn/ui
Framer Motion · cmdk · Recharts · @dnd-kit · next-themes · lucide-react
```

---

## INSTALL COMMANDS (run in order, do not skip)

```bash
# 1. Init project
npx create-next-app@latest talentflow --typescript --tailwind --eslint --app --src-dir=false

# 2. shadcn/ui init
npx shadcn@latest init

# 3. shadcn/ui components
npx shadcn@latest add sidebar card badge button input sheet dialog popover \
  tooltip toast avatar skeleton tabs accordion slider checkbox select \
  separator progress dropdown-menu

# 4. npm packages
npm install framer-motion cmdk recharts \
  @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities \
  next-themes lucide-react

# 5. ESM-compatible tailwind animation plugin
npm install tailwindcss-animate

# 6. Magic UI components (copy-on-install)
npx shadcn@latest add "https://magicui.design/r/number-ticker"
npx shadcn@latest add "https://magicui.design/r/shimmer-button"
npx shadcn@latest add "https://magicui.design/r/animated-gradient-text"
npx shadcn@latest add "https://magicui.design/r/bento-grid"
```

---

## COMPLETE FILE STRUCTURE

```
app/
├── (marketing)/
│   └── page.tsx                    ← Landing page (public)
├── (app)/
│   ├── layout.tsx                  ← App shell (Sidebar + Topbar + providers)
│   ├── dashboard/
│   │   └── page.tsx
│   ├── search/
│   │   └── page.tsx
│   ├── candidates/
│   │   └── [id]/
│   │       └── page.tsx
│   ├── pipeline/
│   │   └── page.tsx
│   ├── compare/
│   │   └── page.tsx
│   ├── integrations/
│   │   └── page.tsx
│   └── settings/
│       └── page.tsx                ← REQUIRED — linked from Sidebar

components/
├── layout/
│   ├── Sidebar.tsx
│   ├── Topbar.tsx                  ← REQUIRED — see 02_design_system.md
│   └── CommandPalette.tsx
├── ui/
│   └── sidebar-provider.tsx        ← Custom provider — see 02_design_system.md
├── candidates/
│   ├── CandidateCard.tsx
│   │   └── [imports Avatar, ScoreGauge, SkillChips, SourceBadges, MatchPopoverTrigger]
│   ├── CandidateCardSkeleton.tsx
│   ├── AIScoreGauge.tsx
│   ├── SkillChip.tsx
│   └── SourceBadge.tsx
├── search/
│   ├── SearchBar.tsx
│   └── FilterSidebar.tsx
├── pipeline/
│   ├── KanbanBoard.tsx
│   ├── KanbanColumn.tsx
│   └── KanbanCard.tsx
├── upload/
│   ├── ResumeUploadZone.tsx
│   └── UploadQueueItem.tsx
├── dashboard/
│   ├── StatCard.tsx
│   ├── ActivityFeed.tsx
│   └── SourceDonutChart.tsx
└── integrations/
    └── IntegrationCard.tsx

lib/
├── api.ts                          ← Axios instance (SSR-safe)
├── mock-data.ts                    ← All mock candidates + activities
└── motion.config.ts                ← Framer Motion presets
```

---

## BUILD ORDER (follow exactly — earlier steps are dependencies of later ones)

```
Step 01  globals.css + tailwind.config.ts + motion.config.ts
Step 02  lib/mock-data.ts + lib/api.ts
Step 03  Shared atomic components: AIScoreGauge, SkillChip, SourceBadge, CandidateCardSkeleton
Step 04  CandidateCard (composed from Step 03 atoms)
Step 05  App layout shell: Sidebar + Topbar + CommandPalette + SidebarProvider
Step 06  Dashboard page: StatCard + ActivityFeed + SourceDonutChart
Step 07  Search page: SearchBar + FilterSidebar + ResultsGrid + WhyThisMatchPopover
Step 08  Candidate profile page (/candidates/[id])
Step 09  Pipeline Kanban page
Step 10  Compare page
Step 11  Integrations page + IntegrationCard
Step 12  Settings page (stub is fine — must not 404)
Step 13  Upload flow: ResumeUploadZone + UploadQueueItem + SSE async states
Step 14  Landing page (uses components from Steps 03–07)
Step 15  Dark mode QA + accessibility pass + mobile responsive pass
```

---

## DEMO FLOW (build so every step works perfectly)

```
1.  Landing page → "Get Started" CTA
2.  Dashboard → stat cards animate in, activity feed, source chart
3.  ⌘K → type "upload" → Enter → opens file picker
4.  Upload 3 resumes → 3 skeletons appear → each resolves independently
5.  Integrations → HRMS Sync → candidates appear
6.  Integrations → LinkedIn Ingest → "Simulated" badge candidates appear
7.  Search → "Senior Python engineers in Bangalore" → ranked cards
8.  "Why this match?" → click popover on top result → full breakdown
9.  Compare → select two candidates → skill diff rendered
10. Pipeline → drag candidate Screening→Interview → spring animation
```

---

## DEMO MODE FALLBACK (implement in Upload flow)

If `NEXT_PUBLIC_DEMO_MODE=true`, skip real SSE and simulate parsing locally:

```ts
// lib/demo-mode.ts
export const DEMO_MODE = process.env.NEXT_PUBLIC_DEMO_MODE === 'true'

export function simulateParsing(
  onUploading: () => void,
  onParsing: () => void,
  onComplete: (candidate: MockCandidate) => void
) {
  onUploading()
  setTimeout(onParsing, 400)
  setTimeout(() => onComplete(getRandomMockCandidate()), 2200)
}
```

Use in `ResumeUploadZone.tsx`:
```ts
if (DEMO_MODE) {
  simulateParsing(setUploading, setParsing, addCandidate)
} else {
  const es = new EventSource(`/events/${uploadId}`)
  es.onmessage = handleSSEEvent
  // cleanup in useEffect return
}
```
