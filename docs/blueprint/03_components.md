# TALENTFLOW AI — SHARED COMPONENTS
## File 03 of 05 — Feed after 02_design_system.md

All corrected bugs from review are marked with // FIX:

---

## 1. lib/mock-data.ts (CORRECTED — cand-007 added, source schema updated)

```ts
// FIX: Source type updated to support simulated flag (was just string[])
export type SourceEntry = {
  type: 'email' | 'upload' | 'linkedin' | 'referral' | 'hrms'
  simulated?: boolean   // FIX: flag for LinkedIn simulation badge
}

export type MockCandidate = {
  id: string
  name: string
  email: string
  currentRole: string
  currentCompany: string
  location: string
  experienceYears: number
  experienceLevel: 'Fresher' | 'Mid' | 'Senior' | 'Principal'
  skills: string[]
  score: number                       // number type — FIX: was risk of string
  sources: SourceEntry[]
  addedAt: string
  suggestedMerge: { id: string; name: string; reason: string } | null
  pipelineStage: 'applied' | 'screening' | 'interview' | 'offer' | 'hired'
}

export const mockCandidates: MockCandidate[] = [
  {
    id: 'cand-001',
    name: 'Rahul Sharma',
    email: 'rahul.sharma@gmail.com',
    currentRole: 'Senior Backend Engineer',
    currentCompany: 'Zepto',
    location: 'Bengaluru, KA',
    experienceYears: 6,
    experienceLevel: 'Senior',
    skills: ['Python', 'FastAPI', 'AWS', 'PostgreSQL', 'Docker', 'Redis', 'Kubernetes'],
    score: 87,              // number — not string
    sources: [{ type: 'email' }, { type: 'upload' }],
    addedAt: '2026-03-12',
    suggestedMerge: null,
    pipelineStage: 'screening',
  },
  {
    id: 'cand-002',
    name: 'Priya Mehta',
    email: 'priya.mehta@outlook.com',
    currentRole: 'Full Stack Engineer',
    currentCompany: 'Razorpay',
    location: 'Mumbai, MH',
    experienceYears: 4,
    experienceLevel: 'Mid',
    skills: ['React', 'TypeScript', 'Node.js', 'MongoDB', 'AWS', 'GraphQL'],
    score: 92,
    sources: [{ type: 'linkedin', simulated: true }],   // FIX: simulated flag
    addedAt: '2026-03-11',
    suggestedMerge: null,
    pipelineStage: 'interview',
  },
  {
    id: 'cand-003',
    name: 'Arjun Singh',
    email: 'arjun.singh@startupxyz.com',
    currentRole: 'ML Engineer',
    currentCompany: 'PhonePe',
    location: 'Bengaluru, KA',
    experienceYears: 5,
    experienceLevel: 'Senior',
    skills: ['Python', 'PyTorch', 'TensorFlow', 'AWS', 'Docker', 'Scikit-learn'],
    score: 78,
    sources: [{ type: 'hrms' }],
    addedAt: '2026-03-10',
    suggestedMerge: { id: 'cand-007', name: 'A. Singh', reason: 'name + city match' },
    pipelineStage: 'applied',
  },
  {
    id: 'cand-004',
    name: 'Neha Joshi',
    email: 'neha.joshi@gmail.com',
    currentRole: 'Product Designer',
    currentCompany: 'CRED',
    location: 'Bengaluru, KA',
    experienceYears: 3,
    experienceLevel: 'Mid',
    skills: ['Figma', 'UX Research', 'Prototyping', 'Design Systems', 'Framer'],
    score: 81,
    sources: [{ type: 'referral' }, { type: 'upload' }],
    addedAt: '2026-03-09',
    suggestedMerge: null,
    pipelineStage: 'offer',
  },
  {
    id: 'cand-005',
    name: 'Vikram Nair',
    email: 'vikram.nair@infosys.com',
    currentRole: 'DevOps Engineer',
    currentCompany: 'Infosys',
    location: 'Pune, MH',
    experienceYears: 7,
    experienceLevel: 'Senior',
    skills: ['Kubernetes', 'Docker', 'Terraform', 'AWS', 'GCP', 'CI/CD'],
    score: 74,
    sources: [{ type: 'email' }],
    addedAt: '2026-03-08',
    suggestedMerge: null,
    pipelineStage: 'applied',
  },
  {
    id: 'cand-006',
    name: 'Ananya Krishnan',
    email: 'ananya.k@freshworks.com',
    currentRole: 'Frontend Engineer',
    currentCompany: 'Freshworks',
    location: 'Chennai, TN',
    experienceYears: 2,
    experienceLevel: 'Mid',
    skills: ['React', 'TypeScript', 'Tailwind CSS', 'Jest', 'Storybook'],
    score: 68,
    sources: [{ type: 'upload' }],
    addedAt: '2026-03-07',
    suggestedMerge: null,
    pipelineStage: 'screening',
  },
  // FIX: cand-007 added — was referenced by cand-003 merge but didn't exist
  {
    id: 'cand-007',
    name: 'A. Singh',
    email: 'a.singh.dev@proton.me',
    currentRole: 'Backend Engineer',
    currentCompany: 'Flipkart',
    location: 'Bengaluru, KA',
    experienceYears: 4,
    experienceLevel: 'Mid',
    skills: ['Python', 'Django', 'PostgreSQL', 'AWS', 'Redis'],
    score: 71,
    sources: [{ type: 'email' }],
    addedAt: '2026-03-06',
    suggestedMerge: { id: 'cand-003', name: 'Arjun Singh', reason: 'name + city match' },
    pipelineStage: 'applied',
  },
]

export function getRandomMockCandidate(): MockCandidate {
  return mockCandidates[Math.floor(Math.random() * mockCandidates.length)]
}

// Activity feed mock data
export const mockActivities = [
  { id: 1, type: 'email' as const,    text: 'New resume received from priya.mehta@gmail.com', time: '2 min ago' },
  { id: 2, type: 'parse' as const,    text: 'AI parsed 5 resumes from batch upload',           time: '8 min ago' },
  { id: 3, type: 'merge' as const,    text: 'Duplicate detected: Rahul S. — Review suggested merge', time: '15 min ago' },
  { id: 4, type: 'pipeline' as const, text: 'Ankit Verma moved to Interview Scheduled',         time: '1 hr ago' },
  { id: 5, type: 'shortlist' as const,text: 'Neha Joshi shortlisted for Product Designer role', time: '2 hr ago' },
]
```

---

## 2. components/candidates/AIScoreGauge.tsx (CORRECTED — circumference formula fixed)

```tsx
'use client'
import { motion } from 'framer-motion'

interface AIScoreGaugeProps {
  score: number   // 0–100, must be number type
  size?: 'sm' | 'md' | 'lg'
  animationDelay?: number
}

const SIZE_MAP = {
  sm: { box: 40, r: 15, strokeWidth: 2.5, textSize: 'text-[10px]' },
  md: { box: 52, r: 20, strokeWidth: 3,   textSize: 'text-xs'     },
  lg: { box: 80, r: 32, strokeWidth: 4,   textSize: 'text-base'   },
}

function getScoreColor(score: number): string {
  if (score >= 80) return '#00D4AA'   // teal
  if (score >= 50) return '#F59E0B'   // amber
  return '#FF6B6B'                     // coral
}

export default function AIScoreGauge({ score, size = 'md', animationDelay = 0 }: AIScoreGaugeProps) {
  const { box, r, strokeWidth, textSize } = SIZE_MAP[size]
  const center = box / 2

  // FIX: correct circumference formula — 2πr (not hardcoded 126)
  const circumference = 2 * Math.PI * r
  const offset = circumference - (score / 100) * circumference
  const color = getScoreColor(score)

  return (
    <div
      className="relative inline-flex items-center justify-center"
      aria-label={`AI match score: ${score} out of 100`}   // accessibility
      role="img"
    >
      <svg width={box} height={box} className="-rotate-90">
        {/* Track ring */}
        <circle
          cx={center} cy={center} r={r}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="none"
          className="text-gray-200 dark:text-gray-700"
        />
        {/* Score arc — animates on mount */}
        <motion.circle
          cx={center} cy={center} r={r}
          stroke={color}
          strokeWidth={strokeWidth}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 0.8, ease: 'easeOut', delay: animationDelay }}
        />
      </svg>
      {/* Score number centered over arc */}
      <span className={`absolute font-bold ${textSize}`} style={{ color }}>
        {score}
      </span>
    </div>
  )
}
```

---

## 3. components/candidates/SourceBadge.tsx (CORRECTED — handles simulated flag)

```tsx
import { SourceEntry } from '@/lib/mock-data'

// FIX: COLOR_MAP defined here — was described but never actually defined before
const COLOR_MAP: Record<SourceEntry['type'], string> = {
  email:    '#3B82F6',
  upload:   '#6C63FF',
  linkedin: '#0A66C2',
  referral: '#F97316',
  hrms:     '#059669',
}

const LABEL_MAP: Record<SourceEntry['type'], string> = {
  email:    'Email',
  upload:   'Upload',
  linkedin: 'LinkedIn',
  referral: 'Referral',
  hrms:     'HRMS',
}

interface SourceBadgeProps {
  source: SourceEntry
  showLabel?: boolean
}

export default function SourceBadge({ source, showLabel = true }: SourceBadgeProps) {
  const color = COLOR_MAP[source.type]
  const label = LABEL_MAP[source.type]

  return (
    <span className="inline-flex items-center gap-1 text-xs text-[var(--color-text-muted)]">
      <span
        className="w-2 h-2 rounded-full shrink-0"
        style={{ backgroundColor: color }}
      />
      {showLabel && (
        <>
          {label}
          {/* FIX: simulated flag renders amber badge — was missing */}
          {source.simulated && (
            <span className="ml-0.5 rounded-full bg-amber-100 text-amber-700 dark:bg-amber-950/30 dark:text-amber-400 text-[10px] px-1.5 py-0.5 font-medium">
              Simulated
            </span>
          )}
        </>
      )}
    </span>
  )
}
```

---

## 4. components/candidates/SkillChip.tsx

```tsx
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import { Badge } from '@/components/ui/badge'
import { motion } from 'framer-motion'

interface SkillChipProps {
  skill: string
  count?: number       // how many resume sections mention it
  confidence?: number  // 0–100
  variant?: 'filled' | 'outline'
}

export default function SkillChip({ skill, count = 1, confidence = 100, variant = 'filled' }: SkillChipProps) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <motion.span whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.97 }}>
          <Badge
            variant={variant === 'filled' ? 'secondary' : 'outline'}
            className={
              variant === 'filled'
                ? 'bg-violet-100 text-violet-700 border-violet-200 dark:bg-violet-950/30 dark:text-violet-300 cursor-default'
                : 'text-[var(--color-text-muted)] cursor-default'
            }
          >
            {skill}
            {confidence < 70 && <span className="ml-1 text-amber-500">~</span>}
          </Badge>
        </motion.span>
      </TooltipTrigger>
      <TooltipContent>
        Found in {count} section{count !== 1 ? 's' : ''} · {confidence}% confidence
      </TooltipContent>
    </Tooltip>
  )
}
```

---

## 5. components/candidates/CandidateCardSkeleton.tsx

```tsx
import { Skeleton } from '@/components/ui/skeleton'

export default function CandidateCardSkeleton() {
  return (
    <div
      className="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5 space-y-4"
      aria-busy="true"
      aria-label="Loading candidate"
    >
      {/* Header row */}
      <div className="flex items-start gap-3">
        <Skeleton className="w-12 h-12 rounded-xl shrink-0" />
        <div className="flex-1 space-y-2">
          <Skeleton className="h-4 w-36" />
          <Skeleton className="h-3 w-24" />
          <Skeleton className="h-3 w-28" />
        </div>
        <Skeleton className="w-12 h-12 rounded-full shrink-0" />
      </div>

      {/* Skill chips row */}
      <div className="flex gap-2">
        <Skeleton className="h-6 w-14 rounded-full" />
        <Skeleton className="h-6 w-16 rounded-full" />
        <Skeleton className="h-6 w-12 rounded-full" />
        <Skeleton className="h-6 w-10 rounded-full" />
      </div>

      {/* Source + date row */}
      <div className="flex items-center gap-3">
        <Skeleton className="h-3 w-20" />
        <Skeleton className="h-3 w-16" />
      </div>

      {/* Action buttons row */}
      <div className="flex gap-2 pt-1 border-t border-[var(--color-border)]">
        <Skeleton className="h-8 w-20 rounded-[var(--radius-md)]" />
        <Skeleton className="h-8 w-24 rounded-[var(--radius-md)]" />
        <Skeleton className="h-8 w-28 rounded-[var(--radius-md)]" />
      </div>
    </div>
  )
}
```

---

## 6. components/candidates/CandidateCard.tsx (CORRECTED — split into sub-components)

```tsx
'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { MapPin, Star, Eye } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { TooltipProvider } from '@/components/ui/tooltip'
import AIScoreGauge from './AIScoreGauge'
import SkillChip from './SkillChip'
import SourceBadge from './SourceBadge'
import WhyThisMatchPopover from '@/components/search/WhyThisMatchPopover'
import type { MockCandidate } from '@/lib/mock-data'
import { variants, transitions } from '@/lib/motion.config'

// FIX: avatar gradient from name hash
function getAvatarGradient(name: string): string {
  const gradients = [
    'from-violet-500 to-purple-600',
    'from-teal-400 to-cyan-500',
    'from-orange-400 to-red-500',
    'from-blue-500 to-indigo-600',
    'from-green-400 to-emerald-500',
    'from-pink-500 to-rose-600',
  ]
  const hash = name.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0)
  return gradients[hash % gradients.length]
}

interface CandidateCardProps {
  candidate: MockCandidate
  index?: number
  onShortlist?: (id: string) => void
}

export default function CandidateCard({ candidate, index = 0, onShortlist }: CandidateCardProps) {
  const router = useRouter()
  const [shortlisted, setShortlisted] = useState(false)

  const initials = candidate.name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
  const visibleSkills = candidate.skills.slice(0, 4)
  const overflowCount = candidate.skills.length - 4

  return (
    <TooltipProvider>
      <motion.div
        variants={variants.slideUp}
        transition={{ ...transitions.base, delay: Math.min(index * 0.04, 0.3) }}  // FIX: cap delay at 0.3s
        whileHover={{ y: -3 }}
        whileTap={{ scale: 0.98 }}
        className="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5 cursor-pointer transition-shadow duration-200 hover:shadow-[var(--shadow-hover)] hover:border-violet-200/60 dark:hover:border-violet-700/40"
        style={{ boxShadow: 'var(--shadow-card)' }}
      >
        {/* Header */}
        <div className="flex items-start gap-3 mb-4">
          {/* Avatar */}
          <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${getAvatarGradient(candidate.name)} flex items-center justify-center text-white font-bold text-base shrink-0`}>
            {initials}
          </div>

          {/* Name + role */}
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-[var(--color-text)] truncate">{candidate.name}</h3>
            <p className="text-sm text-[var(--color-text-muted)] truncate">{candidate.currentRole} · {candidate.currentCompany}</p>
            <p className="text-xs text-[var(--color-text-muted)] flex items-center gap-1 mt-0.5">
              <MapPin size={11} />
              {candidate.location}
            </p>
          </div>

          {/* AI Score Gauge — animates with stagger delay */}
          <AIScoreGauge score={candidate.score} size="md" animationDelay={Math.min(index * 0.05, 0.4)} />
        </div>

        {/* Skills */}
        <div className="flex flex-wrap gap-1.5 mb-4">
          {visibleSkills.map(skill => (
            <SkillChip key={skill} skill={skill} count={Math.ceil(Math.random() * 3)} />
          ))}
          {overflowCount > 0 && (
            <span className="inline-flex items-center rounded-full bg-gray-100 dark:bg-gray-800 text-xs text-[var(--color-text-muted)] px-2 py-1">
              +{overflowCount} more
            </span>
          )}
        </div>

        {/* Sources + date */}
        <div className="flex items-center gap-3 mb-4 text-xs text-[var(--color-text-muted)]">
          {candidate.sources.map((source, i) => (
            <SourceBadge key={i} source={source} showLabel />
          ))}
          <span className="ml-auto">Added {candidate.addedAt}</span>
        </div>

        {/* Divider */}
        <div className="border-t border-[var(--color-border)] pt-3 flex gap-2">
          <Button
            size="sm"
            variant={shortlisted ? 'default' : 'outline'}
            className={shortlisted ? 'bg-teal-500 hover:bg-teal-600 text-white' : ''}
            onClick={(e) => {
              e.stopPropagation()
              setShortlisted(prev => !prev)
              onShortlist?.(candidate.id)
            }}
          >
            <Star size={14} className="mr-1" />
            {shortlisted ? 'Shortlisted' : 'Shortlist'}
          </Button>

          <Button
            size="sm"
            variant="outline"
            onClick={(e) => { e.stopPropagation(); router.push(`/candidates/${candidate.id}`) }}
          >
            <Eye size={14} className="mr-1" />
            View Profile
          </Button>

          {/* Why this match popover */}
          <WhyThisMatchPopover candidate={candidate} />
        </div>
      </motion.div>
    </TooltipProvider>
  )
}
```

---

## 7. components/search/WhyThisMatchPopover.tsx

```tsx
'use client'
import { motion } from 'framer-motion'
import { Check, X, MapPin, Sparkles } from 'lucide-react'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Button } from '@/components/ui/button'
import AIScoreGauge from '@/components/candidates/AIScoreGauge'
import type { MockCandidate } from '@/lib/mock-data'

const QUERY_SKILLS = ['Python', 'FastAPI', 'AWS', 'React']  // Simulated from current query

interface Props { candidate: MockCandidate }

export default function WhyThisMatchPopover({ candidate }: Props) {
  const matched = candidate.skills.filter(s => QUERY_SKILLS.includes(s))
  const missing = QUERY_SKILLS.filter(s => !candidate.skills.includes(s))

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          size="sm"
          variant="ghost"
          className="ml-auto text-violet-600 hover:text-violet-700 text-xs"
          onClick={e => e.stopPropagation()}
        >
          Why this match? ↗
        </Button>
      </PopoverTrigger>
      <PopoverContent
        className="w-[380px] p-0 rounded-[var(--radius-xl)] border-violet-200/60 shadow-[var(--shadow-panel)] overflow-hidden"
        onClick={e => e.stopPropagation()}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.18, ease: 'easeOut' }}
        >
          {/* Score header */}
          <div className="flex items-center gap-4 p-5 border-b border-[var(--color-border)] bg-gradient-to-r from-violet-50 to-teal-50 dark:from-violet-950/20 dark:to-teal-950/20">
            <AIScoreGauge score={candidate.score} size="lg" />
            <div>
              <p className="text-3xl font-bold" style={{ color: candidate.score >= 80 ? '#00D4AA' : candidate.score >= 50 ? '#F59E0B' : '#FF6B6B' }}>
                {candidate.score}
                <span className="text-base font-normal text-[var(--color-text-muted)]">/100</span>
              </p>
              <p className="text-sm font-semibold">{candidate.score >= 80 ? 'Strong Match' : candidate.score >= 50 ? 'Good Match' : 'Partial Match'}</p>
            </div>
          </div>

          {/* Breakdown */}
          <div className="p-5 space-y-4">
            {/* Skills */}
            <div>
              <p className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-2">Skills Match</p>
              <div className="flex flex-wrap gap-1.5">
                {matched.map((s, i) => (
                  <motion.span
                    key={s}
                    initial={{ opacity: 0, x: -6 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.03 }}
                    className="inline-flex items-center gap-1 rounded-full bg-teal-100 text-teal-700 dark:bg-teal-950/30 dark:text-teal-400 text-xs px-2.5 py-1"
                  >
                    <Check size={10} /> {s}
                  </motion.span>
                ))}
                {missing.map((s, i) => (
                  <motion.span
                    key={s}
                    initial={{ opacity: 0, x: -6 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: (matched.length + i) * 0.03 }}
                    className="inline-flex items-center gap-1 rounded-full bg-gray-100 text-[var(--color-text-muted)] dark:bg-gray-800 text-xs px-2.5 py-1 line-through"
                  >
                    <X size={10} /> {s}
                  </motion.span>
                ))}
              </div>
            </div>

            {/* Experience */}
            <div>
              <p className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Experience</p>
              <p className="text-sm">
                <span className="font-semibold">{candidate.experienceLevel}</span>
                {' '}({candidate.experienceYears} yrs)
                <span className="ml-2 text-xs text-teal-600 dark:text-teal-400">
                  {candidate.experienceYears >= 5 ? '+1yr above requirement' : 'Meets requirement'}
                </span>
              </p>
            </div>

            {/* Location */}
            <div>
              <p className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Location</p>
              <p className="text-sm flex items-center gap-1.5">
                <MapPin size={13} className="text-[var(--color-text-muted)]" />
                {candidate.location}
                <span className="rounded-full bg-teal-100 text-teal-700 text-xs px-2 py-0.5">100% match</span>
              </p>
            </div>

            {/* AI Summary */}
            <div className="rounded-[var(--radius-md)] bg-violet-50 dark:bg-violet-950/20 p-3">
              <p className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-1.5 flex items-center gap-1">
                <Sparkles size={11} className="text-violet-500" /> AI Summary
              </p>
              <p className="text-xs italic text-[var(--color-text-muted)] leading-relaxed">
                Strong {candidate.experienceLevel.toLowerCase()} profile at {candidate.currentCompany}.
                {matched.length > 0 && ` Confirmed: ${matched.slice(0, 2).join(', ')}.`}
                {missing.length > 0 && ` Gap: ${missing[0]} — review for transferable skills.`}
              </p>
            </div>
          </div>
        </motion.div>
      </PopoverContent>
    </Popover>
  )
}
```

---

## 8. Activity Feed — icon/color mapping (CORRECTED — was described but never defined)

```tsx
// components/dashboard/ActivityFeed.tsx
import { Mail, Sparkles, GitMerge, ArrowRight, Star } from 'lucide-react'
import { motion } from 'framer-motion'
import { mockActivities } from '@/lib/mock-data'

// FIX: explicit icon + color mapping — was listed in text but never coded
const ACTIVITY_CONFIG = {
  email:     { icon: Mail,       color: '#3B82F6', label: 'Email'     },
  parse:     { icon: Sparkles,   color: '#6C63FF', label: 'AI Parse'  },
  merge:     { icon: GitMerge,   color: '#F59E0B', label: 'Dedup'     },
  pipeline:  { icon: ArrowRight, color: '#00D4AA', label: 'Pipeline'  },
  shortlist: { icon: Star,       color: '#F59E0B', label: 'Shortlist' },
} as const

export default function ActivityFeed() {
  return (
    // FIX: aria-live for screen readers — was missing
    <div className="space-y-1" aria-live="polite" aria-label="Recent activity">
      {mockActivities.map((activity, i) => {
        const config = ACTIVITY_CONFIG[activity.type]
        const Icon = config.icon

        return (
          <motion.div
            key={activity.id}
            initial={{ opacity: 0, x: -12 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className="group flex items-start gap-3 py-3 px-3 rounded-[var(--radius-md)] hover:bg-[var(--color-surface-2)] transition-colors cursor-pointer"
          >
            {/* Timeline dot */}
            <div className="relative flex flex-col items-center shrink-0">
              <div
                className="w-2.5 h-2.5 rounded-full mt-1"
                style={{ backgroundColor: config.color }}
              />
              {i < mockActivities.length - 1 && (
                <div className="w-px flex-1 min-h-[24px] mt-1 border-l-2 border-dashed border-[var(--color-border)]" />
              )}
            </div>

            <div className="flex-1 min-w-0">
              <p className="text-sm text-[var(--color-text)] leading-snug">{activity.text}</p>
              <p className="text-xs text-[var(--color-text-muted)] mt-0.5">{activity.time}</p>
            </div>

            <span className="text-xs text-violet-600 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
              View →
            </span>
          </motion.div>
        )
      })}
    </div>
  )
}
```

---

## 9. Upload SSE — Corrected with cleanup (CRITICAL memory leak fix)

```tsx
// components/upload/ResumeUploadZone.tsx — SSE section
// FIX: useEffect cleanup calls es.close() to prevent memory leak

function useParseSSE(uploadId: string | null) {
  const [status, setStatus] = useState<'idle' | 'uploading' | 'parsing' | 'complete' | 'error'>('idle')
  const [candidate, setCandidate] = useState(null)

  useEffect(() => {
    if (!uploadId) return

    // FIX: SSE cleanup on unmount or uploadId change
    const es = new EventSource(`${process.env.NEXT_PUBLIC_API_URL}/events/${uploadId}`)

    es.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.status === 'uploading') setStatus('uploading')
      if (data.status === 'parsing')   setStatus('parsing')
      if (data.status === 'complete') {
        setStatus('complete')
        setCandidate(data.candidate)
        es.close()   // close after complete
      }
      if (data.status === 'error') {
        setStatus('error')
        es.close()
      }
    }

    es.onerror = () => {
      setStatus('error')
      es.close()
    }

    // FIX: cleanup function — prevents memory leak on unmount
    return () => {
      es.close()
    }
  }, [uploadId])

  return { status, candidate }
}
```

---

## 10. Progress Bar — role="progressbar" (accessibility fix)

```tsx
// FIX: parsing progress bar needs role="progressbar" — was missing
<div
  role="progressbar"
  aria-valuenow={progress}
  aria-valuemin={0}
  aria-valuemax={100}
  aria-label="Resume parsing progress"
  className="h-1 bg-gray-200 rounded-full overflow-hidden"
>
  <motion.div
    className="h-full bg-violet-600 rounded-full"
    initial={{ width: '0%' }}
    animate={{ width: `${progress}%` }}
    transition={{ duration: 0.4, ease: 'easeOut' }}
  />
</div>
```
