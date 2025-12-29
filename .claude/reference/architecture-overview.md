# Global Architecture & Development Philosophy

**Last Updated:** 2025-12-23

This document defines cross-project architectural principles, technology preferences, and coding standards that Claude should follow when working on any project.

---

## Development Philosophy

### Core Principles

1. **Simplicity Over Cleverness** - Prefer readable, maintainable code over clever abstractions
2. **Explicit Over Implicit** - Make behavior obvious; avoid magic
3. **Composition Over Inheritance** - Build with small, composable pieces
4. **Fail Fast** - Validate early, error clearly
5. **Minimize Dependencies** - Every dependency is a liability

### Code Quality Standards

- **No dead code** - Remove unused functions, imports, variables
- **No commented-out code** - Use git history instead
- **Self-documenting code** - Clear names > comments
- **Small functions** - Single responsibility, < 30 lines preferred
- **Consistent formatting** - Use project's formatter (Prettier, Black, etc.)

---

## Technology Preferences

### Frontend Stack (Preferred Order)

| Category | First Choice | Alternatives |
|----------|--------------|--------------|
| Framework | Next.js (App Router) | React, Vue 3 |
| Styling | Tailwind CSS | CSS Modules |
| Components | shadcn/ui | Radix UI |
| State | React Server Components | Zustand, Jotai |
| Forms | React Hook Form + Zod | Formik |
| API Layer | tRPC | TanStack Query |

### Backend Stack (Preferred Order)

| Category | First Choice | Alternatives |
|----------|--------------|--------------|
| Language | TypeScript (Node) | Python 3.12+ |
| Runtime | Node.js 20+ | Bun |
| API Style | tRPC | REST (OpenAPI) |
| Database | PostgreSQL | SQLite (local dev) |
| ORM | Prisma | Drizzle |
| Auth | Clerk, Auth.js | AWS Cognito |

### AWS Preferences

| Service | When to Use |
|---------|-------------|
| Lambda | Event-driven, < 15min execution |
| ECS Fargate | Long-running, containerized |
| API Gateway V2 | HTTP APIs (cheaper, faster than V1) |
| Aurora Serverless v2 | PostgreSQL with auto-scaling |
| Cognito | When AWS-native auth needed |

---

## Project Structure Patterns

### Monorepo (Preferred for Multi-Package)

```
project/
├── apps/
│   ├── web/           # Next.js frontend
│   └── api/           # Backend service
├── packages/
│   ├── ui/            # Shared components
│   ├── config/        # Shared configs
│   └── types/         # Shared TypeScript types
├── turbo.json
└── package.json
```

### Single App (Next.js)

```
app/
├── (auth)/            # Route groups
├── api/               # API routes (or tRPC)
├── layout.tsx
└── page.tsx
components/
├── ui/                # shadcn/ui components
└── [feature]/         # Feature-specific
lib/
├── db/                # Database client
├── auth/              # Auth utilities
└── utils/             # Helpers
```

### Python Lambda

```
BackEnd/
├── lambdas/
│   └── [function-name]/
│       ├── handler.py
│       ├── requirements.txt
│       └── tests/
├── shared/            # Shared code (layers)
└── infrastructure/    # CDK/SAM/Terraform
```

---

## API Design Principles

### REST (When Used)

- **Nouns for resources** - `/users`, `/orders`
- **HTTP verbs for actions** - GET, POST, PUT, DELETE
- **Consistent error format**:
  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Email is required",
      "details": [...]
    }
  }
  ```
- **Pagination** - cursor-based preferred over offset

### tRPC (Preferred)

- **Flat procedure names** - `user.getById`, `order.create`
- **Zod validation** - Input/output schemas
- **Error handling** - Use `TRPCError` with appropriate codes

---

## Database Patterns

### Schema Design

- **UUIDs for IDs** - Better for distributed systems
- **Timestamps** - Always include `created_at`, `updated_at`
- **Soft deletes** - Use `deleted_at` when data recovery needed
- **Multi-tenant** - Row-Level Security (RLS) when applicable

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Tables | snake_case, plural | `user_accounts` |
| Columns | snake_case | `created_at` |
| Indexes | `idx_table_column` | `idx_users_email` |
| Foreign Keys | `fk_table_ref` | `fk_orders_user` |

---

## Testing Strategy

### Test Pyramid

1. **Unit tests** (70%) - Fast, isolated, mock dependencies
2. **Integration tests** (20%) - Test component interactions
3. **E2E tests** (10%) - Critical user flows only

### Testing Preferences

| Type | Tool |
|------|------|
| Unit (JS/TS) | Vitest |
| Unit (Python) | pytest |
| Integration | Vitest + MSW |
| E2E | Playwright |
| API | Supertest, httpx |

---

## Security Baseline

### Always

- **Validate all inputs** - Zod, Pydantic, etc.
- **Parameterized queries** - Never string concatenation for SQL
- **Secrets in env vars** - Never in code
- **HTTPS everywhere** - No exceptions
- **Auth on all endpoints** - Default deny

### Never

- Storing passwords in plain text
- Exposing stack traces in production
- Trusting client-side validation alone
- Hardcoding credentials or API keys

---

## Git Workflow

### Commit Messages

```
<type>: <short description>

[optional body]

[optional footer]
```

**Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

### Branch Naming

- `feature/short-description`
- `fix/issue-number-description`
- `refactor/what-is-being-refactored`

---

## When to Use Plan Mode

### Use Plan Mode For

- New feature implementation
- Refactoring across multiple files
- Adding/changing dependencies
- Architectural changes
- Database migrations
- Multi-step workflows

### Skip Plan Mode For

- Single-line fixes
- Typo corrections
- Adding logs/comments
- Quick renames
- Content-only changes

---

## Non-Goals (What to Avoid)

- Over-engineering for hypothetical future needs
- Premature optimization
- Adding abstraction layers "just in case"
- Chasing latest tech without clear benefit
- Breaking changes without migration path
