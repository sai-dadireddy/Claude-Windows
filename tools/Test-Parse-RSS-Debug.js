// Debug version of Parse RSS Feeds
// This will log what we're actually receiving

console.log('=== DEBUG: Parse RSS Feeds ===');
console.log('Total input items:', $input.all().length);

for (const item of $input.all()) {
  console.log('\n--- Item Structure ---');
  console.log('Keys in item:', Object.keys(item));
  console.log('Keys in item.json:', Object.keys(item.json));

  // Check various possible locations for the XML data
  console.log('item.json.data exists?', !!item.json.data);
  console.log('item.json.body exists?', !!item.json.body);
  console.log('item.json.response exists?', !!item.json.response);

  if (item.json.data) {
    console.log('data type:', typeof item.json.data);
    console.log('data length:', item.json.data?.length);
    console.log('data preview:', item.json.data?.substring(0, 200));
  }

  if (item.json.body) {
    console.log('body type:', typeof item.json.body);
    console.log('body length:', item.json.body?.length);
    console.log('body preview:', item.json.body?.substring(0, 200));
  }
}

return [{ json: { debug: 'Check console output in n8n' } }];
