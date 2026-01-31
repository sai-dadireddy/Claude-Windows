#!/usr/bin/env node

/**
 * Sherpa v4.2 MCP Proxy
 *
 * Hybrid router for local and Lambda MCP endpoints with IAM SigV4 signing.
 * Routes: /mcp/* (router), /memory/* (CRUD), /beads/* (sync), /kb/* (retrieve)
 *
 * Local MCPs: playwright, code-index, context7, github, sequential-thinking, react, shadcn, vercel
 * Lambda MCPs: salesforce, jira, aws, oracle-db, oci, workday, peoplesoft, document-ops, firecrawl
 */

import { fromIni } from '@aws-sdk/credential-providers';
import { STSClient, GetCallerIdentityCommand } from '@aws-sdk/client-sts';
import aws4 from 'aws4';
import https from 'https';
import { spawn } from 'child_process';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

// Get manifest path relative to this file
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const MANIFEST_PATH = join(__dirname, '../../claudecodeshared/.claude/mcp/manifest.json');
const MCP_CONFIG_DIR = join(__dirname, '../../claudecodeshared/.claude/mcp');

// Load manifest for routing decisions
let manifest = null;
function loadManifest() {
  try {
    manifest = JSON.parse(readFileSync(MANIFEST_PATH, 'utf-8'));
    console.error(`[MCP-Proxy] Loaded manifest v${manifest.version} with ${manifest.backends.length} backends`);
  } catch (error) {
    console.error(`[MCP-Proxy] Warning: Could not load manifest: ${error.message}`);
    manifest = { backends: [] };
  }
}

// Get backend config from manifest
function getBackendConfig(mcpName) {
  if (!manifest) loadManifest();
  return manifest.backends.find(b => b.id === mcpName && b.enabled !== false);
}

// Check if MCP should be routed locally
function isLocalMcp(mcpName) {
  const backend = getBackendConfig(mcpName);
  return backend && backend.location === 'local';
}

// Local MCP process cache (for persistent connections)
const localMcpProcesses = new Map();

// AWS Configuration
const AWS_REGION = 'us-east-1';
const AWS_PROFILE = 'sherpa';
const API_ENDPOINT = 'https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod';
const API_HOST = 'hl98rmqgd6.execute-api.us-east-1.amazonaws.com';

// Load credentials from AWS profile
let credentials = null;

async function getCredentials() {
  if (!credentials) {
    const provider = fromIni({ profile: AWS_PROFILE });
    credentials = await provider();
  }
  return credentials;
}

// Verify AWS credentials on startup
async function verifyCredentials() {
  try {
    const creds = await getCredentials();
    const stsClient = new STSClient({
      region: AWS_REGION,
      credentials: creds
    });
    const identity = await stsClient.send(new GetCallerIdentityCommand({}));
    console.error(`[MCP-Proxy] Authenticated as: ${identity.Arn}`);
    return true;
  } catch (error) {
    console.error(`[MCP-Proxy] AWS authentication failed: ${error.message}`);
    return false;
  }
}

// Sign and execute AWS API Gateway request
async function signedRequest(path, method = 'POST', body = null) {
  const creds = await getCredentials();

  const requestOptions = {
    host: API_HOST,
    path: `/prod${path}`,
    method: method,
    region: AWS_REGION,
    service: 'execute-api',
    headers: {
      'Content-Type': 'application/json'
    }
  };

  if (body) {
    requestOptions.body = JSON.stringify(body);
    requestOptions.headers['Content-Length'] = Buffer.byteLength(requestOptions.body);
  }

  // Sign with SigV4
  aws4.sign(requestOptions, {
    accessKeyId: creds.accessKeyId,
    secretAccessKey: creds.secretAccessKey,
    sessionToken: creds.sessionToken
  });

  return new Promise((resolve, reject) => {
    const req = https.request(requestOptions, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(response);
          } else {
            reject(new Error(`API Error (${res.statusCode}): ${response.error || data}`));
          }
        } catch (parseError) {
          reject(new Error(`Failed to parse response: ${data}`));
        }
      });
    });

    req.on('error', (error) => {
      reject(new Error(`Request failed: ${error.message}`));
    });

    if (body) {
      req.write(requestOptions.body);
    }

    req.end();
  });
}

// MCP Tool Handlers

// Execute tool on local MCP server
async function executeLocalMcp(mcpName, toolName, toolArgs) {
  const backend = getBackendConfig(mcpName);
  if (!backend) {
    throw new Error(`Unknown MCP backend: ${mcpName}`);
  }

  // Load the MCP config file
  const configPath = join(MCP_CONFIG_DIR, backend.file);
  let mcpConfig;
  try {
    mcpConfig = JSON.parse(readFileSync(configPath, 'utf-8'));
  } catch (error) {
    throw new Error(`Failed to load MCP config for ${mcpName}: ${error.message}`);
  }

  if (!mcpConfig.command) {
    throw new Error(`MCP ${mcpName} has no command defined`);
  }

  // Execute the local MCP via stdio
  return new Promise((resolve, reject) => {
    const args = mcpConfig.args || [];
    const proc = spawn(mcpConfig.command, args, {
      stdio: ['pipe', 'pipe', 'pipe'],
      env: { ...process.env }
    });

    let stdout = '';
    let stderr = '';
    let responseReceived = false;

    proc.stdout.on('data', (data) => {
      stdout += data.toString();

      // Try to parse JSON-RPC responses
      const lines = stdout.split('\n');
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const response = JSON.parse(line);
          if (response.result && !responseReceived) {
            responseReceived = true;
            proc.kill();
            resolve(response.result);
          }
        } catch (e) {
          // Not valid JSON yet, keep buffering
        }
      }
    });

    proc.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    proc.on('error', (error) => {
      reject(new Error(`Failed to start local MCP ${mcpName}: ${error.message}`));
    });

    proc.on('close', (code) => {
      if (!responseReceived) {
        if (code !== 0) {
          reject(new Error(`Local MCP ${mcpName} exited with code ${code}: ${stderr}`));
        } else {
          reject(new Error(`Local MCP ${mcpName} closed without response`));
        }
      }
    });

    // Set timeout
    const timeout = mcpConfig.config?.timeout_ms || mcpConfig.config?.timeout || 30000;
    setTimeout(() => {
      if (!responseReceived) {
        proc.kill();
        reject(new Error(`Local MCP ${mcpName} timed out after ${timeout}ms`));
      }
    }, timeout);

    // Send initialize request
    const initRequest = {
      jsonrpc: '2.0',
      id: 1,
      method: 'initialize',
      params: {
        protocolVersion: '2024-11-05',
        clientInfo: { name: 'sherpa-mcp-proxy', version: '4.2.0' },
        capabilities: {}
      }
    };
    proc.stdin.write(JSON.stringify(initRequest) + '\n');

    // Send tools/call request after a small delay
    setTimeout(() => {
      const callRequest = {
        jsonrpc: '2.0',
        id: 2,
        method: 'tools/call',
        params: {
          name: toolName,
          arguments: toolArgs || {}
        }
      };
      proc.stdin.write(JSON.stringify(callRequest) + '\n');
    }, 100);
  });
}

async function routerExecute(args) {
  const { mcp_name, tool_name, arguments: toolArgs } = args;

  // Check if this is a local MCP
  if (isLocalMcp(mcp_name)) {
    console.error(`[MCP-Proxy] Routing ${mcp_name}.${tool_name} to LOCAL`);
    const result = await executeLocalMcp(mcp_name, tool_name, toolArgs);
    return result;
  }

  // Route to Lambda
  console.error(`[MCP-Proxy] Routing ${mcp_name}.${tool_name} to LAMBDA`);
  const response = await signedRequest('/mcp/execute', 'POST', {
    mcp_name,
    tool_name,
    arguments: toolArgs
  });

  return response;
}

async function memorySearch(args) {
  const { query, project, type, limit = 10 } = args;

  const response = await signedRequest('/memory/search', 'POST', {
    query,
    project,
    type,
    limit
  });

  return response;
}

async function memorySave(args) {
  const { project, type, content, metadata = {} } = args;

  const response = await signedRequest('/memory/save', 'POST', {
    project,
    type,
    content,
    metadata
  });

  return response;
}

async function beadsSync(args) {
  const { action, data } = args;

  const response = await signedRequest('/beads/sync', 'POST', {
    action,
    data
  });

  return response;
}

async function kbRetrieve(args) {
  const { kb_name, query, top_k = 5 } = args;

  const response = await signedRequest('/kb/retrieve', 'POST', {
    kb_name,
    query,
    top_k
  });

  return response;
}

// Router helper functions

async function routerAnalyzeIntent(args) {
  const { query } = args;
  if (!manifest) loadManifest();

  const queryLower = query.toLowerCase();
  const matches = [];

  // Check each category's triggers
  for (const [category, config] of Object.entries(manifest.categories || {})) {
    const matchedTriggers = config.triggers.filter(t => queryLower.includes(t.toLowerCase()));
    if (matchedTriggers.length > 0) {
      // Find backends in this category
      const backends = manifest.backends.filter(b => b.category === category && b.enabled !== false);
      matches.push({
        category,
        description: config.description,
        matched_triggers: matchedTriggers,
        backends: backends.map(b => ({ id: b.id, location: b.location }))
      });
    }
  }

  // Sort by number of matched triggers
  matches.sort((a, b) => b.matched_triggers.length - a.matched_triggers.length);

  return {
    query,
    suggestions: matches.slice(0, 3),
    top_suggestion: matches[0] || null
  };
}

async function routerListCategories() {
  if (!manifest) loadManifest();

  const categories = {};
  for (const [category, config] of Object.entries(manifest.categories || {})) {
    const backends = manifest.backends.filter(b => b.category === category && b.enabled !== false);
    categories[category] = {
      description: config.description,
      triggers: config.triggers,
      backends: backends.map(b => ({
        id: b.id,
        location: b.location,
        reason: b.reason
      }))
    };
  }

  return {
    version: manifest.version,
    categories,
    total_backends: manifest.backends.filter(b => b.enabled !== false).length
  };
}

async function routerLoadToolset(args) {
  const { mcp_name } = args;
  const backend = getBackendConfig(mcp_name);

  if (!backend) {
    throw new Error(`Unknown or disabled MCP: ${mcp_name}`);
  }

  // Load the MCP config file
  const configPath = join(MCP_CONFIG_DIR, backend.file);
  let mcpConfig;
  try {
    mcpConfig = JSON.parse(readFileSync(configPath, 'utf-8'));
  } catch (error) {
    throw new Error(`Failed to load MCP config for ${mcp_name}: ${error.message}`);
  }

  return {
    id: mcpConfig.id,
    name: mcpConfig.name,
    description: mcpConfig.description,
    location: backend.location,
    tools: mcpConfig.tools || [],
    triggers: mcpConfig.triggers || []
  };
}

// MCP Server Protocol

const tools = [
  {
    name: 'router_analyze_intent',
    description: 'Analyze query to find the right MCP backend based on triggers',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Natural language query to analyze' }
      },
      required: ['query']
    }
  },
  {
    name: 'router_list_categories',
    description: 'List all available MCP categories and their backends',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  },
  {
    name: 'router_load_toolset',
    description: 'Get detailed tool information for a specific MCP backend',
    inputSchema: {
      type: 'object',
      properties: {
        mcp_name: { type: 'string', description: 'MCP backend name to load tools for' }
      },
      required: ['mcp_name']
    }
  },
  {
    name: 'router_execute',
    description: 'Execute tool on backend MCP via Sherpa router (routes to local or Lambda based on manifest)',
    inputSchema: {
      type: 'object',
      properties: {
        mcp_name: { type: 'string', description: 'MCP backend name (e.g., "context7", "github")' },
        tool_name: { type: 'string', description: 'Tool name to execute' },
        arguments: { type: 'object', description: 'Tool arguments' }
      },
      required: ['mcp_name', 'tool_name']
    }
  },
  {
    name: 'memory_search',
    description: 'Search Sherpa memory system',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search query' },
        project: { type: 'string', description: 'Project name (optional)' },
        type: { type: 'string', description: 'Memory type: decision, preference, observation (optional)' },
        limit: { type: 'number', description: 'Max results (default: 10)' }
      },
      required: ['query']
    }
  },
  {
    name: 'memory_save',
    description: 'Save memory to Sherpa system',
    inputSchema: {
      type: 'object',
      properties: {
        project: { type: 'string', description: 'Project name' },
        type: { type: 'string', description: 'Memory type: decision, preference, observation' },
        content: { type: 'string', description: 'Memory content' },
        metadata: { type: 'object', description: 'Additional metadata (optional)' }
      },
      required: ['project', 'type', 'content']
    }
  },
  {
    name: 'beads_sync',
    description: 'Sync with Beads task tracker',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', description: 'Action: list, create, update, close' },
        data: { type: 'object', description: 'Action-specific data' }
      },
      required: ['action']
    }
  },
  {
    name: 'kb_retrieve',
    description: 'Retrieve from knowledge base (Workday/Oracle)',
    inputSchema: {
      type: 'object',
      properties: {
        kb_name: { type: 'string', description: 'KB name: workday, oracle' },
        query: { type: 'string', description: 'Search query' },
        top_k: { type: 'number', description: 'Number of results (default: 5)' }
      },
      required: ['kb_name', 'query']
    }
  }
];

// MCP Message Handler
async function handleMessage(message) {
  const { method, params } = message;

  switch (method) {
    case 'initialize':
      // Load manifest on initialize
      loadManifest();
      return {
        protocolVersion: '2024-11-05',
        serverInfo: {
          name: '@sherpa/mcp-proxy',
          version: '4.2.0'
        },
        capabilities: {
          tools: {}
        }
      };

    case 'tools/list':
      return { tools };

    case 'tools/call':
      const { name, arguments: args } = params;

      try {
        let result;

        switch (name) {
          case 'router_analyze_intent':
            result = await routerAnalyzeIntent(args);
            break;
          case 'router_list_categories':
            result = await routerListCategories();
            break;
          case 'router_load_toolset':
            result = await routerLoadToolset(args);
            break;
          case 'router_execute':
            result = await routerExecute(args);
            break;
          case 'memory_search':
            result = await memorySearch(args);
            break;
          case 'memory_save':
            result = await memorySave(args);
            break;
          case 'beads_sync':
            result = await beadsSync(args);
            break;
          case 'kb_retrieve':
            result = await kbRetrieve(args);
            break;
          default:
            throw new Error(`Unknown tool: ${name}`);
        }

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`
            }
          ],
          isError: true
        };
      }

    default:
      throw new Error(`Unknown method: ${method}`);
  }
}

// Main entry point
async function main() {
  console.error('[MCP-Proxy] Sherpa v4.2 MCP Proxy starting (hybrid local+lambda routing)...');

  // Verify AWS credentials
  const authenticated = await verifyCredentials();
  if (!authenticated) {
    console.error('[MCP-Proxy] Failed to authenticate. Check AWS profile "sherpa"');
    process.exit(1);
  }

  console.error('[MCP-Proxy] Ready. Waiting for MCP messages on stdin...');

  // MCP stdio transport
  let buffer = '';

  process.stdin.on('data', async (chunk) => {
    buffer += chunk.toString();

    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (!line.trim()) continue;

      try {
        const message = JSON.parse(line);
        const response = await handleMessage(message);

        process.stdout.write(JSON.stringify({
          jsonrpc: '2.0',
          id: message.id,
          result: response
        }) + '\n');
      } catch (error) {
        console.error(`[MCP-Proxy] Error handling message: ${error.message}`);
        process.stdout.write(JSON.stringify({
          jsonrpc: '2.0',
          id: null,
          error: {
            code: -32603,
            message: error.message
          }
        }) + '\n');
      }
    }
  });

  process.stdin.on('end', () => {
    console.error('[MCP-Proxy] Stdin closed. Exiting...');
    process.exit(0);
  });
}

main().catch((error) => {
  console.error(`[MCP-Proxy] Fatal error: ${error.message}`);
  process.exit(1);
});
