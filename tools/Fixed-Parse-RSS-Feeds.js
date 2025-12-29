// FIXED: Parse all RSS/Atom feeds using regex (Node.js compatible)
// Version 2.0 - Handles n8n HTTP Request node data structure properly

const extractTag = (xml, tag) => {
  const match = xml.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'i'));
  return match ? match[1].replace(/<!\\[CDATA\\[|\\]\\]>/g, '').trim() : '';
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

  // Check if RSS or Atom format
  const isAtom = xmlText.includes('<entry');
  const itemTag = isAtom ? 'entry' : 'item';

  console.log(`Parsing ${sourceName}: ${xmlText.length} chars, format: ${isAtom ? 'Atom' : 'RSS'}`);

  // Split by item/entry tags
  const itemRegex = new RegExp(`<${itemTag}[^>]*>([\\s\\S]*?)<\\/${itemTag}>`, 'gi');
  const items = xmlText.match(itemRegex) || [];

  console.log(`Found ${items.length} items in ${sourceName}`);

  // Limit to first 10 articles per source to avoid overload
  const limitedItems = items.slice(0, 10);

  limitedItems.forEach(itemXml => {
    let title, link, pubDate, summary;

    if (isAtom) {
      // Atom format
      title = extractTag(itemXml, 'title');
      link = extractAttr(itemXml, 'link', 'href') || extractTag(itemXml, 'link');
      pubDate = extractTag(itemXml, 'published') || extractTag(itemXml, 'updated');
      summary = extractTag(itemXml, 'summary') || extractTag(itemXml, 'content');
    } else {
      // RSS format
      title = extractTag(itemXml, 'title');
      link = extractTag(itemXml, 'link');
      pubDate = extractTag(itemXml, 'pubDate');
      summary = extractTag(itemXml, 'description') || extractTag(itemXml, 'content:encoded');
    }

    // Clean HTML tags from summary
    if (summary) {
      summary = summary.replace(/<[^>]*>/g, '').substring(0, 500);
    }

    // Only add if we have at least title and link
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
    } else {
      console.log(`Skipping article in ${sourceName}: missing title or link`);
    }
  });

  return articles;
};

const getCategoryFromSource = (source) => {
  const categoryMap = {
    'OpenAI': 'OpenAI',
    'Google': 'Google/Gemini',
    'AWS': 'AWS AI/ML',
    'DeepMind': 'Google/Gemini',
    'Anthropic': 'Claude/Anthropic',
    'Microsoft': 'Microsoft AI',
    'Meta': 'Meta AI'
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
  // DEBUG: Log item structure
  console.log(`\\nProcessing item...`);
  console.log(`Available keys: ${Object.keys(item.json).join(', ')}`);

  // Try multiple possible data locations
  let xmlText = '';
  let sourceName = 'Unknown';

  // Method 1: Direct data field (n8n HTTP Request with responseFormat: "text")
  if (item.json.data && typeof item.json.data === 'string') {
    xmlText = item.json.data;
    console.log(`Found XML in 'data' field: ${xmlText.length} chars`);
  }

  // Method 2: Body field (alternative)
  if (!xmlText && item.json.body && typeof item.json.body === 'string') {
    xmlText = item.json.body;
    console.log(`Found XML in 'body' field: ${xmlText.length} chars`);
  }

  // Method 3: Response field (some HTTP clients)
  if (!xmlText && item.json.response && typeof item.json.response === 'string') {
    xmlText = item.json.response;
    console.log(`Found XML in 'response' field: ${xmlText.length} chars`);
  }

  // Method 4: Content field
  if (!xmlText && item.json.content && typeof item.json.content === 'string') {
    xmlText = item.json.content;
    console.log(`Found XML in 'content' field: ${xmlText.length} chars`);
  }

  // Extract source name from node execution data or URL
  if (item.json.__node_name__) {
    sourceName = item.json.__node_name__.replace(' RSS', '').replace(' API', '');
  } else if (item.json.url) {
    // Extract from URL
    sourceName = item.json.url.split('/')[2] || 'Unknown';
  }

  console.log(`Source name: ${sourceName}`);

  if (xmlText) {
    const articles = parseXMLFeed(xmlText, sourceName);
    console.log(`Parsed ${articles.length} articles from ${sourceName}`);
    allArticles.push(...articles);
  } else {
    console.log(`WARNING: No XML text found for this item!`);
    console.log(`Item JSON keys: ${Object.keys(item.json).join(', ')}`);
    // Log first item fully for debugging
    if (allArticles.length === 0) {
      console.log(`First item full structure:`, JSON.stringify(item.json, null, 2).substring(0, 1000));
    }
  }
}

console.log(`=== Parse RSS Feeds END: ${allArticles.length} total articles ===`);

return allArticles.map(article => ({ json: article }));
