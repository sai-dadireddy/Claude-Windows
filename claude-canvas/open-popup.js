#!/usr/bin/env node
/**
 * Claude Canvas - Browser Popup Opener
 * Opens canvas in default browser as popup
 */

import { exec } from 'child_process';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const args = process.argv.slice(2);

// Debug: show received args
console.log('Args received:', args);

// Parse arguments
let type = 'email';
let data = {};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--type' || args[i] === '-t') {
    type = args[++i];
  } else if (args[i] === '--data' || args[i] === '-d') {
    // Collect all remaining args as JSON (in case it got split)
    let jsonStr = args[++i];
    // If JSON was split by shell, reassemble it
    while (i + 1 < args.length && !args[i + 1].startsWith('--')) {
      jsonStr += args[++i];
    }
    try {
      data = JSON.parse(jsonStr);
    } catch (e) {
      console.error('Failed to parse JSON:', jsonStr);
      console.error('Error:', e.message);
    }
  } else if (args[i] === '--help' || args[i] === '-h') {
    console.log(`
Claude Canvas Browser Popup

Usage:
  node open-popup.js --type <type> --data '<json>'

Types: email, todo, table, json

Examples:
  node open-popup.js --type email --data '{"to":"user@example.com"}'
  node open-popup.js --type todo --data '{"items":[{"text":"Task 1","done":false}]}'
`);
    process.exit(0);
  }
}

// Build URL with cache buster
const htmlPath = path.join(__dirname, 'popup.html');
const dataParam = encodeURIComponent(JSON.stringify(data));
const cacheBuster = Date.now();
const url = `file:///${htmlPath.replace(/\\/g, '/')}?type=${type}&data=${dataParam}&_=${cacheBuster}`;

console.log(`Opening ${type} canvas in browser...`);
console.log('Data preview:', JSON.stringify(data).substring(0, 80) + (JSON.stringify(data).length > 80 ? '...' : ''));

// Open in default browser
const platform = process.platform;
let cmd;
if (platform === 'win32') {
  cmd = `start "" "${url}"`;
} else if (platform === 'darwin') {
  cmd = `open "${url}"`;
} else {
  cmd = `xdg-open "${url}"`;
}

exec(cmd, (err) => {
  if (err) {
    console.error('Failed to open browser:', err.message);
    console.log('URL:', url);
  } else {
    console.log('Canvas opened!');
  }
});
