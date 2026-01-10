#!/usr/bin/env bun
/**
 * Claude Canvas CLI
 * Spawn interactive TUI canvases for Claude Code
 */

import { Command } from 'commander';
import { spawnCanvas } from './index.js';

const program = new Command();

program
  .name('claude-canvas')
  .description('Windows-native TUI toolkit for Claude Code')
  .version('1.0.0');

program
  .command('spawn <type>')
  .description('Spawn a canvas of the given type')
  .option('-d, --data <json>', 'Initial data as JSON string')
  .option('-p, --port <number>', 'WebSocket port for Claude communication', '3847')
  .action(async (type: string, options: { data?: string; port: string }) => {
    const data = options.data ? JSON.parse(options.data) : {};
    await spawnCanvas(type, data, parseInt(options.port));
  });

program
  .command('list')
  .description('List available canvas types')
  .action(() => {
    console.log(`
Available Canvas Types:
  email      - Email composer with To/CC/BCC/Subject/Body
  calendar   - Interactive calendar/schedule viewer
  table      - Data table with sorting/filtering
  flight     - Flight booking comparison view
  todo       - Interactive todo list
  markdown   - Markdown preview pane
  json       - JSON viewer/editor
  custom     - Load custom React component
    `);
  });

program
  .command('server')
  .description('Start the WebSocket server for Claude communication')
  .option('-p, --port <number>', 'Port to listen on', '3847')
  .action(async (options: { port: string }) => {
    const { startServer } = await import('./server/index.js');
    await startServer(parseInt(options.port));
  });

program.parse();
