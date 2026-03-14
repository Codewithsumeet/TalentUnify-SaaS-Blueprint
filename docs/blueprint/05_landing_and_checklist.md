# TALENTFLOW AI — LANDING PAGE & FINAL CHECKLIST
## File 05 of 05 — Feed last, after all components and pages are built

---

## LANDING PAGE — `app/(marketing)/page.tsx`

Build in this section order. Each section references 21st.dev component categories as visual inspiration.

---

### SECTION 1: MARKETING NAVBAR

```tsx
'use client'
import { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { ShimmerButton } from '@/components/ui/shimmer-button'  // Magic UI

export function MarketingNav() {
  const [scrolled, setScrolled] = useState(false)
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header className={`fixed top-0 inset-x-0 z-50 h-16 flex items-center justify-between px-6 transition-all duration-300 ${scrolled ? 'backdrop-blur-md bg-white/80 dark:bg-[#0D0D1A]/80 border-b border-[var(--color-border)] shadow-sm' : ''}`}>
      {/* Logo */}
      <div className="flex items-center gap-2.5">
        <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-violet-500 to-teal-400" />
        <span className="font-bold text-[var(--color-text)]">TalentFlow AI</span>
      </div>

      {/* Nav links */}
      <nav className="hidden md:flex items-center gap-6 text-sm text-[var(--color-text-muted)]">
        {['Features', 'Pricing', 'Docs'].map(item => (
          <a key={item} href={`#${item.toLowerCase()}`}
            className="hover:text-[var(--color-text)] transition-colors">{item}</a>
        ))}
      </nav>

      {/* CTAs */}
      <div className="flex items-center gap-3">
        <Link href="/dashboard" className="text-sm text-[var(--color-text-muted)] hover:text-[var(--color-text)] transition-colors hidden md:block">
          Sign In
        </Link>
        <ShimmerButton className="text-sm h-9 px-5 rounded-[var(--radius-md)]">
          Get Started →
        </ShimmerButton>
      </div>
    </header>
  )
}
```

---

### SECTION 2: HERO
**21st.dev inspiration: Heros category — bold headline + animated sub + dual CTA + product mockup**

```tsx
import { AnimatedGradientText } from '@/components/ui/animated-gradient-text'  // Magic UI
import { ShimmerButton } from '@/components/ui/shimmer-button'
import { motion } from 'framer-motion'

function HeroSection() {
  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center px-6 pt-24 pb-16 overflow-hidden">
      {/* Background — radial violet glow */}
      <div className="absolute inset-0 bg-gradient-to-b from-[#FAFAFA] to-white dark:from-[#0D0D1A] dark:to-[#0D0D1A]" />
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[500px] rounded-full bg-violet-400/10 dark:bg-violet-600/15 blur-[120px]" />
        <div className="absolute bottom-1/3 left-1/4 w-[400px] h-[300px] rounded-full bg-teal-400/10 dark:bg-teal-600/10 blur-[100px]" />
      </div>

      <div className="relative max-w-4xl mx-auto text-center space-y-6">
        {/* Badge pill */}
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <span className="inline-flex items-center gap-2 rounded-full border border-violet-200 bg-violet-50 dark:bg-violet-950/30 dark:border-violet-800 text-violet-700 dark:text-violet-400 text-sm px-4 py-1.5">
            ✨ AI-Powered Recruitment Platform
          </span>
        </motion.div>

        {/* Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-5xl md:text-6xl font-bold leading-tight text-[var(--color-text)]"
        >
          Your entire hiring pipeline,
          <br />
          unified by{' '}
          <AnimatedGradientText>AI.</AnimatedGradientText>
        </motion.h1>

        {/* Subheading */}
        <motion.p
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-lg text-[var(--color-text-muted)] max-w-2xl mx-auto leading-relaxed"
        >
          Stop switching between LinkedIn, email, spreadsheets and HRMS.
          TalentFlow AI aggregates every candidate source and finds your best hires in seconds.
        </motion.p>

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="flex items-center justify-center gap-4"
        >
          <ShimmerButton className="h-12 px-8 text-base rounded-[var(--radius-lg)]">
            Get Started Free →
          </ShimmerButton>
          <button className="h-12 px-8 text-base rounded-[var(--radius-lg)] border border-[var(--color-border)] text-[var(--color-text)] hover:border-violet-300 transition-colors flex items-center gap-2">
            ▶ Watch Demo <span className="text-sm text-[var(--color-text-muted)]">2:30</span>
          </button>
        </motion.div>

        {/* Social proof */}
        <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.6 }}
          className="text-sm text-[var(--color-text-muted)]">
          Trusted by <strong>120+</strong> companies including Swiggy, Razorpay, CRED
        </motion.p>

        {/* Product mockup */}
        <motion.div
          initial={{ opacity: 0, y: 30, rotateX: 10 }}
          animate={{ opacity: 1, y: 0, rotateX: 4 }}
          transition={{ delay: 0.5, duration: 0.8, ease: 'easeOut' }}
          style={{ perspective: '1200px' }}
          className="mt-8 rounded-[var(--radius-xl)] border border-[var(--color-border)] shadow-[0_40px_80px_rgba(108,99,255,0.15)] overflow-hidden"
        >
          {/* Mini dashboard mockup */}
          <div className="bg-[var(--color-surface)] p-6">
            <div className="grid grid-cols-4 gap-3 mb-4">
              {['1,284 Candidates', '47 Pending', '89 Shortlisted', '6 Open Roles'].map((s, i) => (
                <div key={i} className="rounded-[var(--radius-md)] border border-[var(--color-border)] p-3">
                  <p className="text-xs text-[var(--color-text-muted)]">{s.split(' ').slice(1).join(' ')}</p>
                  <p className="text-xl font-bold text-[var(--color-text)]">{s.split(' ')[0]}</p>
                </div>
              ))}
            </div>
            <div className="rounded-[var(--radius-md)] border border-[var(--color-border)] p-3 flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-violet-400 animate-pulse" />
              <p className="text-sm text-[var(--color-text-muted)]">AI parsed 5 resumes from batch upload — 8 min ago</p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
```

---

### SECTION 3: STATS STRIP
**21st.dev inspiration: number ticker + clean stat row**

```tsx
import { NumberTicker } from '@/components/ui/number-ticker'
import { useInView } from 'framer-motion'
import { useRef } from 'react'

function StatsStrip() {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true })

  const stats = [
    { value: 10, suffix: 'x', label: 'Faster Sourcing' },
    { value: 2,  suffix: 's', label: 'Search Speed' },
    { value: 3,  suffix: '-layer', label: 'Dedup Engine' },
    { value: 100, suffix: '%', label: 'Async Parsing' },
  ]

  return (
    <section ref={ref} className="border-y border-[var(--color-border)] bg-[var(--color-surface-2)] py-12">
      <div className="max-w-5xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8">
        {stats.map((s, i) => (
          <div key={i} className="text-center">
            <div className="text-4xl font-bold text-[var(--color-text)] flex items-center justify-center gap-0.5">
              {inView && <NumberTicker value={s.value} />}
              <span>{s.suffix}</span>
            </div>
            <p className="text-sm text-[var(--color-text-muted)] mt-1">{s.label}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
```

---

### SECTION 4: FEATURES — Bento Grid
**21st.dev inspiration: Feature sections, Bento Grid from Magic UI**

```tsx
import { BentoGrid, BentoCard } from '@/components/ui/bento-grid'   // Magic UI

function FeaturesSection() {
  return (
    <section id="features" className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-[var(--color-text)]">Everything you need to hire smarter</h2>
          <p className="text-[var(--color-text-muted)] mt-3 max-w-xl mx-auto">
            One platform. Five sources. Zero duplicate records. Infinite insights.
          </p>
        </div>

        <BentoGrid className="grid-cols-3 grid-rows-2">
          {/* Feature 1 — large */}
          <BentoCard className="col-span-2 row-span-1 bg-gradient-to-br from-violet-50 to-purple-50 dark:from-violet-950/20 dark:to-purple-950/20 border border-violet-100 dark:border-violet-900/40 p-8">
            <h3 className="text-xl font-bold mb-2">AI Natural Language Search</h3>
            <p className="text-[var(--color-text-muted)] text-sm mb-4">
              "Senior React engineers in Pune open to remote." Results in under 2 seconds.
            </p>
            {/* Animated search bar preview */}
            <div className="rounded-[var(--radius-lg)] border border-violet-200 bg-white dark:bg-[#1A1A2E] p-3 flex items-center gap-2 text-sm text-[var(--color-text-muted)]">
              <span className="text-violet-500">✦</span>
              Find senior Python engineers in Bangalore...
            </div>
          </BentoCard>

          {/* Feature 2 */}
          <BentoCard className="col-span-1 row-span-1 bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950/20 dark:to-orange-950/20 border border-amber-100 dark:border-amber-900/40 p-8">
            <h3 className="text-xl font-bold mb-2">Smart 3-Layer Dedup</h3>
            <p className="text-[var(--color-text-muted)] text-sm">
              Email exact match → Fuzzy name → 0.92 cosine similarity. One candidate, always.
            </p>
          </BentoCard>

          {/* Feature 3 */}
          <BentoCard className="col-span-1 row-span-1 bg-gradient-to-br from-teal-50 to-cyan-50 dark:from-teal-950/20 dark:to-cyan-950/20 border border-teal-100 dark:border-teal-900/40 p-8">
            <h3 className="text-xl font-bold mb-2">5 Candidate Sources</h3>
            <div className="flex flex-wrap gap-2 mt-3">
              {[['Email','#3B82F6'],['Upload','#6C63FF'],['LinkedIn','#0A66C2'],['Referral','#F97316'],['HRMS','#059669']].map(([label, color]) => (
                <span key={label} className="inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium" style={{ borderColor: `${color}40`, color }}>
                  <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: color }} />
                  {label}
                </span>
              ))}
            </div>
          </BentoCard>

          {/* Feature 4 — large */}
          <BentoCard className="col-span-2 row-span-1 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20 border border-blue-100 dark:border-blue-900/40 p-8">
            <h3 className="text-xl font-bold mb-2">Drag-and-Drop Pipeline Kanban</h3>
            <p className="text-[var(--color-text-muted)] text-sm mb-4">
              Applied → Screening → Interview → Offer → Hired. Bulk actions. Stage timers.
            </p>
            {/* Mini kanban preview */}
            <div className="flex gap-2">
              {['Applied 24', 'Screening 8', 'Interview 3', 'Offer 1'].map((col, i) => (
                <div key={i} className="flex-1 rounded-[var(--radius-md)] bg-white dark:bg-[#1A1A2E] border border-[var(--color-border)] p-2">
                  <p className="text-xs font-semibold text-[var(--color-text)]">{col}</p>
                  {Array.from({ length: Math.min(i === 0 ? 3 : i === 1 ? 2 : 1, 3) }).map((_, j) => (
                    <div key={j} className="mt-1.5 h-6 rounded bg-gray-100 dark:bg-gray-800" />
                  ))}
                </div>
              ))}
            </div>
          </BentoCard>
        </BentoGrid>
      </div>
    </section>
  )
}
```

---

### SECTION 5: WHY THIS MATCH SPOTLIGHT

```tsx
function MatchSpotlightSection() {
  return (
    <section className="py-24 px-6 bg-[var(--color-surface-2)]">
      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <div>
          <span className="text-sm font-semibold text-violet-600 uppercase tracking-wider">Hero Innovation Feature</span>
          <h2 className="text-4xl font-bold text-[var(--color-text)] mt-3 mb-4">
            "Why this match?" — in 3 seconds
          </h2>
          <p className="text-[var(--color-text-muted)] leading-relaxed mb-6">
            Every search result comes with a full AI-powered breakdown. Skills matched, gaps identified,
            experience delta, location match, and a 2-sentence human-readable summary.
            No black box. Total transparency.
          </p>
          <ul className="space-y-2 text-sm">
            {['Pre-computed — zero additional latency', 'Matched and missing skills clearly shown', 'AI summary generated by Claude Haiku', 'Popover stays in context — no page navigation'].map(item => (
              <li key={item} className="flex items-center gap-2 text-[var(--color-text)]">
                <span className="w-5 h-5 rounded-full bg-teal-100 dark:bg-teal-950/30 text-teal-600 flex items-center justify-center text-xs">✓</span>
                {item}
              </li>
            ))}
          </ul>
        </div>

        {/* Animated popover mockup */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 8 }}
          whileInView={{ opacity: 1, scale: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="rounded-[var(--radius-xl)] border border-[var(--color-border)] bg-[var(--color-surface)] shadow-[var(--shadow-panel)] overflow-hidden"
        >
          <div className="p-5 border-b border-[var(--color-border)] bg-gradient-to-r from-violet-50 to-teal-50 dark:from-violet-950/20 dark:to-teal-950/20 flex items-center gap-4">
            <div className="text-4xl font-bold text-teal-500">87<span className="text-base text-[var(--color-text-muted)] font-normal">/100</span></div>
            <div>
              <p className="font-bold text-[var(--color-text)]">Strong Match</p>
              <p className="text-xs text-[var(--color-text-muted)]">Rahul Sharma · Senior Backend Engineer</p>
            </div>
          </div>
          <div className="p-5 space-y-4 text-sm">
            <div>
              <p className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-2">Skills</p>
              <div className="flex flex-wrap gap-1.5">
                {['Python ✓', 'AWS ✓', 'FastAPI ✓'].map(s => <span key={s} className="rounded-full bg-teal-100 text-teal-700 px-2.5 py-1 text-xs">{s}</span>)}
                {['React ✗'].map(s => <span key={s} className="rounded-full bg-gray-100 text-gray-400 line-through px-2.5 py-1 text-xs">{s}</span>)}
              </div>
            </div>
            <div><p className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Experience</p><p>Senior (6 yrs) · <span className="text-teal-600 text-xs">+1yr above requirement</span></p></div>
            <div><p className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-1">Location</p><p>📍 Bengaluru · <span className="text-teal-600 text-xs">100% match</span></p></div>
            <div className="rounded-[var(--radius-md)] bg-violet-50 dark:bg-violet-950/20 p-3 text-xs italic text-[var(--color-text-muted)]">
              "Strong backend profile with production AWS experience. Missing React but has Angular — transferable frontend exposure."
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
```

---

### SECTION 6: TESTIMONIALS (Marquee)

```tsx
function TestimonialsSection() {
  const testimonials = [
    { name: 'Priya M.', title: 'Head of Talent, Swiggy', quote: 'We went from 3 days to shortlist to 3 hours. TalentFlow AI is not a nice-to-have anymore.', stars: 5 },
    { name: 'Arjun K.', title: 'Engineering Manager, Razorpay', quote: 'The "Why this match?" feature alone saved my team 10 hours a week of CV screening.', stars: 5 },
    { name: 'Neha S.', title: 'HR Director, Meesho', quote: 'Finally, no more duplicate candidates. The deduplication engine is scary good.', stars: 5 },
    { name: 'Rohan T.', title: 'Talent Lead, CRED', quote: 'Semantic search is a game changer. I can finally describe what I want in plain English.', stars: 5 },
    { name: 'Divya P.', title: 'Recruiter, PhonePe', quote: 'The Gmail sync pulled in 40 resumes automatically. I didn\'t have to touch a single CSV.', stars: 5 },
  ]

  return (
    <section className="py-24 overflow-hidden">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-[var(--color-text)]">Recruiters love it</h2>
      </div>
      {/* Marquee container */}
      <div className="relative">
        <div className="flex gap-6 animate-marquee w-max">
          {/* Double the items for seamless loop */}
          {[...testimonials, ...testimonials].map((t, i) => (
            <div key={i} className="w-80 shrink-0 rounded-[var(--radius-xl)] border border-[var(--color-border)] bg-[var(--color-surface)] p-6 shadow-[var(--shadow-card)]">
              <div className="flex gap-0.5 mb-3">
                {'★'.repeat(t.stars).split('').map((s, j) => <span key={j} className="text-amber-400 text-sm">{s}</span>)}
              </div>
              <p className="text-sm text-[var(--color-text)] leading-relaxed mb-4">"{t.quote}"</p>
              <div>
                <p className="text-sm font-semibold text-[var(--color-text)]">{t.name}</p>
                <p className="text-xs text-[var(--color-text-muted)]">{t.title}</p>
              </div>
            </div>
          ))}
        </div>
        {/* Fade edges */}
        <div className="absolute inset-y-0 left-0 w-24 bg-gradient-to-r from-[var(--color-bg)] to-transparent pointer-events-none" />
        <div className="absolute inset-y-0 right-0 w-24 bg-gradient-to-l from-[var(--color-bg)] to-transparent pointer-events-none" />
      </div>
    </section>
  )
}
```

---

### SECTION 7: CTA SECTION

```tsx
function CTASection() {
  return (
    <section className="py-24 px-6">
      <div className="max-w-4xl mx-auto relative rounded-[var(--radius-xl)] overflow-hidden p-16 text-center"
        style={{ background: 'linear-gradient(135deg, #1A1A2E 0%, #2D1B69 100%)' }}>
        {/* Glow orbs */}
        <div className="absolute top-0 right-0 w-72 h-72 bg-violet-500/20 rounded-full blur-[80px] pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-56 h-56 bg-teal-500/20 rounded-full blur-[80px] pointer-events-none" />

        <div className="relative">
          <h2 className="text-4xl font-bold text-white mb-4">Ready to hire smarter?</h2>
          <p className="text-violet-300 mb-8 text-lg">Start parsing resumes in 60 seconds. No credit card required.</p>
          <div className="flex items-center justify-center gap-4">
            <ShimmerButton className="h-12 px-8 text-base bg-teal-500 hover:bg-teal-600">
              Start Free Trial
            </ShimmerButton>
            <button className="h-12 px-8 text-base rounded-[var(--radius-lg)] border border-white/20 text-white hover:bg-white/10 transition-colors">
              Schedule a Demo →
            </button>
          </div>
        </div>
      </div>
    </section>
  )
}
```

---

### SECTION 8: FOOTER

```tsx
function Footer() {
  return (
    <footer className="bg-[#0D0D1A] text-gray-400 py-16 px-6">
      <div className="max-w-6xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-violet-500 to-teal-400" />
            <span className="font-bold text-white text-sm">TalentFlow AI</span>
          </div>
          <p className="text-xs leading-relaxed">AI-powered hiring for modern recruitment teams.</p>
        </div>
        {[
          { title: 'Product', links: ['Features', 'Pricing', 'Docs', 'API', 'Changelog'] },
          { title: 'Company', links: ['About', 'Blog', 'Careers', 'Privacy', 'Terms'] },
          { title: 'Connect', links: ['Twitter/X', 'LinkedIn', 'GitHub'] },
        ].map(col => (
          <div key={col.title}>
            <h4 className="text-white font-semibold text-sm mb-4">{col.title}</h4>
            <ul className="space-y-2">
              {col.links.map(link => (
                <li key={link}><a href="#" className="text-xs hover:text-white transition-colors">{link}</a></li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="border-t border-gray-800 pt-6 flex items-center justify-between text-xs">
        <span>© 2026 TalentFlow AI · Built for Breach 2026 Hackathon</span>
        <span className="text-gray-600">Powered by Claude Haiku + Pinecone</span>
      </div>
    </footer>
  )
}
```

---

### COMPLETE LANDING PAGE EXPORT

```tsx
// app/(marketing)/page.tsx
import { MarketingNav } from './components/MarketingNav'
import HeroSection from './components/HeroSection'
import StatsStrip from './components/StatsStrip'
import FeaturesSection from './components/FeaturesSection'
import MatchSpotlightSection from './components/MatchSpotlightSection'
import TestimonialsSection from './components/TestimonialsSection'
import CTASection from './components/CTASection'
import Footer from './components/Footer'

export default function LandingPage() {
  return (
    <main className="bg-[var(--color-bg)]">
      <MarketingNav />
      <HeroSection />
      <StatsStrip />
      <FeaturesSection />
      <MatchSpotlightSection />
      <TestimonialsSection />
      <CTASection />
      <Footer />
    </main>
  )
}
```

---

## MICRO-INTERACTIONS MASTER TABLE

Implement ALL of these. No exceptions.

| Element | Trigger | Animation spec | Duration |
|---|---|---|---|
| Candidate card | hover | `translateY(-3px)` + shadow-hover | 200ms ease |
| Candidate card | click | `scale(0.98)` tap | 100ms spring |
| AI Score gauge | mount | arc sweeps from 0 to score | 800ms ease-out |
| Number ticker (dashboard) | scroll into view | counts 0→value | 600ms ease-out |
| Search bar | focus | border violet + outer glow | 200ms ease |
| Skill chip | hover | `scale(1.05)` + tooltip | 150ms ease |
| Upload zone | drag-over | border teal + bg tint + `scale(1.01)` | 150ms spring |
| File drop | drop | ripple confirmation | 300ms |
| Kanban card | drag start | `scale(1.03)` + `rotate(3deg)` + shadow | 200ms spring |
| Kanban card | drop | snap to column + green border flash 400ms | 300ms spring |
| Stage change | move | card slides to new column | 400ms spring |
| Skeleton→card | parse complete | fade out skeleton, fade in card + green border flash | 300ms |
| Sheet panel | open | `x: 560→0` spring | 300ms spring |
| Command palette | open | `scale(0.96→1)` + opacity + backdrop blur | 150ms ease |
| Bulk action bar | appear | `y: 24→0` + opacity | 300ms spring |
| Status dot (connected) | always | pulse loop | 2s infinite |
| Button | click | `scale(0.97)` | 100ms spring |
| Nav active item | route change | left border slides in | 200ms ease |
| Marketing hero mockup | scroll-in | `rotateX(10→4deg)` + `y(30→0)` | 800ms ease-out |
| Stats numbers | scroll-in | NumberTicker runs | 600ms ease-out |
| Testimonial cards | continuous | CSS marquee `translateX` | 30s linear infinite |

---

## FINAL QA CHECKLIST — Run Before Submission

### Critical (Build-breaking)
- [ ] `Topbar.tsx` exists and renders breadcrumb + theme toggle + notifications + avatar
- [ ] `settings/page.tsx` exists — no 404 from Sidebar Settings link
- [ ] `tailwind.config.ts` uses ESM `import animate from 'tailwindcss-animate'` (not require)
- [ ] `content` paths include `./app/**` and `./components/**`
- [ ] `SidebarProvider` exists at `components/ui/sidebar-provider.tsx`
- [ ] SSE `useEffect` has cleanup: `return () => es.close()`
- [ ] `localStorage` access guarded: `if (typeof window !== 'undefined')`
- [ ] `cand-007` exists in mock data (referenced by cand-003 merge)
- [ ] All icon imports explicit from `lucide-react`
- [ ] `ThemeToggle` uses `useTheme()` from `next-themes`

### Functional
- [ ] Compare page handles no candidates selected (empty state)
- [ ] Upload triggers from ⌘K via `CustomEvent('talentflow:open-upload')`
- [ ] Source badges show amber "Simulated" tag when `source.simulated === true`
- [ ] `NumberTicker` receives `number` type (not string)
- [ ] AI Score gauge circumference uses `2 * Math.PI * r` (not hardcoded 126)
- [ ] Card animation delay capped: `Math.min(index * 0.04, 0.3)` — not unbounded
- [ ] `ActivityFeed` has `aria-live="polite"` on container
- [ ] Parse progress bar has `role="progressbar"` with aria values
- [ ] Demo mode: `NEXT_PUBLIC_DEMO_MODE=true` triggers local simulation

### Polish
- [ ] Dark mode tested on every page (all colors use CSS vars or Tailwind bridge)
- [ ] Mobile responsive: Sidebar collapses to icon rail on sm, grid goes 1-col
- [ ] Focus rings visible (2px violet) — never `outline: none` without replacement
- [ ] All modals/sheets return focus to trigger element on close
- [ ] Command palette closes on `Escape` key
- [ ] Skeleton loaders: `aria-busy="true"` and `aria-label="Loading candidate"`

### Demo Readiness
- [ ] 7 mock candidates seeded (including cand-007)
- [ ] 2 merge pairs exist (cand-003 ↔ cand-007)
- [ ] 3 skeleton → card transitions work with green border flash
- [ ] Pipeline Kanban drag-and-drop works with spring animation
- [ ] "Why this match?" popover opens on every candidate card
- [ ] Compare page works at `/compare?a=cand-001&b=cand-002`
- [ ] LinkedIn candidates show amber "Simulated" badge
- [ ] `NEXT_PUBLIC_DEMO_MODE=true` set in `.env.local` for demo day

---

*End of File 05 — TalentFlow AI Master CLI Prompt (Split Version)*
*Feed files 01→05 in sequence to your CLI agent.*
*Each file is self-contained and ~2,000–3,000 tokens — well within context window.*
