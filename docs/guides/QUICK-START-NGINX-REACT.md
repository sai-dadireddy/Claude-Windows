# NGINX → React Quick Start Card

**Project**: `claude/projects/nginx-to-react-migration/`
**Status**: ✅ Ready for Implementation

---

## 📖 Read These First (In Order)

1. **`PROJECT-SETUP-COMPLETE.md`** ← Start here! (This folder)
2. **`claude/projects/nginx-to-react-migration/GETTING_STARTED.md`**
3. **`claude/projects/nginx-to-react-migration/docs/RECOMMENDATIONS.md`** ⭐

---

## 🚀 Fastest Path to Start

```bash
# 1. Navigate to project
cd claude/projects/nginx-to-react-migration

# 2. Create React app
npm create vite@latest . -- --template react-ts
npm install

# 3. Install Tailwind + shadcn
npx shadcn@latest init

# 4. Install core deps
npm install zustand @tanstack/react-query react-router-dom react-hook-form zod

# 5. Install dev tools
npm install -D eslint eslint-plugin-security prettier husky vitest @testing-library/react

# 6. Start dev server
npm run dev
```

---

## 🎨 Claude Code Commands

```bash
# Switch to project
/project nginx-to-react-migration

# Migrate a component
/migrate-component <ComponentName>

# Visual validation
/design-review <ComponentName> <legacy-url>

# Security audit
/security-check
```

---

## 🤖 Multi-AI Orchestrator

```bash
cd tools
python auto-multi-ai-orchestrator.py \
  --task "Your question" \
  --validate \
  --research \
  --google-api-key "$GOOGLE_API_KEY"
```

**Use for**: Architecture decisions, security audits, performance reviews
**Don't use for**: Component implementations, bug fixes

---

## ✅ Tech Stack (Approved by Codex GPT-5)

- React 18.3+ + TypeScript 5.3+
- Vite 5.x (build tool)
- Tailwind CSS + shadcn/ui
- Zustand (state)
- TanStack Query (data fetching)
- React Router v6
- Vitest + Playwright

---

## 🎯 Migration Strategy

**Incremental (Strangler Pattern)**:
- NGINX reverse proxy routes traffic
- Migrate one route at a time
- Feature flags for gradual rollout
- Easy rollback per route

❌ NOT big bang migration!

---

## 🔒 Security Must-Haves

- httpOnly cookies (NOT localStorage!)
- CSP headers at NGINX
- Input sanitization (DOMPurify)
- npm audit + Snyk
- Strip source maps in production

---

## 📊 Success Metrics

- Lighthouse score > 90
- < 3s initial load
- 80%+ test coverage
- Zero console errors

---

## 🎓 Key Documents

All in `claude/projects/nginx-to-react-migration/`:

- `GETTING_STARTED.md` - Step-by-step guide
- `README.md` - Project overview
- `docs/RECOMMENDATIONS.md` - Complete Codex + research
- `docs/ARCHITECTURE_PLAN.md` - Original proposal

---

## ❓ Questions?

1. Read `GETTING_STARTED.md` FAQ section
2. Use `/security-check` or `/design-review` commands
3. Run multi-AI orchestrator for complex decisions

---

**Ready? Start with `GETTING_STARTED.md`!** 🚀
