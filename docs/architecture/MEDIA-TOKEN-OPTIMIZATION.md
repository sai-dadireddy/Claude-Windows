# Media Token Optimization Guide

**Created**: 2025-10-13
**Purpose**: Optimize token usage for YouTube transcripts and images
**Critical**: Media can consume 20K-50K tokens if not managed!

---

## 🎯 The Problem

You've optimized:
- ✅ MCP overhead: 66.8K → 8K
- ✅ Instructions: 20K → 3.5K
- ✅ Startup: 155K → 40K

But media content can quickly negate these savings:
- YouTube transcripts: 2K-12K tokens per video
- Images: 1K-1.5K tokens per HD screenshot
- Research session: Easily 20K-50K tokens of media!

---

## 📊 Token Costs Reference

### **YouTube Transcripts**
| Video Length | Words | Tokens (with formatting) |
|--------------|-------|--------------------------|
| 10 minutes   | 1,500 | ~2,000 tokens |
| 30 minutes   | 4,500 | ~6,000 tokens |
| 60 minutes   | 9,000 | ~12,000 tokens |

**Real scenarios**:
```
Researching AI news (5 videos, 20-min each): ~20K tokens
Tutorial deep-dive (3 videos, 45-min each): ~27K tokens
Conference talk (1 video, 90-min): ~18K tokens
```

### **Images**
| Image Size | Use Case | Token Cost |
|------------|----------|------------|
| 200x200 | Small icon/logo | ~85 tokens |
| 500x500 | Medium diagram | ~255 tokens |
| 1000x1000 | Large diagram | ~765 tokens |
| 1920x1080 (HD) | Screenshot | ~1,200-1,400 tokens |
| 2000x2000 | High-res diagram | ~1,600 tokens |

**Real scenarios**:
```
Architecture review (10 diagrams): ~7,000-8,000 tokens
UI debugging (5 screenshots): ~6,000-7,000 tokens
Presentation analysis (15 slides): ~12,000-15,000 tokens
```

---

## 🚀 Strategy 1: Agent-Based Media Processing (BEST!)

### **Create YouTube Research Agent**

File: `.claude/agents/youtube-research-heavy.md`

```markdown
---
name: "YouTube Research with Transcript Analysis"
description: "Isolated agent for YouTube transcript extraction and analysis"
model: "sonnet"
---

# YouTube Research Agent (Isolated Context)

You are a specialized YouTube research agent.

## Context Isolation
- Own 200K context window
- Process transcripts in YOUR context, not main
- Return summaries only (2-5K tokens max)

## Workflow
1. Extract YouTube transcript (2K-12K tokens in YOUR context)
2. Analyze and identify key points
3. Create structured summary:
   - Main topics (bullet points)
   - Key insights (numbered list)
   - Relevant quotes (with timestamps)
   - Actionable takeaways
4. Store full transcript in memory-auto (for later reference)
5. Return ONLY summary to main session

## What to Return
```json
{
  "video_title": "...",
  "duration": "30 minutes",
  "main_topics": [...],
  "key_insights": [...],
  "relevant_quotes": [
    {"timestamp": "5:32", "quote": "...", "context": "..."}
  ],
  "actionable_takeaways": [...],
  "full_transcript_stored": "memory_id_12345"
}
```

## Compression Ratio
Aim for 10:1 compression:
- 30-min video (6K tokens) → Summary (600 tokens)
- Main session never sees full transcript!
```

**Usage**:
```
You: "Use youtube-research-heavy to analyze this tutorial: [URL]"

Agent:
├─ Isolated 200K context
├─ Loads transcript: 6K tokens (in agent context)
├─ Analyzes content
├─ Stores full transcript in memory
└─ Returns: 600-token summary to main

Main session: 40K + 0.6K = 40.6K tokens ✅
(vs 40K + 6K = 46K if loaded directly!)
```

---

### **Create Visual Analysis Agent**

File: `.claude/agents/visual-analysis-heavy.md`

```markdown
---
name: "Visual Analysis with Image Processing"
description: "Isolated agent for image analysis and processing"
model: "sonnet"
---

# Visual Analysis Agent (Isolated Context)

You are a specialized visual analysis agent.

## Context Isolation
- Own 200K context window
- Process images in YOUR context
- Return structured analysis only

## Workflow
1. Receive images (1K-1.5K tokens EACH in YOUR context)
2. Analyze visual content:
   - Architecture diagrams → Extract components and relationships
   - Screenshots → Identify UI elements and issues
   - Flowcharts → Convert to text/mermaid diagram
   - Code screenshots → OCR and extract text
3. Create structured output (text-based)
4. Return analysis to main session (NO images!)

## What to Return
For architecture diagrams:
```markdown
## Architecture Analysis

### Components Identified:
- Frontend: React app with Redux state management
- API Gateway: Express.js on port 3000
- Database: PostgreSQL with connection pooling
- Cache: Redis for session storage

### Data Flow:
1. User request → Frontend
2. Frontend → API Gateway (REST)
3. API Gateway → Database (SQL queries)
4. Response cached in Redis
5. Response → Frontend

### Key Observations:
- No load balancer shown
- Single point of failure at API Gateway
- Database not replicated
```

For screenshots:
```markdown
## UI Analysis

### Layout:
- Header: Logo left, nav right
- Main content: 3-column grid
- Sidebar: Filters and search

### Issues Identified:
1. Button text cutoff on mobile (line 45, Button.tsx)
2. Misaligned icons in nav (CSS issue)
3. Color contrast fails WCAG (background #eee, text #ccc)

### Recommendations:
- Add responsive breakpoints at 768px and 1024px
- Increase text color to #666 for contrast
- Fix button padding to prevent text overflow
```

## Compression
- 1 HD screenshot (1.4K tokens) → Text analysis (300 tokens)
- 10 screenshots (14K tokens) → Analysis (3K tokens)
- Compression: 78% token savings!
```

**Usage**:
```
You: "Use visual-analysis-heavy to review these architecture diagrams"
[Attach 10 images]

Agent:
├─ Isolated 200K context
├─ Processes 10 images: 8K tokens (in agent context)
├─ Extracts components, relationships, flows
├─ Creates text-based analysis
└─ Returns: 2K text analysis to main

Main session: 40K + 2K = 42K tokens ✅
(vs 40K + 8K = 48K if images loaded directly!)
```

---

## 🚀 Strategy 2: Memory-Based Caching

### **Store Full Transcripts in Memory**

```
User: "Research these 3 YouTube videos"

Workflow:
1. youtube-research-heavy agent extracts transcripts
2. Agent stores FULL transcripts in memory-auto MCP:
   - video_1_full_transcript (6K tokens in memory, NOT context)
   - video_2_full_transcript (8K tokens in memory)
   - video_3_full_transcript (5K tokens in memory)
3. Agent returns summaries only (2K total to main)
4. Main session: 40K + 2K = 42K tokens ✅

Later:
User: "What did video 2 say about authentication at 15:30?"

Claude:
1. Queries memory for video_2_full_transcript
2. Retrieves relevant 2-minute section (~200 tokens)
3. Answers question using context from memory

No need to load full 8K transcript into main session!
```

**Benefits**:
- Full transcripts available for reference
- Only load what's needed when needed
- Main context stays lean

---

## 🚀 Strategy 3: Progressive Detail Loading

### **Start Minimal, Add Detail as Needed**

```
Level 1: Summary only (600 tokens)
├─ User: "What's this video about?"
└─ Response: Use summary from agent

Level 2: Specific sections (200-500 tokens per section)
├─ User: "What did they say about authentication?"
└─ Load relevant 2-minute transcript section from memory

Level 3: Full transcript (6K tokens)
├─ User: "I need to quote extensively from this"
└─ Load full transcript from memory (only when necessary!)
```

**Example**:
```
Session start: 40K tokens

User: "Research 5 videos on Claude Code optimization"

You:
├─ Spawn youtube-research-heavy agent
├─ Agent extracts 5 transcripts (30K tokens in agent context)
├─ Agent stores full transcripts in memory
├─ Agent returns 5 summaries (3K tokens to main)
└─ Main: 40K + 3K = 43K tokens ✅

User: "What did video 3 say about MCP optimization?"

You:
├─ Query memory for video_3 transcript
├─ Retrieve "MCP optimization" section (500 tokens)
├─ Main: 43K + 0.5K = 43.5K tokens ✅

User: "Give me exact quotes with timestamps for my article"

You:
├─ Load full video_3 transcript from memory (6K tokens)
├─ Main: 43.5K + 6K = 49.5K tokens
└─ Still under 50K! ✅
```

---

## 🚀 Strategy 4: Image Optimization Guidelines

### **Before Loading Images**

1. **Ask if needed**:
   ```
   User: "Here's a screenshot of the error"

   Claude: "Can you describe the error message text?
   I can help without seeing the image, which saves tokens."
   ```

2. **Request optimized size**:
   ```
   Claude: "If you need to share the screenshot:
   - Crop to relevant area only
   - Resize to max 1000x1000
   - Use PNG (not BMP or uncompressed formats)"
   ```

3. **Extract text first**:
   ```
   For code screenshots:
   - OCR the text
   - Share code as text (much fewer tokens!)
   - Image only if formatting/context matters
   ```

### **Image Processing Workflow**

```
User shares HD screenshot (1.4K tokens)

Option A (Inefficient):
├─ Load image into main context: 1.4K tokens
├─ Claude analyzes
└─ Main: 40K + 1.4K = 41.4K tokens

Option B (Efficient - Use Agent):
├─ visual-analysis-heavy agent receives image
├─ Image loaded in agent context: 1.4K (isolated)
├─ Agent extracts text/analysis: 300 tokens
└─ Main: 40K + 0.3K = 40.3K tokens ✅

Savings: 1.1K tokens per image!
10 images: 11K tokens saved!
```

---

## 🚀 Strategy 5: Batch Processing

### **Process Multiple Media Items Together**

```
Instead of:
├─ Load video 1 transcript (6K)
├─ Discuss, then unload
├─ Load video 2 transcript (8K)
├─ Discuss, then unload
├─ Load video 3 transcript (5K)
└─ Total: 19K tokens loaded sequentially

Do this:
├─ Spawn youtube-research-heavy agent
├─ Agent processes all 3 videos in isolated context (19K in agent)
├─ Agent creates comparative analysis
├─ Agent returns: "Video 1 covered X, Video 2 focused on Y, Video 3 added Z"
└─ Main receives: 2K summary covering all 3 videos ✅
```

---

## 📋 Practical Examples

### **Example 1: AI News Research**

**Bad Approach**:
```
Morning: Load 5 AI news video transcripts (25K tokens)
Session: 40K + 25K = 65K tokens (32.5% usage)
After discussion: 65K + 30K work = 95K tokens (47.5%)
```

**Good Approach**:
```
Morning: youtube-research-heavy processes 5 videos
├─ Agent context: 25K tokens (isolated)
├─ Agent returns: 3K summary to main
└─ Main: 40K + 3K = 43K tokens (21.5%)

Throughout day:
├─ Reference specific videos via memory queries
├─ Add 30K work context
└─ End of day: 73K tokens (36.5%)

Savings: 22K tokens (23% less context usage!)
```

---

### **Example 2: Architecture Review**

**Bad Approach**:
```
Load 10 architecture diagrams: 8K tokens
Discuss architecture: 20K tokens
Total: 40K + 8K + 20K = 68K tokens
```

**Good Approach**:
```
visual-analysis-heavy analyzes 10 diagrams:
├─ Agent context: 8K tokens (isolated)
├─ Agent extracts: Components, relationships, flows
├─ Agent returns: 2K text-based analysis
└─ Main: 40K + 2K = 42K tokens

Discuss architecture based on text analysis: 20K
Total: 42K + 20K = 62K tokens

Savings: 6K tokens per architecture review!
```

---

## 🎯 Best Practices Summary

### **YouTube Transcripts**
1. ✅ Always use youtube-research-heavy agent
2. ✅ Store full transcripts in memory
3. ✅ Work from summaries (10:1 compression)
4. ✅ Load specific sections only when needed
5. ❌ Never load full transcripts into main context

### **Images**
1. ✅ Ask if description would work first
2. ✅ Use visual-analysis-heavy agent for batches
3. ✅ Optimize image size (max 1000x1000)
4. ✅ Extract text from code screenshots
5. ❌ Never load full-res images into main context

### **General Media**
1. ✅ Process in agent contexts (isolated)
2. ✅ Store full content in memory
3. ✅ Return summaries/analysis only
4. ✅ Load details progressively as needed
5. ❌ Never accumulate media in main session

---

## 📊 Token Savings Calculator

### **Scenario: Daily Research Session**

**Without Optimization**:
```
Startup: 40K
+ 5 YouTube videos: +25K
+ 10 architecture diagrams: +8K
+ Work context: +30K
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 103K tokens (51.5%)
```

**With Optimization**:
```
Startup: 40K
+ YouTube summaries (agent): +3K
+ Diagram analysis (agent): +2K
+ Work context: +30K
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 75K tokens (37.5%)

Savings: 28K tokens (27% reduction!)
```

---

## 🚀 Quick Start

### **1. Create YouTube Research Agent**
Copy `.claude/agents/youtube-research-heavy.md` template above

### **2. Create Visual Analysis Agent**
Copy `.claude/agents/visual-analysis-heavy.md` template above

### **3. Update Your Workflow**
```
Old: "Analyze this YouTube video: [URL]"
New: "Use youtube-research-heavy to analyze: [URL]"

Old: [Attach 10 screenshots]
New: "Use visual-analysis-heavy to review these images"
```

### **4. Use Memory for Storage**
```
Full transcripts/images → Store in memory-auto
Query memory when you need specific details
Keep main context lean!
```

---

## 🏆 Success Metrics

Your media optimization is working when:
- ✅ YouTube research: +3K tokens (not +25K)
- ✅ Image analysis: +2K tokens (not +8K)
- ✅ Daily sessions: <80K tokens (not 100K+)
- ✅ Never exceeding 50% context in normal work
- ✅ All-day sessions without restart

---

**Combined with MCP + Instruction optimization:**
- MCP: 66.8K → 8K ✅
- Instructions: 20K → 3.5K ✅
- Media: 33K → 5K ✅ (with agents)
- **Total savings: 143K tokens (71.5% reduction!)**

**You can now research 5 videos with 10 images and still be under 50K tokens!** 🎉
