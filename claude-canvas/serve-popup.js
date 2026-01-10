#!/usr/bin/env node
/**
 * Claude Canvas - Local Server Popup
 * Serves canvas via localhost to avoid file:// URL issues
 */

import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { exec } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const args = process.argv.slice(2);

// Parse arguments
let type = 'email';
let data = {};
let port = 3850;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--type' || args[i] === '-t') {
    type = args[++i];
  } else if (args[i] === '--data' || args[i] === '-d') {
    let jsonStr = args[++i];
    while (i + 1 < args.length && !args[i + 1].startsWith('--')) {
      jsonStr += args[++i];
    }
    try {
      data = JSON.parse(jsonStr);
    } catch (e) {
      console.error('JSON parse error:', e.message);
    }
  } else if (args[i] === '--port' || args[i] === '-p') {
    port = parseInt(args[++i]);
  }
}

console.log(`Canvas type: ${type}`);
console.log(`Data: ${JSON.stringify(data).substring(0, 60)}...`);

// Read HTML file
const htmlPath = path.join(__dirname, 'popup.html');
let html = fs.readFileSync(htmlPath, 'utf8');

// Inject the type and data directly into the HTML
const injection = `
<script>
  // Injected by serve-popup.js
  window.CANVAS_TYPE = "${type}";
  window.CANVAS_DATA = ${JSON.stringify(data)};
</script>
`;

// Insert before closing </head>
html = html.replace('</head>', injection + '</head>');

// Modify the JS to use injected values instead of URL params
html = html.replace(
  "const params = new URLSearchParams(window.location.search);",
  "// Using injected values instead of URL params"
);
html = html.replace(
  "const canvasType = params.get('type') || 'email';",
  "const canvasType = window.CANVAS_TYPE || 'email';"
);
html = html.replace(
  "const initialData = params.get('data') ? JSON.parse(decodeURIComponent(params.get('data'))) : {};",
  "const initialData = window.CANVAS_DATA || {};"
);

// Create server
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(html);
});

// Find available port
function tryListen(p) {
  server.listen(p, '127.0.0.1', () => {
    const url = `http://127.0.0.1:${p}`;
    console.log(`Server running at ${url}`);

    // Open browser
    const cmd = process.platform === 'win32' ? `start "" "${url}"` :
                process.platform === 'darwin' ? `open "${url}"` : `xdg-open "${url}"`;

    exec(cmd, (err) => {
      if (err) console.error('Failed to open browser:', err.message);
      else console.log('Browser opened!');
    });

    // Auto-close server after 60 seconds
    setTimeout(() => {
      console.log('Server auto-closing after 60s');
      server.close();
      process.exit(0);
    }, 60000);
  });

  server.on('error', (e) => {
    if (e.code === 'EADDRINUSE') {
      console.log(`Port ${p} in use, trying ${p + 1}...`);
      tryListen(p + 1);
    } else {
      console.error('Server error:', e);
    }
  });
}

tryListen(port);
