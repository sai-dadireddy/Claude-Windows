/**
 * Claude Canvas - Electron Preload Script
 * Exposes safe IPC methods to renderer
 */

import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  sendUpdate: (canvasId: string, data: any) => {
    ipcRenderer.send('canvas-update', { canvasId, data });
  },

  onInit: (callback: (payload: { type: string; data: any; canvasId: string }) => void) => {
    ipcRenderer.on('canvas-init', (_, payload) => callback(payload));
  },

  onUpdate: (callback: (data: any) => void) => {
    ipcRenderer.on('canvas-update', (_, data) => callback(data));
  },

  getCanvasData: (canvasId: string) => {
    return ipcRenderer.invoke('get-canvas-data', canvasId);
  },

  closeWindow: () => {
    window.close();
  },
});
