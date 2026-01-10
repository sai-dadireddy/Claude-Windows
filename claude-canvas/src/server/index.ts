/**
 * Claude Canvas WebSocket Server
 * Handles two-way communication between Claude Code and canvas instances
 */

import { WebSocketServer, WebSocket } from 'ws';

interface CanvasInfo {
  id: string;
  type: string;
  ws: WebSocket;
  data: any;
}

const canvases = new Map<string, CanvasInfo>();

export function startServer(port: number = 3847): Promise<void> {
  return new Promise((resolve) => {
    const wss = new WebSocketServer({ port });

    console.log(`[Canvas Server] Starting on port ${port}...`);

    wss.on('connection', (ws) => {
      console.log('[Canvas Server] New connection');
      let canvasId: string | null = null;

      ws.on('message', (msg) => {
        try {
          const data = JSON.parse(msg.toString());
          console.log('[Canvas Server] Received:', data.type);

          switch (data.type) {
            case 'canvas_ready':
              canvasId = data.canvasId;
              canvases.set(canvasId, {
                id: canvasId,
                type: data.canvasType,
                ws,
                data: {},
              });
              console.log(`[Canvas Server] Canvas registered: ${canvasId} (${data.canvasType})`);
              break;

            case 'canvas_update':
              if (canvasId && canvases.has(canvasId)) {
                const canvas = canvases.get(canvasId)!;
                canvas.data = data.data;
                // Broadcast to any listeners (Claude Code)
                broadcastToClients(wss, {
                  type: 'canvas_data',
                  canvasId,
                  data: data.data,
                });
              }
              break;

            case 'canvas_closed':
              if (canvasId) {
                canvases.delete(canvasId);
                console.log(`[Canvas Server] Canvas closed: ${canvasId}`);
              }
              break;

            // Commands from Claude Code
            case 'spawn':
              // Forward spawn request - handled by CLI
              console.log(`[Canvas Server] Spawn request: ${data.canvasType}`);
              break;

            case 'update':
              // Update existing canvas
              if (data.canvasId && canvases.has(data.canvasId)) {
                const canvas = canvases.get(data.canvasId)!;
                canvas.ws.send(JSON.stringify({
                  action: 'update',
                  data: data.data,
                }));
              }
              break;

            case 'close':
              // Close canvas
              if (data.canvasId && canvases.has(data.canvasId)) {
                const canvas = canvases.get(data.canvasId)!;
                canvas.ws.send(JSON.stringify({ action: 'close' }));
                canvases.delete(data.canvasId);
              }
              break;

            case 'list':
              // List active canvases
              ws.send(JSON.stringify({
                type: 'canvas_list',
                canvases: Array.from(canvases.values()).map(c => ({
                  id: c.id,
                  type: c.type,
                  data: c.data,
                })),
              }));
              break;
          }
        } catch (e) {
          console.error('[Canvas Server] Parse error:', e);
        }
      });

      ws.on('close', () => {
        if (canvasId) {
          canvases.delete(canvasId);
          console.log(`[Canvas Server] Connection closed: ${canvasId}`);
        }
      });
    });

    wss.on('listening', () => {
      console.log(`[Canvas Server] Listening on ws://localhost:${port}`);
      resolve();
    });

    wss.on('error', (err) => {
      console.error('[Canvas Server] Error:', err);
    });

    // Handle shutdown
    process.on('SIGINT', () => {
      console.log('[Canvas Server] Shutting down...');
      wss.close();
      process.exit(0);
    });
  });
}

function broadcastToClients(wss: WebSocketServer, message: any) {
  const msg = JSON.stringify(message);
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(msg);
    }
  });
}

// Run if called directly
if (import.meta.main) {
  const port = parseInt(process.argv[2] || '3847');
  startServer(port);
}
