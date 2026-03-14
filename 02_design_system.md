# TALENTFLOW AI — DESIGN SYSTEM & LAYOUT SHELL
## File 02 of 05 — Feed after 01_system_prompt.md

---

## 1. globals.css

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300..800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --color-navy:         #1A1A2E;
  --color-violet:       #6C63FF;
  --color-teal:         #00D4AA;
  --color-coral:        #FF6B6B;
  --color-amber:        #F59E0B;
  --color-orange:       #F97316;
  --color-bg:           #FAFAFA;
  --color-surface:      #FFFFFF;
  --color-surface-2:    #F5F5F7;
  --color-border:       #E5E7EB;
  --color-text:         #1E1E2E;
  --color-text-muted:   #6B7280;
  --color-score-high:   #00D4AA;
  --color-score-mid:    #F59E0B;
  --color-score-low:    #FF6B6B;
  --source-email:       #3B82F6;
  --source-upload:      #6C63FF;
  --source-linkedin:    #0A66C2;
  --source-referral:    #F97316;
  --source-hrms:        #059669;
  --shadow-card:        0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(108,99,255,0.04);
  --shadow-hover:       0 4px 16px rgba(108,99,255,0.12), 0 1px 4px rgba(0,0,0,0.08);
  --shadow-panel:       0 20px 60px rgba(0,0,0,0.15);
  --radius-sm:   6px;
  --radius-md:   10px;
  --radius-lg:   14px;
  --radius-xl:   20px;
  --radius-full: 9999px;
}

.dark {
  --color-bg:          #0D0D1A;
  --color-surface:     #1A1A2E;
  --color-surface-2:   #1E1E32;
  --color-border:      #2D2D4A;
  --color-text:        #F0F0FF;
  --color-text-muted:  #8B8BA8;
}

@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}
@keyframes pulse-teal {
  0%, 100% { box-shadow: 0 0 0 0 rgba(0,212,170,0.4); }
  50%       { box-shadow: 0 0 0 6px rgba(0,212,170,0); }
}
@keyframes marquee {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0f0 50%, #f0f0f0 75%);
  background-size: 200%;
  animation: shimmer 1.5s infinite;
}
.dark .skeleton {
  background: linear-gradient(90deg, #1e1e2e 25%, #2d2d4a 50%, #1e1e2e 75%);
  background-size: 200%;
}
```

---

## 2. tailwind.config.ts (CORRECTED — ESM, correct content paths)

```ts
import type { Config } from 'tailwindcss'
import animate from 'tailwindcss-animate'   // ESM import — NOT require()

const config: Config = {
  darkMode: ['class'],
  content: [
    './app/**/*.{ts,tsx}',          // Next.js App Router
    './components/**/*.{ts,tsx}',   // Shared components
    './src/**/*.{ts,tsx}',          // Fallback for any /src usage
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'monospace'],
      },
      colors: {
        navy:   '#1A1A2E',
        violet: { DEFAULT: '#6C63FF', light: '#8B84FF', dark: '#5B52E8' },
        teal:   { DEFAULT: '#00D4AA', light: '#1ADDB4', dark: '#00B893' },
        coral:  { DEFAULT: '#FF6B6B', light: '#FF8585', dark: '#E85555' },
        // CSS variable bridge — allows bg-surface, text-muted etc in Tailwind
        surface:       'var(--color-surface)',
        'surface-2':   'var(--color-surface-2)',
        border:        'var(--color-border)',
        foreground:    'var(--color-text)',
        muted:         'var(--color-text-muted)',
      },
      animation: {
        shimmer:      'shimmer 1.5s infinite',
        'pulse-teal': 'pulse-teal 2s infinite',
        marquee:      'marquee 30s linear infinite',
      },
    },
  },
  plugins: [animate],   // ESM — not require()
}
export default config
```

**NOTE**: Use `bg-[var(--color-surface)]` when Tailwind bridge colors aren't available (e.g., in arbitrary values). Do NOT use bare `bg-surface` unless you've confirmed the color bridge above is active.

---

## 3. lib/motion.config.ts

```ts
export const transitions = {
  instant:    { duration: 0.1, ease: 'easeOut' },
  fast:       { duration: 0.2, ease: 'easeOut' },
  base:       { duration: 0.3, ease: 'easeOut' },
  slow:       { duration: 0.5, ease: 'easeOut' },
  spring:     { type: 'spring' as const, stiffness: 400, damping: 30 },
  springSlow: { type: 'spring' as const, stiffness: 200, damping: 25 },
}

export const variants = {
  fadeIn:  { hidden: { opacity: 0 },               visible: { opacity: 1 } },
  slideUp: { hidden: { opacity: 0, y: 12 },         visible: { opacity: 1, y: 0 } },
  slideIn: { hidden: { opacity: 0, x: 24 },         visible: { opacity: 1, x: 0 } },
  scaleIn: { hidden: { opacity: 0, scale: 0.95 },   visible: { opacity: 1, scale: 1 } },
  stagger: { visible: { transition: { staggerChildren: 0.05 } } },
}
```

---

## 4. lib/api.ts (CORRECTED — SSR-safe localStorage access)

```ts
import axios from 'axios'

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

// SSR-safe: localStorage is browser-only — guard with typeof window check
api.interceptors.request.use(config => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token')
    if (token) config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

---

## 5. App Layout Shell — `app/(app)/layout.tsx`

```tsx
'use client'
import { SidebarProvider } from '@/components/ui/sidebar-provider'
import { ThemeProvider } from 'next-themes'
import AppSidebar from '@/components/layout/Sidebar'
import Topbar from '@/components/layout/Topbar'
import CommandPalette from '@/components/layout/CommandPalette'

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem disableTransitionOnChange>
      <SidebarProvider>
        <div className="flex h-screen overflow-hidden bg-[var(--color-bg)]">
          <AppSidebar />
          <div className="flex flex-col flex-1 overflow-hidden">
            <Topbar />
            <main className="flex-1 overflow-y-auto p-6">
              <div className="max-w-7xl mx-auto w-full">
                {children}
              </div>
            </main>
          </div>
        </div>
        <CommandPalette />
      </SidebarProvider>
    </ThemeProvider>
  )
}
```

---

## 6. components/ui/sidebar-provider.tsx (REQUIRED — shadcn doesn't ship this)

```tsx
'use client'
import { createContext, useContext, useState } from 'react'

interface SidebarContextType {
  collapsed: boolean
  setCollapsed: (v: boolean) => void
  toggle: () => void
}

const SidebarContext = createContext<SidebarContextType>({
  collapsed: false,
  setCollapsed: () => {},
  toggle: () => {},
})

export function SidebarProvider({ children }: { children: React.ReactNode }) {
  const [collapsed, setCollapsed] = useState(false)
  const toggle = () => setCollapsed(prev => !prev)
  return (
    <SidebarContext.Provider value={{ collapsed, setCollapsed, toggle }}>
      {children}
    </SidebarContext.Provider>
  )
}

export const useSidebar = () => useContext(SidebarContext)
```

---

## 7. components/layout/Sidebar.tsx

```tsx
'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import {
  LayoutDashboard, Search, Kanban, GitCompare,
  Plug, Settings, ChevronLeft, ChevronRight
} from 'lucide-react'
import { useSidebar } from '@/components/ui/sidebar-provider'
import { cn } from '@/lib/utils'
import {
  Tooltip, TooltipContent, TooltipProvider, TooltipTrigger
} from '@/components/ui/tooltip'

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard',    href: '/dashboard' },
  { icon: Search,          label: 'Search',       href: '/search' },
  { icon: Kanban,          label: 'Pipeline',     href: '/pipeline' },
  { icon: GitCompare,      label: 'Compare',      href: '/compare' },    // ADDED — was missing
  { icon: Plug,            label: 'Integrations', href: '/integrations' },
  { icon: Settings,        label: 'Settings',     href: '/settings' },
]

export default function AppSidebar() {
  const pathname = usePathname()
  const { collapsed, toggle } = useSidebar()

  return (
    <TooltipProvider delayDuration={0}>
      <aside
        className={cn(
          'relative flex flex-col h-screen border-r border-[var(--color-border)]',
          'bg-[var(--color-surface)] transition-all duration-300',
          collapsed ? 'w-14' : 'w-60'
        )}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-4 h-16 border-b border-[var(--color-border)]">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-violet-500 to-teal-400 shrink-0" />
          <AnimatePresence>
            {!collapsed && (
              <motion.span
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -8 }}
                className="font-bold text-sm text-[var(--color-text)] whitespace-nowrap"
              >
                TalentFlow AI
              </motion.span>
            )}
          </AnimatePresence>
        </div>

        {/* Nav */}
        <nav className="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
          {navItems.map(({ icon: Icon, label, href }) => {
            const active = pathname === href || pathname.startsWith(href + '/')
            const item = (
              <Link
                key={href}
                href={href}
                className={cn(
                  'flex items-center gap-3 rounded-[var(--radius-md)] px-3 py-2.5',
                  'text-sm transition-all duration-150',
                  active
                    ? 'bg-violet-50 dark:bg-violet-950/30 text-violet-700 font-semibold border-l-[3px] border-violet-600 pl-[calc(0.75rem-3px)]'
                    : 'text-[var(--color-text-muted)] hover:bg-gray-100 dark:hover:bg-white/5 hover:text-[var(--color-text)]'
                )}
              >
                <Icon size={18} className="shrink-0" />
                <AnimatePresence>
                  {!collapsed && (
                    <motion.span
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                    >
                      {label}
                    </motion.span>
                  )}
                </AnimatePresence>
              </Link>
            )

            return collapsed ? (
              <Tooltip key={href}>
                <TooltipTrigger asChild>{item}</TooltipTrigger>
                <TooltipContent side="right">{label}</TooltipContent>
              </Tooltip>
            ) : item
          })}
        </nav>

        {/* ⌘K hint */}
        {!collapsed && (
          <div className="px-4 pb-3">
            <span className="inline-flex items-center gap-1.5 text-xs text-[var(--color-text-muted)]">
              <kbd className="rounded border border-[var(--color-border)] px-1.5 py-0.5 font-mono text-[10px]">⌘K</kbd>
              Quick actions
            </span>
          </div>
        )}

        {/* User footer */}
        <div className="p-3 border-t border-[var(--color-border)]">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-teal-400 flex items-center justify-center text-white text-xs font-bold shrink-0">
              P
            </div>
            {!collapsed && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-[var(--color-text)] truncate">Priya Sharma</p>
                <p className="text-xs text-[var(--color-text-muted)]">Head of Talent</p>
              </div>
            )}
          </div>
        </div>

        {/* Collapse toggle */}
        <button
          onClick={toggle}
          className="absolute -right-3 top-20 w-6 h-6 rounded-full border border-[var(--color-border)] bg-[var(--color-surface)] flex items-center justify-center shadow-sm hover:border-violet-300 transition-colors"
        >
          {collapsed ? <ChevronRight size={12} /> : <ChevronLeft size={12} />}
        </button>
      </aside>
    </TooltipProvider>
  )
}
```

---

## 8. components/layout/Topbar.tsx (PREVIOUSLY MISSING — now fully defined)

```tsx
'use client'
import { Bell, Sun, Moon, Monitor, ChevronRight } from 'lucide-react'
import { useTheme } from 'next-themes'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem,
  DropdownMenuSeparator, DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'

// Breadcrumb map — extend as routes are added
const BREADCRUMB_MAP: Record<string, string[]> = {
  '/dashboard':     ['Dashboard'],
  '/search':        ['Candidates', 'Search'],
  '/pipeline':      ['Candidates', 'Pipeline'],
  '/compare':       ['Candidates', 'Compare'],
  '/integrations':  ['Integrations'],
  '/settings':      ['Settings'],
}

function ThemeToggle() {
  const { theme, setTheme } = useTheme()  // next-themes hook — properly implemented

  const options = [
    { value: 'light',  icon: Sun,     label: 'Light' },
    { value: 'dark',   icon: Moon,    label: 'Dark' },
    { value: 'system', icon: Monitor, label: 'System' },
  ]

  const current = options.find(o => o.value === theme) ?? options[2]
  const CurrentIcon = current.icon

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="w-9 h-9">
          <CurrentIcon size={16} />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {options.map(({ value, icon: Icon, label }) => (
          <DropdownMenuItem key={value} onClick={() => setTheme(value)} className="gap-2">
            <Icon size={14} />
            {label}
            {theme === value && <span className="ml-auto text-violet-600">✓</span>}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

export default function Topbar() {
  const pathname = usePathname()

  // Match breadcrumb by longest matching prefix
  const breadcrumb = Object.entries(BREADCRUMB_MAP)
    .filter(([key]) => pathname.startsWith(key))
    .sort((a, b) => b[0].length - a[0].length)[0]?.[1] ?? ['Dashboard']

  return (
    <header className="h-16 flex items-center justify-between px-6 border-b border-[var(--color-border)] bg-[var(--color-surface)] shrink-0">

      {/* Left: Breadcrumb */}
      <nav className="flex items-center gap-1.5 text-sm">
        {breadcrumb.map((crumb, i) => (
          <span key={crumb} className="flex items-center gap-1.5">
            {i > 0 && <ChevronRight size={14} className="text-[var(--color-text-muted)]" />}
            <span className={i === breadcrumb.length - 1
              ? 'font-semibold text-[var(--color-text)]'
              : 'text-[var(--color-text-muted)]'
            }>
              {crumb}
            </span>
          </span>
        ))}
      </nav>

      {/* Center: ⌘K hint */}
      <button
        className="hidden md:flex items-center gap-2 px-4 py-2 rounded-[var(--radius-md)] border border-[var(--color-border)] text-sm text-[var(--color-text-muted)] hover:border-violet-300 transition-colors"
        onClick={() => {
          // Dispatch custom event that CommandPalette listens to
          document.dispatchEvent(new KeyboardEvent('keydown', { key: 'k', metaKey: true }))
        }}
      >
        <span>Search...</span>
        <kbd className="rounded border border-[var(--color-border)] px-1.5 py-0.5 font-mono text-[10px]">⌘K</kbd>
      </button>

      {/* Right: Notifications + Theme + Avatar */}
      <div className="flex items-center gap-2">

        {/* Notification bell */}
        <Button variant="ghost" size="icon" className="w-9 h-9 relative">
          <Bell size={16} />
          {/* Red dot for new notifications */}
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-coral animate-pulse" />
          <span className="sr-only">Notifications</span>
        </Button>

        {/* Theme toggle — properly wired to next-themes */}
        <ThemeToggle />

        {/* User avatar dropdown */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" className="w-9 h-9 rounded-full p-0">
              <Avatar className="w-8 h-8">
                <AvatarFallback className="bg-gradient-to-br from-violet-500 to-teal-400 text-white text-xs font-bold">
                  PS
                </AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-52">
            <div className="px-3 py-2">
              <p className="text-sm font-semibold">Priya Sharma</p>
              <p className="text-xs text-[var(--color-text-muted)]">priya@company.com</p>
            </div>
            <DropdownMenuSeparator />
            <DropdownMenuItem>Profile</DropdownMenuItem>
            <DropdownMenuItem>Settings</DropdownMenuItem>
            <DropdownMenuItem>Keyboard shortcuts</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="text-coral">Log out</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  )
}
```

---

## 9. components/layout/CommandPalette.tsx

```tsx
'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useTheme } from 'next-themes'
import { Command } from 'cmdk'
import { AnimatePresence, motion } from 'framer-motion'
import {
  LayoutDashboard, Search, Kanban, GitCompare,
  Plug, Upload, UserPlus, GitMerge, Sun, Moon
} from 'lucide-react'

const COMMANDS = [
  {
    group: 'Navigation',
    items: [
      { icon: LayoutDashboard, label: 'Go to Dashboard',    action: 'navigate', href: '/dashboard' },
      { icon: Search,          label: 'Search Candidates',  action: 'navigate', href: '/search' },
      { icon: Kanban,          label: 'Open Pipeline',      action: 'navigate', href: '/pipeline' },
      { icon: GitCompare,      label: 'Compare Candidates', action: 'navigate', href: '/compare' },  // ADDED
      { icon: Plug,            label: 'Integrations',       action: 'navigate', href: '/integrations' },
    ],
  },
  {
    group: 'Actions',
    items: [
      { icon: Upload,   label: 'Upload Resumes',         action: 'upload'  },
      { icon: UserPlus, label: 'Add Candidate Manually', action: 'add'     },
      { icon: GitMerge, label: 'Review Suggested Merges',action: 'merges'  },
    ],
  },
  {
    group: 'Appearance',
    items: [
      { icon: Sun,  label: 'Toggle Light Mode', action: 'theme', value: 'light' },
      { icon: Moon, label: 'Toggle Dark Mode',  action: 'theme', value: 'dark'  },
    ],
  },
]

export default function CommandPalette() {
  const [open, setOpen] = useState(false)
  const router = useRouter()
  const { setTheme } = useTheme()

  // Listen for ⌘K globally
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setOpen(prev => !prev)
      }
    }
    document.addEventListener('keydown', handler)
    return () => document.removeEventListener('keydown', handler)
  }, [])

  const runCommand = (item: typeof COMMANDS[0]['items'][0]) => {
    setOpen(false)
    if (item.action === 'navigate' && item.href) router.push(item.href)
    if (item.action === 'theme' && item.value) setTheme(item.value)
    if (item.action === 'upload') {
      // Trigger hidden file input via global event
      document.dispatchEvent(new CustomEvent('talentflow:open-upload'))
    }
  }

  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[9998]"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setOpen(false)}
          />

          {/* Dialog */}
          <motion.div
            className="fixed top-[20vh] left-1/2 -translate-x-1/2 z-[9999] w-[min(640px,calc(100vw-32px))]"
            initial={{ opacity: 0, scale: 0.96, y: -8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: -8 }}
            transition={{ duration: 0.15, ease: 'easeOut' }}
          >
            <Command
              className="rounded-[20px] border border-[var(--color-border)] bg-[var(--color-surface)] shadow-[var(--shadow-panel)] overflow-hidden"
            >
              <Command.Input
                placeholder="Search commands or candidates..."
                className="w-full h-14 px-5 text-base bg-transparent border-b border-[var(--color-border)] outline-none placeholder:text-[var(--color-text-muted)]"
              />
              <Command.List className="max-h-[360px] overflow-y-auto p-2">
                <Command.Empty className="py-8 text-center text-sm text-[var(--color-text-muted)]">
                  No results found.
                </Command.Empty>

                {COMMANDS.map(group => (
                  <Command.Group key={group.group} heading={group.group}
                    className="[&>[cmdk-group-heading]]:px-2 [&>[cmdk-group-heading]]:py-1.5 [&>[cmdk-group-heading]]:text-xs [&>[cmdk-group-heading]]:font-semibold [&>[cmdk-group-heading]]:text-[var(--color-text-muted)] [&>[cmdk-group-heading]]:uppercase [&>[cmdk-group-heading]]:tracking-wider"
                  >
                    {group.items.map(item => (
                      <Command.Item
                        key={item.label}
                        onSelect={() => runCommand(item)}
                        className="flex items-center gap-3 px-3 py-2.5 rounded-[8px] cursor-pointer text-sm text-[var(--color-text)] data-[selected=true]:bg-violet-50 dark:data-[selected=true]:bg-violet-950/30 data-[selected=true]:text-violet-700"
                      >
                        <item.icon size={16} className="shrink-0 text-[var(--color-text-muted)]" />
                        {item.label}
                        <kbd className="ml-auto text-[10px] font-mono text-[var(--color-text-muted)] border border-[var(--color-border)] rounded px-1.5 py-0.5">↵</kbd>
                      </Command.Item>
                    ))}
                  </Command.Group>
                ))}
              </Command.List>
            </Command>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

---

## 10. Settings Page Stub — `app/(app)/settings/page.tsx`
(REQUIRED — prevents 404 from Sidebar nav link)

```tsx
export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[var(--color-text)]">Settings</h1>
        <p className="text-sm text-[var(--color-text-muted)] mt-1">
          Manage your account, preferences, and integrations.
        </p>
      </div>

      {/* Placeholder sections */}
      <div className="grid gap-4">
        {['Profile', 'Notifications', 'API Keys', 'Team Members', 'Billing'].map(section => (
          <div
            key={section}
            className="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-6 flex items-center justify-between"
          >
            <div>
              <h3 className="font-semibold text-[var(--color-text)]">{section}</h3>
              <p className="text-sm text-[var(--color-text-muted)] mt-0.5">
                Configure your {section.toLowerCase()} settings
              </p>
            </div>
            <span className="text-[var(--color-text-muted)] text-sm">Coming soon →</span>
          </div>
        ))}
      </div>
    </div>
  )
}
```
