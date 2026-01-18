#!/usr/bin/env node

/**
 * Sherpa v4.1 MCP Proxy
 *
 * Thin proxy for AWS Lambda MCP endpoints with IAM SigV4 signing.
 * Routes: /mcp/* (router), /memory/* (CRUD), /beads/* (sync), /kb/* (retrieve)
 */

import { fromIni } from '@aws-sdk/credential-providers';
import { STSClient, GetCallerIdentityCommand } from '@aws-sdk/client-sts';
import aws4 from 'aws4';
import https from 'https';

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

async function routerExecute(args) {
  const { mcp_name, tool_name, arguments: toolArgs } = args;

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

// MCP Server Protocol

const tools = [
  {
    name: 'router_execute',
    description: 'Execute tool on backend MCP via Sherpa router',
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
      return {
        protocolVersion: '2024-11-05',
        serverInfo: {
          name: '@sherpa/mcp-proxy',
          version: '4.1.0'
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
  console.error('[MCP-Proxy] Sherpa v4.1 MCP Proxy starting...');

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
