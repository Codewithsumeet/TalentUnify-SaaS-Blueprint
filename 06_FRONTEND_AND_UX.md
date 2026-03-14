# 06 — FRONTEND & UX DESIGN
## Page Layouts, Component Library & Design System

---

## 🎨 Design System

### Color Palette
| Token | Value | Usage |
|-------|-------|-------|
| Primary | `#2563EB` | Buttons, links, active states |
| Secondary | `#10B981` | Success states, positive indicators |
| Danger | `#EF4444` | Errors, delete actions |
| Warning | `#F59E0B` | Warnings, medium match scores |
| Background | `#F9FAFB` | Page backgrounds |
| Surface | `#FFFFFF` | Cards, modals |
| Text Primary | `#1F2937` | Headlines, body text |
| Text Secondary | `#6B7280` | Labels, descriptions |

### Typography
| Element | Font | Size | Weight |
|---------|------|------|--------|
| H1 | Inter | 32px | Bold |
| H2 | Inter | 24px | Semibold |
| H3 | Inter | 18px | Semibold |
| Body | Inter | 14-16px | Regular |
| Small | Inter | 12px | Regular |
| Code | JetBrains Mono | 13px | Regular |

### Components Library
Using **shadcn/ui** for: Button, Card, Table, Badge, Input, Modal, Spinner, Dropdown, Toast, Tabs

---

## 📄 Page Designs (5 Core Pages)

### Page 1: Recruiter Dashboard (`/dashboard`)

```
┌──────────────────────────────────────────────────────────┐
│ [Logo] TalentUnify     🔍 Quick Search    [User Menu ▼]  │
├──────────┬───────────────────────────────────────────────┤
│          │                                               │
│ 📊 Dash  │  📊 Quick Stats Row                          │
│ 🔍 Search│  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│ 👤 Cands │  │ 150      │ │ 45       │ │ 12       │     │
│ 🔗 Integ │  │ Total    │ │ In Review│ │ Offered  │     │
│ ⚙️ Setts │  └──────────┘ └──────────┘ └──────────┘     │
│          │                                               │
│          │  🕐 Recently Added Candidates                 │
│          │  ┌────────────────────────────────────────┐   │
│          │  │ Name     │ Skills      │ Source │ Date │   │
│          │  │ John Doe │ Python, AWS │ Email  │ 2h   │   │
│          │  │ Jane S.  │ React, TS   │ Upload │ 1h   │   │
│          │  │ Alex M.  │ Go, K8s     │ Gmail  │ 30m  │   │
│          │  └────────────────────────────────────────┘   │
│          │                                               │
│          │  ⚡ Quick Actions                             │
│          │  [Upload Resume] [Connect Gmail]              │
│          │  [Search Candidates] [Import CSV]             │
│          │                                               │
└──────────┴───────────────────────────────────────────────┘
```

**Components:** `<StatsCard />`, `<CandidateTable />`, `<ActionButtons />`, `<Sidebar />`

---

### Page 2: Candidate Search (`/search`)

```
┌──────────────────────────────────────────────────────────┐
│         🔍 Natural Language Search                        │
│  ┌───────────────────────────────────────────────────┐   │
│  │ Find Python developers with 5+ years in SF...    │   │
│  └───────────────────────────────────────────────────┘   │
│                          [Search]                         │
├────────────────────┬─────────────────────────────────────┤
│                    │                                     │
│  Filters           │  Results: 12 candidates             │
│                    │                                     │
│  ☐ Skills          │  ┌─────────────────────────────┐   │
│    ☐ Python        │  │ 🟢 95% Match                │   │
│    ☐ AWS           │  │ John Doe                    │   │
│    ☐ React         │  │ Python ⭐⭐⭐⭐⭐ · AWS ⭐⭐⭐⭐│  │
│    ☐ Docker        │  │ 8 years · San Francisco     │   │
│                    │  │ Why: Expert Python, AWS...   │   │
│  ☐ Experience      │  │ [View Profile] [Compare]    │   │
│    ☐ 3-5 years     │  └─────────────────────────────┘   │
│    ☐ 5-10 years    │                                     │
│    ☐ 10+ years     │  ┌─────────────────────────────┐   │
│                    │  │ 🟡 87% Match                │   │
│  ☐ Location        │  │ Jane Smith                  │   │
│    ☐ USA           │  │ Python ⭐⭐⭐⭐ · AWS ⭐⭐⭐⭐⭐│  │
│    ☐ Remote        │  │ 5 years · NYC (Remote OK)   │   │
│                    │  │ [View Profile] [Compare]    │   │
│  [Clear Filters]   │  └─────────────────────────────┘   │
│                    │                                     │
│                    │  [Load More...]                     │
└────────────────────┴─────────────────────────────────────┘
```

**Components:** `<SearchBar />`, `<FilterPanel />`, `<ResultCard />`, `<MatchBadge />`
**Key UX:** Keyboard shortcut `Ctrl+K` to focus search bar

---

### Page 3: Candidate Profile (`/candidates/:id`)

```
┌──────────────────────────────────────────────────────────┐
│ ◀ Back   John Doe   ⭐⭐⭐⭐☆ (4/5)   Status: Screened  │
├──────────────────────────┬───────────────────────────────┤
│                          │                               │
│ 📋 Contact Info          │ 🔧 Top Skills                │
│ ├─ john@example.com      │ ├─ Python ⭐⭐⭐⭐⭐ (8y)      │
│ ├─ +1-234-567-8900       │ ├─ AWS ⭐⭐⭐⭐ (6y)          │
│ └─ San Francisco, CA     │ ├─ Docker ⭐⭐⭐ (4y)         │
│                          │ └─ PostgreSQL ⭐⭐⭐ (5y)      │
│ 💼 Experience            │                               │
│ ├─ Sr. Engineer, Google  │ 🎓 Education                 │
│ │   2020-2024 (4y)       │ ├─ BS Computer Science       │
│ ├─ Engineer, Microsoft   │ │   MIT, 2018                │
│ │   2018-2020 (2y)       │ └─ Bootcamp Certificate      │
│ └─ Intern, StartupX     │                               │
│     2017 (6mo)           │ ⚡ Actions                    │
│                          │ [Download Resume]             │
│ 📝 Recruiter Notes       │ [Schedule Interview]          │
│ ┌────────────────────┐   │ [Add to Pipeline]             │
│ │ "Great fit for Sr. │   │ [Compare with Others]         │
│ │  role. Strong AWS." │   │                               │
│ │      — Jane        │   │ 🔗 Similar Candidates        │
│ └────────────────────┘   │ Jane S. 88% · Alex M. 85%   │
│                          │                               │
└──────────────────────────┴───────────────────────────────┘
```

**Components:** `<ProfileHeader />`, `<ContactCard />`, `<SkillsPanel />`, `<ExperienceTimeline />`, `<NotesSection />`, `<RelatedCandidates />`

---

### Page 4: Integrations (`/settings/integrations`)

```
┌──────────────────────────────────────────────────────────┐
│  🔗 Integrations & Data Sources                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  📧 Gmail                                               │
│  ├─ Status: ✅ Connected (john@company.com)              │
│  ├─ Last Sync: 2 hours ago                              │
│  ├─ Resumes Found: 45 → Candidates Imported: 42        │
│  └─ [Sync Now] [Disconnect]                             │
│                                                          │
│  💼 HRMS (Simulated)                                    │
│  ├─ Status: ✅ Connected                                │
│  ├─ Candidates Imported: 120                            │
│  └─ [Import CSV] [Settings]                             │
│                                                          │
│  🔗 LinkedIn (Simulated)                                │
│  ├─ Status: ✅ Connected (Mock Data)                    │
│  └─ [Sync Now]                                          │
│                                                          │
│  📤 Manual Upload                                       │
│  └─ [Upload Resume] [Bulk Upload CSV] (Max 25MB)       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Components:** `<IntegrationCard />`, `<GmailConnectButton />`, `<SyncButton />`, `<UploadZone />`

---

### Page 5: Candidate Comparison (`/compare?ids=...`) — Tier 2

```
┌──────────────────────────────────────────────────────────┐
│  Comparing 3 Candidates                                   │
├──────────────────────────────────────────────────────────┤
│              │ John Doe      │ Jane Smith    │ Alex M.    │
│──────────────┼───────────────┼──────────────┼────────────│
│ Match %      │ 🟢 95%       │ 🟡 87%       │ 🟡 78%    │
│ Experience   │ 8 years       │ 5 years      │ 10 years   │
│ Location     │ San Francisco │ NYC (Remote) │ Boston     │
│ Python       │ ⭐⭐⭐⭐⭐    │ ⭐⭐⭐⭐      │ ⭐⭐⭐     │
│ AWS          │ ⭐⭐⭐⭐      │ ⭐⭐⭐⭐⭐    │ ⭐⭐⭐⭐   │
│ Docker       │ ⭐⭐⭐        │ ⭐⭐⭐        │ ⭐⭐⭐⭐⭐ │
└──────────────────────────────────────────────────────────┘
```

---

## 🧩 Component Architecture

```
src/
├── pages/
│   ├── DashboardPage.tsx        ← Orchestrates dashboard widgets
│   ├── CandidateSearchPage.tsx  ← SearchBar + Filters + Results
│   ├── CandidateProfilePage.tsx ← Full candidate view
│   ├── ComparisonPage.tsx       ← Side-by-side (Tier 2)
│   └── IntegrationsPage.tsx     ← Connection management
│
├── components/
│   ├── Navigation/   → Navbar, Sidebar, Breadcrumbs
│   ├── Candidate/    → CandidateCard, CandidateList, SkillBadge
│   ├── Search/       → SearchBar, SearchResults, FilterPanel
│   ├── Resume/       → ResumeUploadZone, ParseProgress
│   ├── Integration/  → GmailConnectButton, IntegrationStatus
│   └── UI/           → Button, Card, Table, Modal, Spinner (shadcn/ui)
│
├── services/
│   ├── api.ts               → Axios instance + interceptors
│   ├── candidateService.ts  → /candidate API calls
│   ├── searchService.ts     → /search API calls
│   └── authService.ts       → JWT token management
│
├── hooks/
│   ├── useAuth.ts           → Login/logout/token state
│   ├── useCandidates.ts     → TanStack Query for candidates
│   └── useDebounce.ts       → Debounced search input
│
└── types/
    ├── candidate.ts
    ├── search.ts
    └── api.ts
```

---

## 📱 Responsive Strategy

| Breakpoint | Layout |
|-----------|--------|
| Desktop (>1024px) | Sidebar + main content |
| Tablet (768-1024px) | Collapsible sidebar, full-width content |
| Mobile (<768px) | Bottom nav, stacked cards, simplified search |

**Priority:** Desktop-first for hackathon demo. Mobile responsiveness is polish work (Hour 36-42).

---

## 🔗 Cross-References
- **API endpoints to connect to:** → [05_DATABASE_AND_API.md](./05_DATABASE_AND_API.md)
- **Frontend file ownership:** → [07_PROJECT_STRUCTURE_AND_OWNERSHIP.md](./07_PROJECT_STRUCTURE_AND_OWNERSHIP.md)
- **When to build each page:** → [08_DEVELOPMENT_TIMELINE.md](./08_DEVELOPMENT_TIMELINE.md)

---

*Source: REFINED_CTO_BLUEPRINT_PROMPT.md (Section 9)*
