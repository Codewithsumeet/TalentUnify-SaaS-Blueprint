# TALENTFLOW AI — PAGE SPECS
## File 04 of 05 — Feed after 03_components.md

All icons must be explicitly imported from lucide-react. Do not assume global imports.

---

## GLOBAL ICON IMPORTS (include in every file that uses icons)

```tsx
import {
  LayoutDashboard, Search, Kanban, GitCompare, Plug, Settings,
  MapPin, Mail, Upload, Sparkles, Star, Eye, Bell, Sun, Moon,
  Monitor, ChevronRight, ChevronLeft, Check, X, GitMerge,
  ArrowRight, Users, Clock, Briefcase, Building2, UserPlus,
  FileText, AlertCircle, CheckCircle, Loader2
} from 'lucide-react'
```

---

## PAGE 1 — Dashboard (`/dashboard`)

```tsx
// app/(app)/dashboard/page.tsx
import { motion } from 'framer-motion'
import { variants } from '@/lib/motion.config'
import StatCard from '@/components/dashboard/StatCard'
import ActivityFeed from '@/components/dashboard/ActivityFeed'
import SourceDonutChart from '@/components/dashboard/SourceDonutChart'
import { Users, Clock, Star, Briefcase, Upload, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'

const stats = [
  { label: 'Total Candidates', value: 1284, icon: Users,     accent: 'violet', delta: '+23 this week',  up: true  },
  { label: 'Pending Review',   value: 47,   icon: Clock,     accent: 'amber',  delta: '12 urgent',      up: false },
  { label: 'Shortlisted',      value: 89,   icon: Star,      accent: 'teal',   delta: '+8 today',       up: true  },
  { label: 'Open Roles',       value: 6,    icon: Briefcase, accent: 'coral',  delta: '2 closing soon', up: false },
]

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text)]">Welcome back, Priya 👋</h1>
          <p className="text-sm text-[var(--color-text-muted)] mt-1">Here's what's happening today.</p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline" size="sm"><Upload size={15} className="mr-1.5" /> Upload Resumes</Button>
          <Button size="sm" className="bg-violet-600 hover:bg-violet-700 text-white">
            <Sparkles size={15} className="mr-1.5" /> AI Search
          </Button>
        </div>
      </div>

      {/* Stat cards grid */}
      <motion.div
        variants={variants.stagger}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
      >
        {stats.map((stat, i) => (
          <StatCard key={stat.label} {...stat} index={i} />
        ))}
      </motion.div>

      {/* Content grid */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Activity feed — 3/5 */}
        <div className="lg:col-span-3 rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
          <h2 className="font-semibold text-[var(--color-text)] mb-4">Recent Activity</h2>
          <ActivityFeed />
        </div>

        {/* Donut chart — 2/5 */}
        <div className="lg:col-span-2 rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
          <h2 className="font-semibold text-[var(--color-text)] mb-4">Sources</h2>
          <SourceDonutChart />
        </div>
      </div>

      {/* Pipeline health strip */}
      <div className="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
        <h2 className="font-semibold text-[var(--color-text)] mb-4">Pipeline Health</h2>
        <PipelineHealthStrip />
      </div>
    </div>
  )
}

// Inline sub-components
function PipelineHealthStrip() {
  const roles = [
    { role: 'Senior Backend Eng.', applied: 24, screening: 8, interview: 3, offer: 1 },
    { role: 'Product Designer',    applied: 12, screening: 5, interview: 2, offer: 0 },
    { role: 'ML Engineer',         applied: 31, screening: 3, interview: 1, offer: 0 },
  ]
  const stages = [
    { key: 'applied',   label: 'Applied',   color: '#3B82F6' },
    { key: 'screening', label: 'Screening', color: '#6C63FF' },
    { key: 'interview', label: 'Interview', color: '#F59E0B' },
    { key: 'offer',     label: 'Offer',     color: '#00D4AA' },
  ] as const

  return (
    <div className="space-y-3">
      {roles.map(r => (
        <div key={r.role} className="flex items-center gap-4">
          <span className="text-sm font-medium text-[var(--color-text)] w-44 shrink-0">{r.role}</span>
          <div className="flex gap-2">
            {stages.map(s => (
              <span key={s.key}
                className="inline-flex items-center gap-1.5 rounded-full text-xs font-medium px-2.5 py-1"
                style={{ backgroundColor: `${s.color}15`, color: s.color, border: `1px solid ${s.color}30` }}
              >
                {s.label}: {r[s.key]}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
```

### StatCard Component

```tsx
// components/dashboard/StatCard.tsx
'use client'
import { motion } from 'framer-motion'
import { NumberTicker } from '@/components/ui/number-ticker'   // from Magic UI
import { variants } from '@/lib/motion.config'
import type { LucideIcon } from 'lucide-react'

const ACCENT_COLORS = {
  violet: { bg: '#6C63FF15', icon: '#6C63FF', bar: 'from-violet-400 to-violet-600' },
  amber:  { bg: '#F59E0B15', icon: '#F59E0B', bar: 'from-amber-400 to-amber-600'   },
  teal:   { bg: '#00D4AA15', icon: '#00D4AA', bar: 'from-teal-400 to-teal-600'     },
  coral:  { bg: '#FF6B6B15', icon: '#FF6B6B', bar: 'from-coral-400 to-coral-600'   },
}

interface StatCardProps {
  label: string
  value: number    // MUST be number — FIX: was risk of passing string
  icon: LucideIcon
  accent: keyof typeof ACCENT_COLORS
  delta: string
  up: boolean
  index?: number
}

export default function StatCard({ label, value, icon: Icon, accent, delta, up, index = 0 }: StatCardProps) {
  const colors = ACCENT_COLORS[accent]

  return (
    <motion.div
      variants={variants.slideUp}
      whileHover={{ y: -2 }}
      className="relative rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-6 overflow-hidden"
      style={{ boxShadow: 'var(--shadow-card)' }}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="w-10 h-10 rounded-[var(--radius-md)] flex items-center justify-center"
          style={{ backgroundColor: colors.bg }}>
          <Icon size={20} style={{ color: colors.icon }} />
        </div>
        <span className={`text-xs font-medium px-2 py-1 rounded-full ${up ? 'bg-teal-100 text-teal-700 dark:bg-teal-950/30 dark:text-teal-400' : 'bg-amber-100 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400'}`}>
          {delta}
        </span>
      </div>

      {/* FIX: value passed as number type to NumberTicker */}
      <NumberTicker value={value} className="text-3xl font-bold text-[var(--color-text)]" />
      <p className="text-sm text-[var(--color-text-muted)] mt-1">{label}</p>

      {/* Bottom accent bar */}
      <div className={`absolute bottom-0 left-0 right-0 h-[3px] bg-gradient-to-r ${colors.bar}`} />
    </motion.div>
  )
}
```

---

## PAGE 2 — Search (`/search`)

```tsx
// app/(app)/search/page.tsx
// FIX: split into sub-components — was too many responsibilities in one file
'use client'
import { useState } from 'react'
import { motion } from 'framer-motion'
import { variants } from '@/lib/motion.config'
import SearchBar from '@/components/search/SearchBar'
import FilterSidebar from '@/components/search/FilterSidebar'
import CandidateCard from '@/components/candidates/CandidateCard'
import CandidateCardSkeleton from '@/components/candidates/CandidateCardSkeleton'
import { Sheet, SheetContent } from '@/components/ui/sheet'
import { mockCandidates, type MockCandidate } from '@/lib/mock-data'
import { Loader2 } from 'lucide-react'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<MockCandidate[]>(mockCandidates)
  const [selectedCandidate, setSelectedCandidate] = useState<MockCandidate | null>(null)

  const handleSearch = async (q: string) => {
    setLoading(true)
    setQuery(q)
    await new Promise(r => setTimeout(r, 800))   // simulate API
    setResults(mockCandidates)
    setLoading(false)
  }

  return (
    <div className="space-y-6">
      {/* Search bar — centered hero */}
      <div className="flex flex-col items-center gap-4">
        <SearchBar onSearch={handleSearch} />
      </div>

      {/* Parsing queue banner */}
      <ParsingBanner />

      <div className="flex gap-6">
        {/* Filter sidebar */}
        <FilterSidebar />

        {/* Results grid */}
        <div className="flex-1">
          {loading ? (
            <motion.div
              variants={variants.stagger}
              initial="hidden"
              animate="visible"
              className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"
            >
              {Array.from({ length: 6 }).map((_, i) => (
                <motion.div key={i} variants={variants.slideUp}>
                  <CandidateCardSkeleton />
                </motion.div>
              ))}
            </motion.div>
          ) : (
            <motion.div
              variants={variants.stagger}
              initial="hidden"
              animate="visible"
              className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"
            >
              {results.map((candidate, i) => (
                <CandidateCard
                  key={candidate.id}
                  candidate={candidate}
                  index={i}
                  onShortlist={() => {}}
                />
              ))}
            </motion.div>
          )}
        </div>
      </div>

      {/* Slide-in detail Sheet */}
      <Sheet open={!!selectedCandidate} onOpenChange={() => setSelectedCandidate(null)}>
        <SheetContent side="right" className="w-[560px] sm:max-w-[560px] overflow-y-auto">
          {selectedCandidate && <p className="p-6">Detail panel for {selectedCandidate.name}</p>}
        </SheetContent>
      </Sheet>
    </div>
  )
}

// Parsing queue banner — shows when SSE uploads are in progress
function ParsingBanner() {
  const parsingCount = 0  // connect to upload state
  if (parsingCount === 0) return null
  return (
    <motion.div initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }}
      className="rounded-[var(--radius-lg)] bg-violet-50 dark:bg-violet-950/20 border border-violet-200 dark:border-violet-800 p-3 flex items-center gap-3"
    >
      <Loader2 className="animate-spin text-violet-500 shrink-0" size={18} />
      <span className="text-sm text-violet-700 dark:text-violet-400 font-medium">
        Parsing {parsingCount} resume{parsingCount !== 1 ? 's' : ''}...
      </span>
    </motion.div>
  )
}
```

### SearchBar Component

```tsx
// components/search/SearchBar.tsx
'use client'
import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Sparkles } from 'lucide-react'

const PLACEHOLDERS = [
  'Find React engineers in Pune with 4+ years...',
  'Show senior designers open to remote...',
  'Backend engineers with AWS + startup experience...',
  'Freshers with Python graduating 2024...',
  'Find candidates similar to our best hire...',
]

const QUICK_FILTERS = ['React', 'Python', 'Remote', 'Senior', 'Bangalore', 'AWS', 'Fresher', 'ML']

interface SearchBarProps {
  onSearch: (query: string) => void
}

export default function SearchBar({ onSearch }: SearchBarProps) {
  const [value, setValue] = useState('')
  const [placeholderIdx, setPlaceholderIdx] = useState(0)
  const [focused, setFocused] = useState(false)
  const [activeFilters, setActiveFilters] = useState<string[]>([])
  const inputRef = useRef<HTMLInputElement>(null)

  // Cycle placeholder text
  useEffect(() => {
    if (focused) return
    const t = setInterval(() => setPlaceholderIdx(i => (i + 1) % PLACEHOLDERS.length), 3000)
    return () => clearInterval(t)
  }, [focused])

  const handleSubmit = () => onSearch(value)

  const toggleFilter = (f: string) => {
    setActiveFilters(prev =>
      prev.includes(f) ? prev.filter(x => x !== f) : [...prev, f]
    )
    setValue(prev => prev.includes(f) ? prev.replace(f, '').trim() : `${prev} ${f}`.trim())
  }

  return (
    <div className="w-full max-w-[860px] space-y-3">
      {/* Main search input */}
      <div className="relative">
        {/* Sparkle icon with gradient */}
        <div className="absolute left-4 top-1/2 -translate-y-1/2 pointer-events-none">
          <Sparkles size={20} style={{
            background: 'linear-gradient(135deg, #6C63FF, #00D4AA)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }} />
        </div>

        <input
          ref={inputRef}
          value={value}
          onChange={e => setValue(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSubmit()}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          placeholder={PLACEHOLDERS[placeholderIdx]}
          className="w-full h-14 pl-12 pr-5 rounded-[14px] text-base bg-[var(--color-surface)] border-2 transition-all duration-200 outline-none placeholder:text-[var(--color-text-muted)] text-[var(--color-text)]"
          style={{
            borderColor: focused ? '#6C63FF' : 'var(--color-border)',
            boxShadow: focused
              ? '0 0 0 4px rgba(108,99,255,0.12), 0 4px 24px rgba(108,99,255,0.08)'
              : '0 4px 24px rgba(108,99,255,0.06)',
          }}
        />
      </div>

      {/* Quick filter chips */}
      <div className="flex flex-wrap gap-2">
        {QUICK_FILTERS.map(f => (
          <button
            key={f}
            onClick={() => toggleFilter(f)}
            className={`rounded-full px-3 py-1 text-sm font-medium border transition-all duration-150 ${
              activeFilters.includes(f)
                ? 'bg-violet-600 text-white border-violet-600'
                : 'bg-transparent text-[var(--color-text-muted)] border-[var(--color-border)] hover:border-violet-300 hover:text-violet-600'
            }`}
          >
            {f}
          </button>
        ))}
      </div>
    </div>
  )
}
```

---

## PAGE 3 — Candidate Profile (`/candidates/[id]`)

```tsx
// app/(app)/candidates/[id]/page.tsx
'use client'
import { useParams } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { MapPin, Mail, Phone, Star, GitMerge, X, Link } from 'lucide-react'
import AIScoreGauge from '@/components/candidates/AIScoreGauge'
import SkillChip from '@/components/candidates/SkillChip'
import SourceBadge from '@/components/candidates/SourceBadge'
import { mockCandidates } from '@/lib/mock-data'

export default function CandidateProfilePage() {
  const { id } = useParams()
  const candidate = mockCandidates.find(c => c.id === id) ?? mockCandidates[0]

  return (
    <div className="space-y-6">
      {/* Hero section */}
      <div className="relative rounded-[var(--radius-xl)] overflow-hidden p-8"
        style={{ background: 'linear-gradient(135deg, #1A1A2E 0%, #2D1B69 100%)' }}>

        {/* Noise texture */}
        <div className="absolute inset-0 opacity-[0.03]"
          style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 256 256\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noise)\'/%3E%3C/svg%3E")' }} />

        <div className="relative flex items-start gap-6">
          {/* Avatar */}
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-violet-500 to-teal-400 flex items-center justify-center text-white text-2xl font-bold shrink-0">
            {candidate.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
          </div>

          <div className="flex-1 min-w-0">
            <h1 className="text-3xl font-bold text-white">{candidate.name}</h1>
            <p className="text-violet-300 mt-1">{candidate.currentRole} · {candidate.currentCompany}</p>
            <p className="text-gray-400 text-sm flex items-center gap-1 mt-1">
              <MapPin size={13} /> {candidate.location}
            </p>
            <div className="flex gap-2 mt-3 flex-wrap">
              {candidate.sources.map((s, i) => <SourceBadge key={i} source={s} />)}
            </div>
          </div>

          <AIScoreGauge score={candidate.score} size="lg" />
        </div>

        {/* Suggested merge alert */}
        {candidate.suggestedMerge && (
          <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }}
            className="relative mt-6 rounded-[var(--radius-lg)] border border-amber-400/40 bg-amber-900/20 p-4 flex items-start gap-3"
          >
            <GitMerge size={18} className="text-amber-400 shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="font-medium text-amber-200 text-sm">Possible duplicate detected</p>
              <p className="text-amber-400/80 text-xs mt-0.5">
                Matches {candidate.suggestedMerge.name} · {candidate.suggestedMerge.reason}
              </p>
            </div>
            <Button size="sm" variant="outline" className="border-amber-400/40 text-amber-300 hover:bg-amber-900/40 text-xs">
              Review Side-by-Side →
            </Button>
          </motion.div>
        )}

        {/* Actions */}
        <div className="relative mt-6 flex gap-3 flex-wrap">
          <Button className="bg-teal-500 hover:bg-teal-600 text-white"><Star size={15} className="mr-1.5" /> Shortlist</Button>
          <Button variant="outline" className="border-white/20 text-white hover:bg-white/10"><Mail size={15} className="mr-1.5" /> Send Email</Button>
          <Button variant="ghost" className="text-red-400 hover:bg-red-900/20 hover:text-red-300 ml-auto"><X size={15} className="mr-1.5" /> Reject</Button>
        </div>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="experience">Experience</TabsTrigger>
          <TabsTrigger value="activity">Activity</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="mt-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Skills */}
            <div className="lg:col-span-2 rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
              <h3 className="font-semibold mb-4 text-[var(--color-text)]">Skills</h3>
              <div className="flex flex-wrap gap-2">
                {candidate.skills.map(skill => (
                  <SkillChip key={skill} skill={skill} count={Math.ceil(Math.random() * 3)} />
                ))}
              </div>
            </div>
            {/* Contact */}
            <div className="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-6 space-y-3">
              <h3 className="font-semibold mb-4 text-[var(--color-text)]">Contact</h3>
              <div className="flex items-center gap-2 text-sm"><Mail size={14} className="text-violet-500" />{candidate.email}</div>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="experience" className="mt-4">
          <ExperienceTimeline />
        </TabsContent>

        <TabsContent value="activity" className="mt-4">
          <div className="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
            <p className="text-sm text-[var(--color-text-muted)]">Activity log coming soon.</p>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

function ExperienceTimeline() {
  const roles = [
    { company: 'Zepto', title: 'Senior Backend Engineer', duration: 'Jan 2022 – Present (2y 3m)', summary: 'Built payment microservices handling 2M+ daily transactions. Led k8s migration.', current: true },
    { company: 'Razorpay', title: 'Software Engineer', duration: 'Jun 2019 – Dec 2021 (2y 6m)', summary: 'Developed core payment gateway APIs. Owned fraud detection pipeline.', current: false },
    { company: 'Infosys', title: 'Junior Developer', duration: 'Jan 2018 – May 2019 (1y 4m)', summary: 'Maintained Java Spring Boot services for banking client.', current: false },
  ]
  return (
    <div className="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-6 space-y-0">
      {roles.map((role, i) => (
        <div key={i} className="flex gap-4">
          <div className="flex flex-col items-center">
            <div className={`w-3 h-3 rounded-full border-2 border-[var(--color-surface)] shrink-0 mt-1 ${role.current ? 'bg-teal-400 animate-[pulse-teal_2s_infinite]' : 'bg-violet-500'}`} />
            {i < roles.length - 1 && <div className="w-0.5 flex-1 my-1" style={{ background: 'linear-gradient(to bottom, #6C63FF, #00D4AA)' }} />}
          </div>
          <div className="pb-6 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <h4 className="font-semibold text-[var(--color-text)]">{role.title}</h4>
              {role.current && <span className="text-xs rounded-full bg-teal-100 text-teal-700 px-2 py-0.5">Current</span>}
            </div>
            <p className="text-sm text-violet-600 dark:text-violet-400">{role.company}</p>
            <p className="text-xs text-[var(--color-text-muted)] mt-0.5">{role.duration}</p>
            <p className="text-sm text-[var(--color-text)] mt-2 leading-relaxed">{role.summary}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
```

---

## PAGE 4 — Compare (`/compare`)

```tsx
// app/(app)/compare/page.tsx
'use client'
import { useState } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { Check, Minus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import AIScoreGauge from '@/components/candidates/AIScoreGauge'
import SourceBadge from '@/components/candidates/SourceBadge'
import { mockCandidates, type MockCandidate } from '@/lib/mock-data'

export default function ComparePage() {
  const searchParams = useSearchParams()
  const [candA, setCandA] = useState<MockCandidate | null>(
    mockCandidates.find(c => c.id === searchParams.get('a')) ?? null
  )
  const [candB, setCandB] = useState<MockCandidate | null>(
    mockCandidates.find(c => c.id === searchParams.get('b')) ?? null
  )

  const allSkills = [...new Set([...(candA?.skills ?? []), ...(candB?.skills ?? [])])]

  if (!candA && !candB) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4 text-[var(--color-text-muted)]">
        <div className="text-6xl">⚖️</div>
        <h2 className="text-xl font-semibold text-[var(--color-text)]">Compare Candidates</h2>
        <p className="text-sm">Select two candidates to see a side-by-side comparison.</p>
        <Button onClick={() => { setCandA(mockCandidates[0]); setCandB(mockCandidates[1]) }}>
          Load Example Comparison
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-[var(--color-text)]">Compare Candidates</h1>

      <div className="grid grid-cols-2 gap-6">
        {[candA, candB].map((cand, side) => cand ? (
          <div key={cand.id} className="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] overflow-hidden">
            {/* Hero */}
            <div className="p-6 bg-gradient-to-br from-violet-50 to-teal-50 dark:from-violet-950/20 dark:to-teal-950/20 flex items-start gap-4">
              <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-violet-500 to-teal-400 flex items-center justify-center text-white text-xl font-bold shrink-0">
                {cand.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-bold text-lg text-[var(--color-text)]">{cand.name}</h3>
                <p className="text-sm text-[var(--color-text-muted)]">{cand.currentRole}</p>
                <p className="text-sm text-[var(--color-text-muted)]">{cand.location} · {cand.experienceYears}yr</p>
                <div className="flex gap-1 mt-2 flex-wrap">
                  {cand.sources.map((s, i) => <SourceBadge key={i} source={s} />)}
                </div>
              </div>
              <AIScoreGauge score={cand.score} size="md" />
            </div>

            {/* Skills diff */}
            <div className="p-6">
              <h4 className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-3">Skills</h4>
              <div className="flex flex-wrap gap-1.5">
                {allSkills.map(skill => {
                  const has = cand.skills.includes(skill)
                  const other = side === 0 ? candB : candA
                  const shared = other?.skills.includes(skill)
                  return (
                    <span key={skill} className={`inline-flex items-center gap-1 rounded-full text-xs px-2.5 py-1 border font-medium ${
                      has && shared   ? 'bg-teal-100 text-teal-700 border-teal-200 dark:bg-teal-950/30 dark:text-teal-400'
                      : has           ? 'bg-violet-100 text-violet-700 border-violet-200 dark:bg-violet-950/30 dark:text-violet-400'
                      : 'bg-gray-100 text-gray-400 border-gray-200 line-through dark:bg-gray-800'
                    }`}>
                      {has && <Check size={10} />}
                      {!has && <Minus size={10} />}
                      {skill}
                    </span>
                  )
                })}
              </div>
            </div>

            {/* CTA */}
            <div className="px-6 pb-6">
              <Button className="w-full bg-teal-500 hover:bg-teal-600 text-white">
                Add to Shortlist
              </Button>
            </div>
          </div>
        ) : (
          <div key={side} className="rounded-[var(--radius-lg)] border-2 border-dashed border-[var(--color-border)] flex items-center justify-center min-h-[300px] text-[var(--color-text-muted)]">
            <p className="text-sm">Select a candidate</p>
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="flex gap-4 text-xs text-[var(--color-text-muted)]">
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-teal-200" /> Shared skill</span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-violet-200" /> Unique skill</span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-gray-200" /> Missing</span>
      </div>
    </div>
  )
}
```

---

## PAGE 5, 6, 7 — Pipeline, Integrations, Settings

Pipeline page: uses KanbanBoard component from `components/pipeline/KanbanBoard.tsx` with `@dnd-kit`. Reference Section 7 of the original spec for the full Kanban layout. Key requirements:
- 5 columns: Applied | Screening | Interview | Offer | Hired
- `DndContext` wraps all columns, `useSortable` on each card
- Drag state: `scale(1.03) rotate(3deg)` via `DragOverlay`
- Column drop target glow uses `useDroppable` `isOver` state
- Bulk selection bar uses `AnimatePresence` fixed bottom-8 centered
- Keyboard alternative: click card → dropdown to move stage (accessibility)

Integrations page: uses IntegrationCard grid. Status pills: teal pulse (connected), amber (simulated), gray (disconnected). LinkedIn cards show "Simulated" amber pill. HRMS card shows "connected" with processedCount.

Settings page: see stub in 02_design_system.md — must not 404.
