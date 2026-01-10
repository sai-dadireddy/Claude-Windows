/**
 * Claude Canvas - Electron Main Process
 * Spawns always-on-top popup windows for rich UI canvases
 */

import { app, BrowserWindow, ipcMain, screen } from 'electron';
import { WebSocket, WebSocketServer } from 'ws';
import * as path from 'path';
import * as fs from 'fs';

interface CanvasWindow {
  id: string;
  type: string;
  window: BrowserWindow;
  data: any;
}

const canvasWindows = new Map<string, CanvasWindow>();
let wss: WebSocketServer | null = null;
let claudeWs: WebSocket | null = null;

// Window size presets by canvas type
const WINDOW_SIZES: Record<string, { width: number; height: number }> = {
  email: { width: 500, height: 450 },
  calendar: { width: 400, height: 500 },
  table: { width: 600, height: 400 },
  todo: { width: 350, height: 450 },
  json: { width: 500, height: 500 },
  markdown: { width: 600, height: 500 },
  chart: { width: 500, height: 400 },
  default: { width: 450, height: 400 },
};

function getWindowPosition(width: number, height: number) {
  const display = screen.getPrimaryDisplay();
  const { width: screenWidth, height: screenHeight } = display.workAreaSize;

  // Position in bottom-right corner with padding
  return {
    x: screenWidth - width - 20,
    y: screenHeight - height - 60,
  };
}

function createCanvasWindow(type: string, data: any): string {
  const canvasId = `canvas_${Date.now()}`;
  const size = WINDOW_SIZES[type] || WINDOW_SIZES.default;
  const position = getWindowPosition(size.width, size.height);

  const win = new BrowserWindow({
    width: size.width,
    height: size.height,
    x: position.x,
    y: position.y,
    alwaysOnTop: true,
    frame: false,
    transparent: false,
    resizable: true,
    skipTaskbar: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, '../preload/index.js'),
    },
  });

  // Load the renderer
  const rendererPath = path.join(__dirname, '../renderer/index.html');
  if (fs.existsSync(rendererPath)) {
    win.loadFile(rendererPath);
  } else {
    // Development: load from local server or inline
    win.loadURL(`data:text/html,${encodeURIComponent(getInlineHTML(type, data, canvasId))}`);
  }

  // Send initial data once loaded
  win.webContents.on('did-finish-load', () => {
    win.webContents.send('canvas-init', { type, data, canvasId });
  });

  win.on('closed', () => {
    canvasWindows.delete(canvasId);
    notifyClaude({ type: 'canvas_closed', canvasId });
  });

  canvasWindows.set(canvasId, { id: canvasId, type, window: win, data });

  return canvasId;
}

function getInlineHTML(type: string, data: any, canvasId: string): string {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Claude Canvas - ${type}</title>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {
      margin: 0;
      font-family: system-ui, -apple-system, sans-serif;
      background: #1a1a2e;
      color: #eee;
      overflow: hidden;
    }
    .titlebar {
      -webkit-app-region: drag;
      background: #16213e;
      padding: 8px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #0f3460;
    }
    .titlebar button {
      -webkit-app-region: no-drag;
    }
    .close-btn {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #e94560;
      border: none;
      cursor: pointer;
    }
    .close-btn:hover { background: #ff6b6b; }
    .content { padding: 16px; height: calc(100vh - 45px); overflow-y: auto; }
    input, textarea {
      background: #16213e;
      border: 1px solid #0f3460;
      color: #eee;
      padding: 8px 12px;
      border-radius: 6px;
      width: 100%;
      box-sizing: border-box;
    }
    input:focus, textarea:focus {
      outline: none;
      border-color: #e94560;
    }
    .btn {
      background: #e94560;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 6px;
      cursor: pointer;
    }
    .btn:hover { background: #ff6b6b; }
    label { display: block; margin-bottom: 4px; color: #aaa; font-size: 12px; }
    .field { margin-bottom: 12px; }
  </style>
</head>
<body>
  <div class="titlebar">
    <span style="font-size: 13px; font-weight: 500;">${type.charAt(0).toUpperCase() + type.slice(1)} Canvas</span>
    <button class="close-btn" onclick="window.close()"></button>
  </div>
  <div id="root" class="content"></div>
  <script>
    const canvasId = "${canvasId}";
    const canvasType = "${type}";
    const initialData = ${JSON.stringify(data)};

    // Canvas components
    const components = {
      email: EmailCanvas,
      todo: TodoCanvas,
      table: TableCanvas,
      json: JsonCanvas,
    };

    function EmailCanvas({ data, onUpdate }) {
      const [form, setForm] = React.useState({
        to: data.to || '',
        cc: data.cc || '',
        bcc: data.bcc || '',
        subject: data.subject || '',
        body: data.body || '',
      });

      const handleChange = (field, value) => {
        const newForm = { ...form, [field]: value };
        setForm(newForm);
        onUpdate(newForm);
      };

      return React.createElement('div', null, [
        React.createElement('div', { className: 'field', key: 'to' }, [
          React.createElement('label', null, 'To'),
          React.createElement('input', {
            value: form.to,
            onChange: e => handleChange('to', e.target.value),
            placeholder: 'recipient@example.com'
          })
        ]),
        React.createElement('div', { className: 'field', key: 'cc' }, [
          React.createElement('label', null, 'Cc'),
          React.createElement('input', {
            value: form.cc,
            onChange: e => handleChange('cc', e.target.value)
          })
        ]),
        React.createElement('div', { className: 'field', key: 'subject' }, [
          React.createElement('label', null, 'Subject'),
          React.createElement('input', {
            value: form.subject,
            onChange: e => handleChange('subject', e.target.value)
          })
        ]),
        React.createElement('div', { className: 'field', key: 'body' }, [
          React.createElement('label', null, 'Body'),
          React.createElement('textarea', {
            value: form.body,
            onChange: e => handleChange('body', e.target.value),
            rows: 8,
            style: { resize: 'vertical' }
          })
        ]),
        React.createElement('button', {
          className: 'btn',
          key: 'send',
          onClick: () => onUpdate({ ...form, action: 'send' })
        }, 'Send to Claude')
      ]);
    }

    function TodoCanvas({ data, onUpdate }) {
      const [items, setItems] = React.useState(data.items || []);
      const [newItem, setNewItem] = React.useState('');

      const addItem = () => {
        if (newItem.trim()) {
          const updated = [...items, { id: Date.now(), text: newItem, done: false }];
          setItems(updated);
          setNewItem('');
          onUpdate({ items: updated });
        }
      };

      const toggle = (id) => {
        const updated = items.map(i => i.id === id ? { ...i, done: !i.done } : i);
        setItems(updated);
        onUpdate({ items: updated });
      };

      return React.createElement('div', null, [
        React.createElement('div', { style: { display: 'flex', gap: '8px', marginBottom: '16px' }, key: 'input' }, [
          React.createElement('input', {
            value: newItem,
            onChange: e => setNewItem(e.target.value),
            placeholder: 'Add item...',
            onKeyPress: e => e.key === 'Enter' && addItem(),
            style: { flex: 1 }
          }),
          React.createElement('button', { className: 'btn', onClick: addItem }, '+')
        ]),
        ...items.map(item =>
          React.createElement('div', {
            key: item.id,
            onClick: () => toggle(item.id),
            style: {
              padding: '8px',
              marginBottom: '4px',
              background: '#16213e',
              borderRadius: '4px',
              cursor: 'pointer',
              textDecoration: item.done ? 'line-through' : 'none',
              opacity: item.done ? 0.6 : 1
            }
          }, (item.done ? '✓ ' : '○ ') + item.text)
        )
      ]);
    }

    function TableCanvas({ data, onUpdate }) {
      const columns = data.columns || (data.rows?.[0] ? Object.keys(data.rows[0]) : []);
      const rows = data.rows || [];

      return React.createElement('div', { style: { overflowX: 'auto' } },
        React.createElement('table', { style: { width: '100%', borderCollapse: 'collapse' } }, [
          React.createElement('thead', { key: 'head' },
            React.createElement('tr', null,
              columns.map(col =>
                React.createElement('th', {
                  key: col,
                  style: { padding: '8px', textAlign: 'left', borderBottom: '1px solid #0f3460', color: '#e94560' }
                }, col)
              )
            )
          ),
          React.createElement('tbody', { key: 'body' },
            rows.map((row, i) =>
              React.createElement('tr', { key: i },
                columns.map(col =>
                  React.createElement('td', {
                    key: col,
                    style: { padding: '8px', borderBottom: '1px solid #0f3460' }
                  }, String(row[col] ?? ''))
                )
              )
            )
          )
        ])
      );
    }

    function JsonCanvas({ data, onUpdate }) {
      const jsonData = data.data || data;
      return React.createElement('pre', {
        style: {
          background: '#16213e',
          padding: '12px',
          borderRadius: '6px',
          overflow: 'auto',
          fontSize: '12px',
          lineHeight: 1.5
        }
      }, JSON.stringify(jsonData, null, 2));
    }

    // Render
    const Component = components[canvasType] || JsonCanvas;
    const onUpdate = (newData) => {
      if (window.electronAPI) {
        window.electronAPI.sendUpdate(canvasId, newData);
      }
    };

    ReactDOM.render(
      React.createElement(Component, { data: initialData, onUpdate }),
      document.getElementById('root')
    );
  </script>
</body>
</html>`;
}

function notifyClaude(message: any) {
  if (claudeWs?.readyState === WebSocket.OPEN) {
    claudeWs.send(JSON.stringify(message));
  }
}

function startWebSocketServer(port: number = 3848) {
  wss = new WebSocketServer({ port });

  console.log(`[Canvas Electron] WebSocket server on port ${port}`);

  wss.on('connection', (ws) => {
    claudeWs = ws;
    console.log('[Canvas Electron] Claude connected');

    ws.on('message', (msg) => {
      try {
        const { action, type, data, canvasId } = JSON.parse(msg.toString());

        switch (action) {
          case 'spawn':
            const id = createCanvasWindow(type, data);
            ws.send(JSON.stringify({ type: 'canvas_spawned', canvasId: id }));
            break;

          case 'update':
            if (canvasId && canvasWindows.has(canvasId)) {
              const canvas = canvasWindows.get(canvasId)!;
              canvas.window.webContents.send('canvas-update', data);
            }
            break;

          case 'close':
            if (canvasId && canvasWindows.has(canvasId)) {
              canvasWindows.get(canvasId)!.window.close();
            }
            break;

          case 'list':
            ws.send(JSON.stringify({
              type: 'canvas_list',
              canvases: Array.from(canvasWindows.values()).map(c => ({
                id: c.id,
                type: c.type,
                data: c.data,
              })),
            }));
            break;
        }
      } catch (e) {
        console.error('[Canvas Electron] Parse error:', e);
      }
    });

    ws.on('close', () => {
      claudeWs = null;
      console.log('[Canvas Electron] Claude disconnected');
    });
  });
}

// IPC handlers
ipcMain.on('canvas-update', (event, { canvasId, data }) => {
  if (canvasWindows.has(canvasId)) {
    canvasWindows.get(canvasId)!.data = data;
  }
  notifyClaude({ type: 'canvas_data', canvasId, data });
});

ipcMain.handle('get-canvas-data', (event, canvasId) => {
  return canvasWindows.get(canvasId)?.data;
});

// App lifecycle
app.whenReady().then(() => {
  startWebSocketServer();

  // Parse command line for initial canvas
  const args = process.argv.slice(2);
  const typeIdx = args.indexOf('--type');
  const dataIdx = args.indexOf('--data');

  if (typeIdx !== -1 && args[typeIdx + 1]) {
    const type = args[typeIdx + 1];
    const data = dataIdx !== -1 && args[dataIdx + 1] ? JSON.parse(args[dataIdx + 1]) : {};
    createCanvasWindow(type, data);
  }
});

app.on('window-all-closed', () => {
  // Keep running for new canvas requests
});

app.on('before-quit', () => {
  wss?.close();
});
