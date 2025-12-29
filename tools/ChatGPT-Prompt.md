# n8n Workflow Debugging - Parse RSS Feeds Issue

## Problem Summary
I have an n8n workflow that fetches RSS feeds and parses them, but the Parse RSS Feeds node is outputting 0 items even though the RSS fetch nodes successfully return data (each showing "1 item").

## Current Setup

**Workflow Flow:**
```
5 RSS Feed Nodes → Parse RSS Feeds → Merge All Sources → Deduplicate → Ollama Scoring → Filter → Save
```

**RSS Feed Nodes (HTTP Request):**
- URL: Various RSS feeds (OpenAI, Google AI, AWS ML, etc.)
- Response Format: `text` (configured in options)
- Successfully fetching data (shows "1 item" in execution)

**Parse RSS Feeds Node (Code):**
- Type: n8n Code node
- Receives input from 5 RSS feed nodes
- Should parse XML and extract articles
- Currently outputs 0 items

## The Issue

**Symptoms:**
1. RSS feed nodes show "1 item" (success)
2. Parse RSS Feeds node shows "No fields - node executed, but no items were sent on this branch"
3. Workflow completes in 4 seconds (should be 5-10 minutes)
4. articles.json has 0 articles

**Current Parse Code:**
```javascript
// Parse all RSS/Atom feeds using regex (Node.js compatible)
const extractTag = (xml, tag) => {
  const match = xml.match(new RegExp(`<${tag}[^>]*>([\s\S]*?)<\/${tag}>`, 'i'));
  return match ? match[1].replace(/<!\[CDATA\[|\]\]>/g, '').trim() : '';
};

const extractAttr = (xml, tag, attr) => {
  const match = xml.match(new RegExp(`<${tag}[^>]*${attr}="([^"]*)"`));
  return match ? match[1] : '';
};

const parseXMLFeed = (xmlText, sourceName) => {
  const articles = [];

  if (!xmlText || typeof xmlText !== 'string') {
    console.log(`WARNING: Invalid XML for ${sourceName}`);
    return articles;
  }

  const isAtom = xmlText.includes('<entry');
  const itemTag = isAtom ? 'entry' : 'item';

  const itemRegex = new RegExp(`<${itemTag}[^>]*>([\s\S]*?)<\/${itemTag}>`, 'gi');
  const items = xmlText.match(itemRegex) || [];

  console.log(`Found ${items.length} items in ${sourceName}`);

  const limitedItems = items.slice(0, 10);

  limitedItems.forEach(itemXml => {
    let title, link, pubDate, summary;

    if (isAtom) {
      title = extractTag(itemXml, 'title');
      link = extractAttr(itemXml, 'link', 'href') || extractTag(itemXml, 'link');
      pubDate = extractTag(itemXml, 'published') || extractTag(itemXml, 'updated');
      summary = extractTag(itemXml, 'summary') || extractTag(itemXml, 'content');
    } else {
      title = extractTag(itemXml, 'title');
      link = extractTag(itemXml, 'link');
      pubDate = extractTag(itemXml, 'pubDate');
      summary = extractTag(itemXml, 'description') || extractTag(itemXml, 'content:encoded');
    }

    if (summary) {
      summary = summary.replace(/<[^>]*>/g, '').substring(0, 500);
    }

    if (title && link) {
      articles.push({
        id: `${sourceName}-${Date.now()}-${Math.random()}`,
        source: sourceName,
        title: title,
        link: link,
        publishedDate: pubDate || new Date().toISOString(),
        summary: summary || '',
        category: getCategoryFromSource(sourceName)
      });
    }
  });

  return articles;
};

const getCategoryFromSource = (source) => {
  const categoryMap = {
    'OpenAI': 'OpenAI',
    'Google': 'Google/Gemini',
    'AWS': 'AWS AI/ML',
    'DeepMind': 'Google/Gemini'
  };

  for (const [key, value] of Object.entries(categoryMap)) {
    if (source.includes(key)) return value;
  }

  return 'General AI';
};

// Process all incoming items
const allArticles = [];

console.log(`=== Parse RSS Feeds START ===`);
console.log(`Total input items: ${$input.all().length}`);

for (const item of $input.all()) {
  console.log(`\nProcessing item...`);
  console.log(`Available keys: ${Object.keys(item.json).join(', ')}`);

  let xmlText = '';
  let sourceName = 'Unknown';

  // Try multiple possible data locations
  if (item.json.data && typeof item.json.data === 'string') {
    xmlText = item.json.data;
    console.log(`Found XML in 'data' field: ${xmlText.length} chars`);
  }

  if (!xmlText && item.json.body && typeof item.json.body === 'string') {
    xmlText = item.json.body;
    console.log(`Found XML in 'body' field: ${xmlText.length} chars`);
  }

  if (!xmlText && item.json.response && typeof item.json.response === 'string') {
    xmlText = item.json.response;
    console.log(`Found XML in 'response' field: ${xmlText.length} chars`);
  }

  if (item.json.__node_name__) {
    sourceName = item.json.__node_name__.replace(' RSS', '').replace(' API', '');
  }

  console.log(`Source name: ${sourceName}`);

  if (xmlText) {
    const articles = parseXMLFeed(xmlText, sourceName);
    console.log(`Parsed ${articles.length} articles from ${sourceName}`);
    allArticles.push(...articles);
  } else {
    console.log(`WARNING: No XML text found for this item!`);
    console.log(`Item JSON keys: ${Object.keys(item.json).join(', ')}`);
  }
}

console.log(`=== Parse RSS Feeds END: ${allArticles.length} total articles ===`);

return allArticles.map(article => ({ json: article }));
```

## Questions for ChatGPT

1. **What is the correct data structure returned by n8n HTTP Request nodes** when `responseFormat: "text"` is configured?
   - Where does the actual response data get stored? (`data`, `body`, `response`, or something else?)
   - Is it different for n8n version 1.x vs 2.x?

2. **Is my parsing code accessing the data correctly?**
   - I'm checking `item.json.data`, `item.json.body`, `item.json.response`
   - Should I be looking somewhere else?

3. **Why would the HTTP Request node show "1 item" but the Code node receive empty/undefined data?**

4. **Best practices for debugging n8n Code nodes:**
   - How can I inspect the exact structure of incoming data?
   - Are console.log statements visible anywhere in n8n?

5. **Alternative approaches:**
   - Should I use the XML node instead of parsing manually?
   - Is there a better way to handle multiple RSS feeds in n8n?

## What We've Tried

1. ✅ Fixed RSS feed URLs (OpenAI, removed Anthropic)
2. ✅ Added User-Agent headers to prevent 403 errors
3. ✅ Replaced non-existent Ollama community node with HTTP Request
4. ✅ Fixed workflow connections (all properly wired)
5. ✅ Updated parsing code to check multiple data field locations
6. ❌ Still outputs 0 articles

## Expected Behavior

When I tested the RSS feed manually with PowerShell:
```powershell
$response = Invoke-WebRequest -Uri 'https://openai.com/news/rss.xml' -UserAgent 'Mozilla/5.0...'
# Returns 687 items in the RSS feed
```

So the feeds definitely have data. The issue is in how n8n is passing data between nodes.

## Additional Context

- n8n running on localhost:5678
- Using free/open-source version of n8n
- HTTP Request node TypeVersion: 4.1
- Code node TypeVersion: 2

Please help me understand:
1. The correct data structure from n8n HTTP Request nodes
2. Why the parsing code isn't finding the XML data
3. How to properly debug and inspect data flowing between nodes in n8n

Thank you!
