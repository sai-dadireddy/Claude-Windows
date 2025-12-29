# Implementation Decisions - Web Scraper Architecture

**Date:** 2025-10-17
**Status:** ✅ GO - Ready for implementation with noted adjustments
**Decision Authority:** Multi-AI consultation + Architecture review

---

## 1. GO/NO-GO Decision

### ✅ GO - Proceed with Implementation

**Conditions:**
- ✅ Add explicit SQLite concurrency guards (WAL mode)
- ✅ Document all concurrency settings before coding
- ✅ Implement pre-work items (see Critical Changes)

---

## 2. LangGraph Decision

### ❌ NO for MVP - Revisit in Phase 2

**Rationale:**
- Current fallback chain is **deterministic** (WebFetch → Playwright → WebSearch)
- Async primitives (asyncio, FastAPI) are **sufficient** for MVP
- LangGraph would add:
  - Extra dependency overhead
  - Schema translation complexity
  - 3-4 days of ramp-up time
- **No need** for visual introspection or multi-branch workflows yet

**When to revisit:**
- Phase 2+: If we need visual workflow inspection
- If fallback logic becomes non-deterministic
- If we add per-user personalization or branching workflows
- If we need agent-like decision making

**Time saved:** 3-4 days by skipping LangGraph in MVP

---

## 3. Critical Changes (Before Coding)

### Priority 1: SQLite Concurrency (RISK: Medium)

**Problem:** SQLite can lock under concurrent Playwright tasks

**Solution:**
```python
# Enable WAL mode for better concurrency
import sqlite3

def init_db():
    conn = sqlite3.connect('orchestrator.db')

    # CRITICAL: Enable WAL mode
    conn.execute('PRAGMA journal_mode=WAL')

    # CRITICAL: Set busy timeout (30 seconds)
    conn.execute('PRAGMA busy_timeout=30000')

    # Optimize for performance
    conn.execute('PRAGMA synchronous=NORMAL')
    conn.execute('PRAGMA cache_size=-64000')  # 64MB cache
    conn.execute('PRAGMA temp_store=MEMORY')

    return conn
```

**Async DAO Layer:**
```python
import aiosqlite

class AsyncDAO:
    """Thin async wrapper to prevent locked-db failures"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._pool = None

    async def init(self):
        """Initialize connection pool"""
        self._pool = await aiosqlite.connect(
            self.db_path,
            isolation_level=None,  # Autocommit mode
            timeout=30.0
        )

        # Enable WAL mode
        await self._pool.execute('PRAGMA journal_mode=WAL')
        await self._pool.execute('PRAGMA busy_timeout=30000')
        await self._pool.commit()

    async def execute(self, query: str, params: tuple = ()):
        """Thread-safe execute"""
        async with self._pool.execute(query, params) as cursor:
            return await cursor.fetchall()

    async def execute_many(self, query: str, params_list: list):
        """Batch operations"""
        await self._pool.executemany(query, params_list)
        await self._pool.commit()
```

### Priority 2: Shared Rate-Limit Registry (RISK: Medium)

**Problem:** Cache miss bursts can trigger accidental bans

**Solution:**
```python
from collections import defaultdict
from asyncio import Lock
import time

class RateLimitRegistry:
    """Per-domain token bucket rate limiter"""

    def __init__(self):
        self.buckets = defaultdict(lambda: {
            'tokens': 10.0,
            'last_refill': time.time(),
            'lock': Lock()
        })

        # Domain-specific limits (tokens per second)
        self.limits = {
            'medium.com': 2.0,      # 2 req/sec
            'github.com': 5.0,      # 5 req/sec
            'default': 3.0,         # 3 req/sec default
        }

        # Burst limits
        self.burst_sizes = {
            'medium.com': 5,
            'github.com': 10,
            'default': 6,
        }

    async def acquire(self, domain: str):
        """Acquire token, blocks if none available"""
        bucket = self.buckets[domain]
        rate = self.limits.get(domain, self.limits['default'])
        burst = self.burst_sizes.get(domain, self.burst_sizes['default'])

        async with bucket['lock']:
            now = time.time()
            elapsed = now - bucket['last_refill']

            # Refill tokens based on elapsed time
            bucket['tokens'] = min(
                burst,
                bucket['tokens'] + (elapsed * rate)
            )
            bucket['last_refill'] = now

            # Wait if no tokens available
            while bucket['tokens'] < 1.0:
                await asyncio.sleep(0.1)
                now = time.time()
                elapsed = now - bucket['last_refill']
                bucket['tokens'] = min(
                    burst,
                    bucket['tokens'] + (elapsed * rate)
                )
                bucket['last_refill'] = now

            # Consume token
            bucket['tokens'] -= 1.0
```

### Priority 3: Circuit Breaker Persistence (RISK: Low)

**Problem:** In-memory state vanishes on restart

**Solution:**
```sql
CREATE TABLE circuit_breakers (
    id INTEGER PRIMARY KEY,
    tool TEXT NOT NULL,
    domain TEXT NOT NULL,

    -- State
    is_open BOOLEAN DEFAULT FALSE,
    failure_count INTEGER DEFAULT 0,
    consecutive_failures INTEGER DEFAULT 0,

    -- Thresholds
    failure_threshold INTEGER DEFAULT 5,
    timeout_seconds INTEGER DEFAULT 900,  -- 15 minutes

    -- Timing
    opened_at TIMESTAMP,
    closes_at TIMESTAMP,
    last_failure_at TIMESTAMP,
    last_success_at TIMESTAMP,

    -- Decay window (reset counts after success)
    success_window_minutes INTEGER DEFAULT 60,

    UNIQUE(tool, domain)
);

CREATE INDEX idx_breaker_state ON circuit_breakers(is_open, closes_at);
```

**Reset Policy:**
```python
class CircuitBreaker:
    """Persistent circuit breaker with decay"""

    async def check_and_maybe_close(self, tool: str, domain: str):
        """Check if breaker should close due to timeout"""
        breaker = await self.db.get_breaker(tool, domain)

        if breaker.is_open and now() >= breaker.closes_at:
            # Timeout expired, attempt half-open
            await self.db.update_breaker(
                tool, domain,
                is_open=False,
                consecutive_failures=0
            )
            logger.info(f"Circuit breaker half-open: {tool}/{domain}")

    async def record_success(self, tool: str, domain: str):
        """Success resets failure counter with decay"""
        breaker = await self.db.get_breaker(tool, domain)

        # Decay consecutive failures
        new_count = max(0, breaker.consecutive_failures - 1)

        await self.db.update_breaker(
            tool, domain,
            consecutive_failures=new_count,
            last_success_at=now()
        )
```

---

## 4. Tech Stack Adjustments

### Approved Stack:

| Component | Technology | Reason |
|-----------|------------|--------|
| **Framework** | FastAPI | Async, proven |
| **HTTP Client** | httpx | Async, connection pooling |
| **Playwright** | async_playwright | JavaScript rendering |
| **Database** | aiosqlite | Async SQLite wrapper |
| **HTML Parsing** | selectolax (primary) | Speed in hot paths |
|  | lxml (fallback) | Complex cleanup |
| **Serialization** | orjson | Fast JSON for cache blobs |
| **Content Extract** | readability-lxml + trafilatura | Quality extraction |

### Key Changes from Original:
- ✅ **aiosqlite** instead of blocking SQLite
- ✅ **selectolax** preferred over lxml for speed
- ✅ **orjson** for cache serialization

---

## 5. MVP Scope (Refined)

### ✅ KEEP in MVP:

1. **Cache system** (SQLite + disk blobs)
2. **Routing policy** (domain heuristics)
3. **Tool adapters** (WebFetch, Playwright, WebSearch)
4. **Fallback chain** (deterministic)
5. **Telemetry skeleton** (JSON logs + Prometheus)
6. **Rate limiting** (shared registry)
7. **Circuit breakers** (persistent)
8. **Content cleaning** (basic pipeline)

### ❌ CUT from MVP (Move to Phase 2):

1. **MinHash deduplication** → Stub with simple hash
2. **Multi-source aggregation** → Use top-1 result only
3. **LangGraph orchestration** → Async primitives sufficient
4. **Vector semantic dedupe** → Not needed yet
5. **LLM quality grading** → Heuristics only

**Rationale:** Stabilize base pipeline first, add complexity later

---

## 6. Implementation Order

### Week 1: Persistence Foundation
```
Day 1-2: SQLite schema + WAL setup + AsyncDAO layer
Day 3-4: Cache writer (metadata + disk blobs) + tests
Day 5-6: Circuit breaker tables + persistence logic
Day 7: Rate limit registry + domain config
```

### Week 2: Tool Adapters + Routing
```
Day 1-2: WebFetch adapter + httpx connection pool
Day 3-4: Playwright adapter (single context) + tests
Day 5-6: WebSearch adapter + aggregation
Day 7: Routing policy engine + fallback chain
```

### Week 3: Content Pipeline + Integration
```
Day 1-2: HTML extraction (selectolax + readability)
Day 3-4: Content cleaning + normalization
Day 5-6: Response schema + JSON serialization (orjson)
Day 7: Telemetry hooks (JSON logs + Prometheus metrics)
```

---

## 7. Testing Strategy

### Unit Tests (pytest)

```python
# DAO Layer
def test_async_dao_concurrent_writes():
    """Verify WAL mode handles concurrent writes"""
    pass

# Routing Policy
@pytest.mark.parametrize("domain,expected_tool", [
    ("medium.com", "playwright"),
    ("github.com", "webfetch"),
    ("unknown.com", "webfetch"),  # Try fast first
])
def test_routing_decision(domain, expected_tool):
    """Test routing logic with fixtures"""
    pass

# Content Cleaners
def test_content_cleaner_golden_html():
    """Test with golden HTML fixtures"""
    with open("tests/fixtures/medium_article.html") as f:
        html = f.read()

    cleaned = cleaner.process(html)
    assert len(cleaned.text) > 1000
    assert cleaned.quality_score > 0.7
```

### Integration Tests

```python
@pytest.fixture
async def fake_http_server():
    """Spin up pytest-httpserver"""
    with pytest_httpserver.HTTPServer() as server:
        yield server

async def test_webfetch_403_fallback(fake_http_server):
    """Verify fallback on 403"""
    fake_http_server.expect_request("/article").respond_with_data(
        status=403
    )

    result = await orchestrator.fetch(
        url=fake_http_server.url_for("/article")
    )

    # Should fallback to Playwright
    assert result.tool_used == "playwright"
    assert result.fallback_from == "webfetch"

async def test_playwright_smoke():
    """Lightweight Playwright test"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        content = await page.content()
        assert "Example Domain" in content
```

### Regression Corpus

```yaml
# tests/data/retrieval_cases.yaml

success_cases:
  - url: https://github.com/microsoft/playwright
    expected_tool: webfetch
    min_quality: 0.8

  - url: https://angular.io/guide/routing
    expected_tool: webfetch
    min_quality: 0.9

failure_cases:
  - url: https://medium.com/@author/article
    expected_tool: playwright  # WebFetch will fail
    fallback_from: webfetch
    min_quality: 0.7

edge_cases:
  - url: https://timeout-site.example.com/slow
    expected_behavior: timeout_fallback
    max_latency_seconds: 30
```

**Run nightly:**
```bash
pytest tests/regression/test_corpus.py --corpus=tests/data/retrieval_cases.yaml
```

---

## 8. Observability

### JSON Structured Logging

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "retrieval_attempt",
    request_id="req-12345",
    url="https://medium.com/article",
    domain="medium.com",
    tool="playwright",
    cache_hit=False,
    latency_ms=3420,
    quality_score=0.82,
    success=True,
    fallback_from="webfetch",
    error_type=None,
)
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Success/Failure counts
retrieval_success_total = Counter(
    'retrieval_success_total',
    'Successful retrievals',
    ['tool', 'domain']
)

retrieval_failure_total = Counter(
    'retrieval_failure_total',
    'Failed retrievals',
    ['tool', 'domain', 'error_type']
)

# Latency histograms
retrieval_latency_seconds = Histogram(
    'retrieval_latency_seconds',
    'Retrieval latency',
    ['tool'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

# Cache performance
cache_hit_ratio = Gauge('cache_hit_ratio', 'Cache hit ratio')

# Circuit breakers
circuit_breaker_open_total = Gauge(
    'circuit_breaker_open_total',
    'Open circuit breakers',
    ['tool', 'domain']
)

# Rate limiter
rate_limiter_throttles_total = Counter(
    'rate_limiter_throttles_total',
    'Rate limiter throttles',
    ['domain']
)
```

### Health Endpoint

```python
@app.get("/health")
async def health_check():
    """Lightweight health check"""
    return {
        "status": "healthy",
        "queue_depth": orchestrator.queue.qsize(),
        "open_breakers": await db.count_open_breakers(),
        "cache_hit_ratio": metrics.cache_hit_ratio.get(),
        "uptime_seconds": time.time() - start_time,
    }
```

---

## 9. Security Concerns

### HTML Sanitization

```python
from bleach import clean

def sanitize_html(html: str) -> str:
    """Strip dangerous content before caching"""
    return clean(
        html,
        tags=['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li',
              'code', 'pre', 'blockquote', 'strong', 'em', 'table', 'tr', 'td'],
        attributes={'a': ['href'], 'code': ['class']},
        strip=True
    )
```

### Credential Management

```python
# NEVER store credentials in code or DB
# Use Windows Credential Manager

import keyring

def get_site_credentials(domain: str) -> Optional[dict]:
    """Retrieve credentials from Windows Credential Manager"""
    username = keyring.get_password(f"claude-scraper:{domain}", "username")
    password = keyring.get_password(f"claude-scraper:{domain}", "password")

    if username and password:
        # Log access for audit
        await audit_log.log_credential_access(domain, reason="playwright_auth")
        return {'username': username, 'password': password}

    return None
```

### robots.txt Enforcement

```python
@app.before_request
async def enforce_robots_txt(request):
    """Enforce robots.txt BEFORE any fetch"""
    domain = extract_domain(request.url)

    # Check compliance
    allowed = await compliance_checker.is_allowed(domain, request.url)

    if not allowed:
        # Log denial
        logger.warning(
            "robots_txt_denial",
            url=request.url,
            domain=domain,
            reason="disallowed_by_robots_txt"
        )

        raise ForbiddenError(f"robots.txt disallows scraping {request.url}")
```

---

## 10. Long-Term Advice

### Migration Path (When Needed)

**Trigger:** Concurrent sessions > 10

**Actions:**
1. Migrate metadata: SQLite → PostgreSQL
2. Move cache blobs: Disk → S3/MinIO
3. Keep abstraction layer (DAO pattern) for mechanical change

```python
# Abstraction layer allows easy swap
class StorageBackend(Protocol):
    async def store(self, key: str, content: bytes): ...
    async def retrieve(self, key: str) -> bytes: ...

# Implementations
class DiskStorage(StorageBackend): ...
class S3Storage(StorageBackend): ...

# Usage
storage: StorageBackend = DiskStorage()  # MVP
# Later: storage = S3Storage()  # Phase 3
```

### Refactor Triggers

**Consider LangGraph/Temporal when:**
- Fallback chains need per-user personalization
- Workflow branching becomes complex
- Need visual workflow inspection
- Agent-like decision making required

### KPIs to Track

```python
KPI_TARGETS = {
    'tool_success_rate_per_domain': {
        'target': 0.95,
        'alert_threshold': 0.80,
    },
    'avg_time_to_first_content': {
        'target': 3.0,  # seconds
        'alert_threshold': 10.0,
    },
    'cache_hit_ratio': {
        'target': 0.70,
        'alert_threshold': 0.40,
    },
    'breaker_open_rate': {
        'target': 0.05,  # 5% of requests
        'alert_threshold': 0.20,
    },
    'pages_per_minute': {
        'target': 20,
        'alert_threshold': 5,
    },
}
```

---

## Summary

### ✅ GREEN LIGHT - Proceed with Implementation

**Conditions met:**
1. ✅ SQLite WAL mode + AsyncDAO layer
2. ✅ Shared rate-limit registry designed
3. ✅ Circuit breaker persistence documented
4. ✅ Tech stack adjusted (aiosqlite, selectolax, orjson)
5. ✅ MVP scope refined (cut complexity)
6. ✅ Implementation order defined
7. ✅ Testing strategy complete
8. ✅ Observability plan ready
9. ✅ Security concerns addressed

**Time to MVP:** 3 weeks (reduced from 6-10 days estimate by being realistic about testing/polish)

**Next step:** Begin Week 1 implementation - Persistence Foundation

---

**Decision Date:** 2025-10-17
**Decision Authority:** Multi-AI consultation synthesis + Architecture review
**Status:** ✅ APPROVED - Ready to code
