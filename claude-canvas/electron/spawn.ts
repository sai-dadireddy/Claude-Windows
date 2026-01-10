#!/usr/bin/env tsx
/**
 * Claude Canvas - Electron Popup Spawner
 * Quick way to spawn popup canvases without running full Electron app
 */

import { spawn } from 'child_process';
import { WebSocket } from 'ws';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const args = process.argv.slice(2);

// Parse arguments
let type = 'email';
let data: any = {};
let port = 3848;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--type' || args[i] === '-t') {
    type = args[++i];
  } else if (args[i] === '--data' || args[i] === '-d') {
    data = JSON.parse(args[++i]);
  } else if (args[i] === '--port' || args[i] === '-p') {
    port = parseInt(args[++i]);
  } else if (args[i] === 'help' || args[i] === '--help') {
    console.log(`
Claude Canvas Popup Spawner

Usage:
  npm run popup -- --type <type> --data '<json>'

Options:
  --type, -t   Canvas type (email, todo, table, json, calendar)
  --data, -d   Initial data as JSON string
  --port, -p   WebSocket port (default: 3848)

Examples:
  npm run popup -- --type email --data '{"to":"user@example.com"}'
  npm run popup -- --type todo --data '{"items":[{"text":"Task 1","done":false}]}'
  npm run popup -- --type table --data '{"rows":[{"name":"Alice","age":30}]}'
`);
    process.exit(0);
  }
}

async function tryConnectToServer(): Promise<boolean> {
  return new Promise((resolve) => {
    const ws = new WebSocket(`ws://localhost:${port}`);
    const timeout = setTimeout(() => {
      ws.close();
      resolve(false);
    }, 1000);

    ws.on('open', () => {
      clearTimeout(timeout);
      console.log(`[Popup] Connected to Electron server, spawning ${type} canvas...`);
      ws.send(JSON.stringify({ action: 'spawn', type, data }));

      ws.on('message', (msg) => {
        const response = JSON.parse(msg.toString());
        if (response.type === 'canvas_spawned') {
          console.log(`[Popup] Canvas spawned: ${response.canvasId}`);
          ws.close();
          resolve(true);
        }
      });
    });

    ws.on('error', () => {
      clearTimeout(timeout);
      resolve(false);
    });
  });
}

async function startElectronAndSpawn() {
  console.log('[Popup] Starting Electron app...');

  const electronPath = path.join(__dirname, '../node_modules/.bin/electron');
  const mainPath = path.join(__dirname, 'main/index.ts');

  const proc = spawn('npx', ['tsx', mainPath, '--type', type, '--data', JSON.stringify(data)], {
    stdio: 'inherit',
    shell: true,
    cwd: path.join(__dirname, '..'),
  });

  proc.on('error', (err) => {
    console.error('[Popup] Failed to start Electron:', err.message);
  });
}

async function main() {
  console.log(`[Popup] Spawning ${type} canvas...`);

  // Try to connect to existing server
  const connected = await tryConnectToServer();

  if (!connected) {
    // Start Electron app with initial canvas
    await startElectronAndSpawn();
  }
}

main().catch(console.error);
