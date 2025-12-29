---
description: Optimize and enhance prompts using Claude Smart Improver techniques
---

# Prompt Improver - One-Click Optimization

Transform basic prompts into professional-grade, optimized versions using Anthropic's proven techniques.

## Your Prompt to Improve

**Paste your prompt below** (or describe what you want to achieve):

```
[USER WILL PASTE THEIR PROMPT HERE]
```

---

## Optimization Process

Apply the **5 Core Optimization Techniques**:

### 1. Chain-of-Thought Reasoning
- Add `<thinking>` sections for step-by-step reasoning
- Break down complex tasks into logical steps
- Make reasoning explicit and visible

### 2. Example Standardization
- Convert examples to consistent XML format
- Structure with `<example>` tags
- Include input/output pairs

### 3. Example Enrichment
- Generate 2-3 synthetic examples if none exist
- Show edge cases and variations
- Demonstrate desired output format

### 4. Prompt Rewriting
- Clarify vague instructions
- Fix grammatical/spelling issues
- Use active voice and specific verbs
- Organize into clear sections with XML tags:
  - `<task>` - What to do
  - `<rules>` - How to do it
  - `<examples>` - Demonstrations
  - `<output_format>` - Expected format

### 5. Prefill Addition
- Add Assistant prefill to guide response format
- Ensure output starts correctly
- Enforce structure from the beginning

---

## Output Format

Provide:

1. **Analysis** of the original prompt:
   - Strengths
   - Weaknesses
   - Improvement opportunities

2. **Optimized Prompt** with:
   - Clear structure (XML tags)
   - Chain-of-thought instructions
   - 2-3 high-quality examples
   - Explicit output format
   - Prefill guidance

3. **Before/After Comparison**:
   - Show key improvements
   - Explain why changes boost performance

4. **Expected Performance Gains**:
   - Accuracy improvement estimate
   - Format adherence
   - Consistency boost

---

## Optimization Guidelines

### When to Use Heavy Optimization:
- Complex reasoning tasks
- High accuracy requirements
- Migration from other AI models
- Production deployment
- Multi-step workflows

### When to Keep It Light:
- Simple, straightforward tasks
- Latency-sensitive applications
- Quick prototyping
- Speed is more important than perfection

---

## Example Transformation

### Before (Basic):
```
Classify this customer feedback into categories.
```

### After (Optimized):
```xml
<task>
Analyze customer feedback and classify it into predefined categories with confidence scores.
</task>

<rules>
1. Read the feedback carefully in the <thinking> section
2. Identify key themes and sentiments
3. Match to the most appropriate category
4. Assign confidence score (0-100)
5. Provide brief justification
</rules>

<examples>
<example>
<feedback>The product arrived damaged and customer service was unhelpful.</feedback>
<thinking>
- Issue: Damaged product (product quality)
- Issue: Unhelpful service (customer service)
- Sentiment: Negative
- Primary category: Product Quality (more specific complaint)
- Secondary: Customer Service
- Confidence: High (explicit complaints)
</thinking>
<output>
{
  "primary_category": "Product Quality",
  "secondary_category": "Customer Service",
  "confidence": 95,
  "justification": "Explicit mention of damaged product with secondary complaint about service response"
}
</output>
</example>
</examples>

<output_format>
Return JSON with:
- primary_category (string)
- secondary_category (string, optional)
- confidence (0-100)
- justification (brief explanation)
</output_format>
```

---

## Best Practices

✅ **Do:**
- Use XML tags for structure
- Include chain-of-thought reasoning
- Provide 2-3 diverse examples
- Specify exact output format
- Use active, specific language

❌ **Don't:**
- Over-optimize simple tasks
- Add unnecessary complexity
- Use vague instructions
- Skip examples for complex tasks
- Ignore output format specification

---

## Performance Metrics

Based on Anthropic's testing, expect:

- **+30% accuracy** for classification tasks
- **100% format adherence** for structured output
- **Reduced misinterpretation** of instructions
- **More consistent** results across runs
- **Better handling** of edge cases

---

## Quick Tips

1. **Start with structure**: Use `<task>`, `<rules>`, `<examples>` tags
2. **Show, don't tell**: Examples > long explanations
3. **Be specific**: "List 3 items" > "list some items"
4. **Use prefills**: Start the response for Claude
5. **Test iteratively**: Improve based on actual outputs

---

Now, **paste your prompt above** and I'll transform it using these proven techniques! 🚀
