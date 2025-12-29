# Progress Dashboard

Track your learning journey through the AI Learning Syllabus.

<div id="progress-dashboard">
    <p>Loading your progress...</p>
</div>

---

## Actions

<div class="dashboard-actions">
    <button id="export-progress" class="btn btn-primary">📥 Export Progress</button>
    <button id="reset-progress" class="btn btn-danger">🔄 Reset All Progress</button>
</div>

---

## Tips for Success

### 📅 Study Consistently
- **Set a schedule**: Dedicate specific hours each week
- **Track streaks**: Aim for consecutive days of learning
- **Review regularly**: Revisit completed topics monthly

### 📝 Take Good Notes
- **Summarize** key concepts in your own words
- **Code snippets**: Save examples that work
- **Questions**: Note what you don't understand to research later

### 🛠️ Build Projects
- **Don't skip projects**: They consolidate learning
- **Customize**: Adapt projects to your interests
- **Share**: Publish to GitHub and write blog posts

### 🤝 Get Help
- **Ask AI providers**: Use Claude, GPT, and Gemini for questions
- **Community**: Join forums and Discord servers
- **Office hours**: Some courses offer live Q&A

---

## Study Mode Guide

<div class="study-modes-guide">
    <div class="study-mode-card">
        <h3><span class="study-mode-tag study-mode-learn">Learn</span></h3>
        <p><strong>Focus</strong>: Understanding concepts, theory, architecture</p>
        <p><strong>Activities</strong>: Reading, watching videos, taking notes</p>
        <p><strong>Time</strong>: 30-50% of topic time</p>
        <p><strong>Best Provider</strong>: Claude (patient explanations, analogies)</p>
    </div>

    <div class="study-mode-card">
        <h3><span class="study-mode-tag study-mode-practice">Practice</span></h3>
        <p><strong>Focus</strong>: Coding, implementing, experimenting</p>
        <p><strong>Activities</strong>: Exercises, mini-projects, debugging</p>
        <p><strong>Time</strong>: 40-60% of topic time</p>
        <p><strong>Best Provider</strong>: GPT/Codex (best coding, debugging)</p>
    </div>

    <div class="study-mode-card">
        <h3><span class="study-mode-tag study-mode-deploy">Deploy</span></h3>
        <p><strong>Focus</strong>: Production deployment, monitoring, optimization</p>
        <p><strong>Activities</strong>: CI/CD setup, cloud deployment, observability</p>
        <p><strong>Time</strong>: 10-20% of topic time</p>
        <p><strong>Best Provider</strong>: Gemini (scale patterns, monitoring)</p>
    </div>
</div>

---

## Progress Milestones

### 🏁 Milestone 1: Foundation Complete (25%)
**Topics**: 1-13 (LLM Fundamentals, Data Engineering, RAG Basics)

**Achievement**: ✅ You understand transformers, embeddings, and basic RAG
**Next**: Start Project 1 (Local RAG Q&A Bot)

### 🏁 Milestone 2: Advanced Retrieval (50%)
**Topics**: 14-20 (Query Rewriting, HyDE, Reranking, Self-RAG, Graph RAG)

**Achievement**: ✅ You can build production-quality retrieval systems
**Next**: Complete Project 2 (Conversational Agent)

### 🏁 Milestone 3: Production Ready (75%)
**Topics**: 21-40 (Agents, LLMOps, Security, Optimization)

**Achievement**: ✅ You can deploy secure, monitored production systems
**Next**: Complete Project 3 (Multi-Agent System with LLMOps)

### 🏁 Milestone 4: Expert Mastery (100%)
**Topics**: 41-52 (Fine-Tuning, Responsible AI, Multimodal, Edge Deployment)

**Achievement**: ✅ Portfolio-ready AI engineer with capstone project
**Next**: Job applications, freelancing, or advanced research

---

## Learning Statistics

### Average Completion Times
- **Beginner Track**: 6 weeks (15-20 hours/week)
- **Standard Track**: 10 weeks (15-20 hours/week)
- **Deep Mastery**: 16 weeks (15-20 hours/week)

### Topic Difficulty Distribution
- **Beginner Topics**: 12 topics (~25%)
- **Intermediate Topics**: 25 topics (~48%)
- **Advanced Topics**: 15 topics (~27%)

### Hands-On vs Theory
- **Conceptual Learning**: 30%
- **Hands-On Practice**: 50%
- **Projects**: 20%

---

## Frequently Asked Questions

### Can I skip topics?
**Yes, but not recommended.** Topics are ordered with dependencies. If you skip, you may struggle with later topics.

**Exception**: If you already know a topic (e.g., you've built transformers before), you can mark it complete after reviewing the blueprint briefly.

### Can I change tracks mid-way?
**Yes!** Tracks are flexible. You can:
- Start Beginner, then jump to Standard if it's too easy
- Start Standard, then drop to Beginner if it's too fast
- Complete tracks non-linearly (but respect dependencies)

### How do I export my progress?
Click **"Export Progress"** button above. You'll get a JSON file with:
- All completed topics
- Your notes
- Timestamps
- Overall statistics

You can import this on another device or keep it as a backup.

### What if I lose my progress?
Progress is saved in browser **localStorage**. It persists across sessions but:
- ❌ Clearing browser data will delete it
- ❌ Different browsers don't sync
- ✅ Export regularly as backup
- ✅ Consider using browser profile sync

### Can multiple people use this on one computer?
Yes, but they'll share the same progress (same browser profile). Solutions:
- Use different browser profiles
- Use different browsers
- Export/import progress when switching users

---

## Next Steps

Ready to continue learning? Choose based on your progress:

<div class="dashboard-actions">
    <a href="topics/transformer-architecture/" class="btn btn-primary">📖 Next Topic</a>
    <a href="reference/topic-map/" class="btn btn-secondary">🗺️ View All Topics</a>
    <a href="tracks/overview/" class="btn btn-secondary">🎯 Review Study Tracks</a>
</div>

<style>
.study-modes-guide {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.study-mode-card {
    background: var(--md-code-bg-color);
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 4px solid var(--md-primary-fg-color);
}

.study-mode-card h3 {
    margin-top: 0;
}

.study-mode-card p {
    margin: 0.5rem 0;
    font-size: 0.875rem;
}
</style>
