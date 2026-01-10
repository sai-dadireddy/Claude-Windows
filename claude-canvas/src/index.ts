/**
 * Claude Canvas - Main Entry
 * Spawns TUI canvases in Windows Terminal
 */

import { render } from 'ink';
import React from 'react';
import { WebSocket } from 'ws';

// Canvas components
import { EmailCanvas } from './canvases/email.js';
import { CalendarCanvas } from './canvases/calendar.js';
import { TableCanvas } from './canvases/table.js';
import { TodoCanvas } from './canvases/todo.js';
import { JsonCanvas } from './canvases/json.js';

export type CanvasType = 'email' | 'calendar' | 'table' | 'todo' | 'json' | 'markdown' | 'flight' | 'custom';

interface CanvasState {
  id: string;
  type: CanvasType;
  data: any;
  ws?: WebSocket;
}

const canvasComponents: Record<string, React.FC<any>> = {
  email: EmailCanvas,
  calendar: CalendarCanvas,
  table: TableCanvas,
  todo: TodoCanvas,
  json: JsonCanvas,
};

let activeCanvas: CanvasState | null = null;

export async function spawnCanvas(type: CanvasType, initialData: any = {}, port: number = 3847): Promise<void> {
  const canvasId = `canvas_${Date.now()}`;

  // Connect to Claude's WebSocket server
  let ws: WebSocket | undefined;
  try {
    ws = new WebSocket(`ws://localhost:${port}`);
    await new Promise<void>((resolve, reject) => {
      ws!.on('open', () => {
        ws!.send(JSON.stringify({ type: 'canvas_ready', canvasId, canvasType: type }));
        resolve();
      });
      ws!.on('error', reject);
      setTimeout(() => resolve(), 1000); // Continue even without server
    });
  } catch {
    // Server not running, continue standalone
  }

  activeCanvas = { id: canvasId, type, data: initialData, ws };

  const CanvasComponent = canvasComponents[type];
  if (!CanvasComponent) {
    console.error(`Unknown canvas type: ${type}`);
    process.exit(1);
  }

  // Handle updates from Claude
  if (ws) {
    ws.on('message', (msg: Buffer) => {
      try {
        const { action, data } = JSON.parse(msg.toString());
        if (action === 'update' && activeCanvas) {
          activeCanvas.data = { ...activeCanvas.data, ...data };
          // Re-render will happen via React state
        } else if (action === 'close') {
          process.exit(0);
        }
      } catch {}
    });
  }

  // Callback to send data back to Claude
  const onUpdate = (newData: any) => {
    if (activeCanvas) {
      activeCanvas.data = { ...activeCanvas.data, ...newData };
      if (ws?.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
          type: 'canvas_update',
          canvasId,
          data: activeCanvas.data
        }));
      }
    }
  };

  const onClose = () => {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'canvas_closed', canvasId }));
    }
    process.exit(0);
  };

  // Render the canvas
  const { waitUntilExit } = render(
    React.createElement(CanvasComponent, {
      ...initialData,
      onUpdate,
      onClose,
    })
  );

  await waitUntilExit();
}

export { EmailCanvas, CalendarCanvas, TableCanvas, TodoCanvas, JsonCanvas };
