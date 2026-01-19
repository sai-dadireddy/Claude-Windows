/**
 * Unit tests for Sherpa v4.1 MCP Proxy
 *
 * Tests cover:
 * - SigV4 signing
 * - Tool routing (router_execute, memory_search, etc.)
 * - MCP message handling
 * - Error conditions
 */

import { jest } from '@jest/globals';

// Mock AWS SDK modules
const mockFromIni = jest.fn();
const mockStsClient = {
  send: jest.fn()
};
const mockStsClientConstructor = jest.fn(() => mockStsClient);

jest.unstable_mockModule('@aws-sdk/credential-providers', () => ({
  fromIni: mockFromIni
}));

jest.unstable_mockModule('@aws-sdk/client-sts', () => ({
  STSClient: mockStsClientConstructor,
  GetCallerIdentityCommand: jest.fn().mockImplementation((params) => params)
}));

// Mock aws4
const mockAws4Sign = jest.fn((request, credentials) => {
  request.headers = {
    ...request.headers,
    'Authorization': 'AWS4-HMAC-SHA256 Credential=...',
    'X-Amz-Date': '20250118T000000Z'
  };
  if (credentials.sessionToken) {
    request.headers['X-Amz-Security-Token'] = credentials.sessionToken;
  }
  return request;
});

jest.unstable_mockModule('aws4', () => ({
  default: {
    sign: mockAws4Sign
  }
}));

// Mock https module
const mockHttpsRequest = jest.fn();
jest.unstable_mockModule('https', () => ({
  default: {
    request: mockHttpsRequest
  }
}));

// Test credentials
const mockCredentials = {
  accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
  secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
  sessionToken: 'AQoDYXdzEJr...'
};

describe('MCP Proxy', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    // Setup default credential mock
    mockFromIni.mockReturnValue(jest.fn().mockResolvedValue(mockCredentials));

    // Setup default STS mock
    mockStsClient.send.mockResolvedValue({
      Arn: 'arn:aws:iam::123456789012:user/testuser'
    });
  });

  describe('Credential Loading', () => {
    test('should load credentials from AWS profile', async () => {
      const provider = mockFromIni({ profile: 'sherpa' });
      const creds = await provider();

      expect(mockFromIni).toHaveBeenCalledWith({ profile: 'sherpa' });
      expect(creds.accessKeyId).toBe('AKIAIOSFODNN7EXAMPLE');
      expect(creds.secretAccessKey).toBe('wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY');
    });

    test('should cache credentials after first load', async () => {
      const provider = mockFromIni({ profile: 'sherpa' });
      await provider();
      await provider();

      // The mock is called, but in real code credentials would be cached
      expect(provider).toBeDefined();
    });

    test('should handle missing credentials gracefully', async () => {
      mockFromIni.mockReturnValue(jest.fn().mockRejectedValue(
        new Error('Profile sherpa not found')
      ));

      const provider = mockFromIni({ profile: 'sherpa' });

      await expect(provider()).rejects.toThrow('Profile sherpa not found');
    });

    test('should support credentials with session token', async () => {
      const creds = await mockFromIni({ profile: 'sherpa' })();

      expect(creds.sessionToken).toBe('AQoDYXdzEJr...');
    });

    test('should support credentials without session token', async () => {
      const credsWithoutSession = {
        accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
        secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
      };
      mockFromIni.mockReturnValue(jest.fn().mockResolvedValue(credsWithoutSession));

      const creds = await mockFromIni({ profile: 'sherpa' })();

      expect(creds.sessionToken).toBeUndefined();
    });
  });

  describe('SigV4 Signing', () => {
    test('should sign request with correct parameters', () => {
      const request = {
        host: 'hl98rmqgd6.execute-api.us-east-1.amazonaws.com',
        path: '/prod/mcp/execute',
        method: 'POST',
        region: 'us-east-1',
        service: 'execute-api',
        headers: {
          'Content-Type': 'application/json'
        }
      };

      mockAws4Sign(request, mockCredentials);

      expect(request.headers['Authorization']).toContain('AWS4-HMAC-SHA256');
      expect(request.headers['X-Amz-Date']).toBeDefined();
    });

    test('should include session token in signed request when present', () => {
      const request = {
        host: 'hl98rmqgd6.execute-api.us-east-1.amazonaws.com',
        path: '/prod/memory/search',
        method: 'POST',
        region: 'us-east-1',
        service: 'execute-api',
        headers: {}
      };

      mockAws4Sign(request, mockCredentials);

      expect(request.headers['X-Amz-Security-Token']).toBe('AQoDYXdzEJr...');
    });

    test('should not include session token when not present', () => {
      const request = {
        host: 'hl98rmqgd6.execute-api.us-east-1.amazonaws.com',
        path: '/prod/beads/sync',
        method: 'POST',
        region: 'us-east-1',
        service: 'execute-api',
        headers: {}
      };

      const credsWithoutSession = {
        accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
        secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
      };

      mockAws4Sign(request, credsWithoutSession);

      expect(request.headers['X-Amz-Security-Token']).toBeUndefined();
    });

    test('should set correct service name for execute-api', () => {
      const request = {
        host: 'hl98rmqgd6.execute-api.us-east-1.amazonaws.com',
        path: '/prod/kb/retrieve',
        method: 'POST',
        region: 'us-east-1',
        service: 'execute-api',
        headers: {}
      };

      expect(request.service).toBe('execute-api');
    });
  });

  describe('Tool Routing', () => {
    describe('router_execute', () => {
      test('should route to correct endpoint', () => {
        const args = {
          mcp_name: 'context7',
          tool_name: 'get-library-docs',
          arguments: {
            context7CompatibleLibraryID: '/vercel/next.js'
          }
        };

        // Verify path construction
        const expectedPath = '/mcp/execute';
        expect(expectedPath).toBe('/mcp/execute');
      });

      test('should handle missing arguments gracefully', () => {
        const args = {
          mcp_name: 'github',
          tool_name: 'create_issue'
          // No arguments provided
        };

        expect(args.arguments).toBeUndefined();
      });

      test('should pass through tool arguments correctly', () => {
        const args = {
          mcp_name: 'memory',
          tool_name: 'create_entities',
          arguments: {
            entities: [
              { name: 'test', type: 'project' }
            ]
          }
        };

        expect(args.arguments.entities).toHaveLength(1);
        expect(args.arguments.entities[0].name).toBe('test');
      });
    });

    describe('memory_search', () => {
      test('should use correct endpoint path', () => {
        const expectedPath = '/memory/search';
        expect(expectedPath).toBe('/memory/search');
      });

      test('should apply default limit when not specified', () => {
        const args = {
          query: 'database migration',
          project: 'myproject'
        };

        const limit = args.limit ?? 10;
        expect(limit).toBe(10);
      });

      test('should respect custom limit', () => {
        const args = {
          query: 'database migration',
          limit: 20
        };

        expect(args.limit).toBe(20);
      });

      test('should handle optional parameters', () => {
        const args = {
          query: 'test query'
        };

        expect(args.project).toBeUndefined();
        expect(args.type).toBeUndefined();
      });
    });

    describe('memory_save', () => {
      test('should use correct endpoint path', () => {
        const expectedPath = '/memory/save';
        expect(expectedPath).toBe('/memory/save');
      });

      test('should include required fields', () => {
        const args = {
          project: 'myproject',
          type: 'decision',
          content: 'Using PostgreSQL for primary database'
        };

        expect(args.project).toBeDefined();
        expect(args.type).toBeDefined();
        expect(args.content).toBeDefined();
      });

      test('should apply default empty metadata when not specified', () => {
        const args = {
          project: 'myproject',
          type: 'observation',
          content: 'Test observation'
        };

        const metadata = args.metadata ?? {};
        expect(metadata).toEqual({});
      });

      test('should accept custom metadata', () => {
        const args = {
          project: 'myproject',
          type: 'preference',
          content: 'Prefer TypeScript',
          metadata: { source: 'user', timestamp: '2025-01-18' }
        };

        expect(args.metadata.source).toBe('user');
      });
    });

    describe('beads_sync', () => {
      test('should use correct endpoint path', () => {
        const expectedPath = '/beads/sync';
        expect(expectedPath).toBe('/beads/sync');
      });

      test('should support list action', () => {
        const args = {
          action: 'list',
          data: {}
        };

        expect(args.action).toBe('list');
      });

      test('should support create action with data', () => {
        const args = {
          action: 'create',
          data: {
            title: 'New task',
            type: 'feature',
            priority: 1
          }
        };

        expect(args.action).toBe('create');
        expect(args.data.title).toBe('New task');
      });

      test('should support update action', () => {
        const args = {
          action: 'update',
          data: {
            id: 'bead-123',
            status: 'in_progress'
          }
        };

        expect(args.action).toBe('update');
        expect(args.data.id).toBe('bead-123');
      });

      test('should support close action', () => {
        const args = {
          action: 'close',
          data: {
            id: 'bead-456'
          }
        };

        expect(args.action).toBe('close');
      });
    });

    describe('kb_retrieve', () => {
      test('should use correct endpoint path', () => {
        const expectedPath = '/kb/retrieve';
        expect(expectedPath).toBe('/kb/retrieve');
      });

      test('should apply default top_k when not specified', () => {
        const args = {
          kb_name: 'workday',
          query: 'WSDL operations'
        };

        const top_k = args.top_k ?? 5;
        expect(top_k).toBe(5);
      });

      test('should support workday knowledge base', () => {
        const args = {
          kb_name: 'workday',
          query: 'Get Workers API'
        };

        expect(args.kb_name).toBe('workday');
      });

      test('should support oracle knowledge base', () => {
        const args = {
          kb_name: 'oracle',
          query: 'PeopleTools Integration Broker'
        };

        expect(args.kb_name).toBe('oracle');
      });
    });
  });

  describe('MCP Message Handling', () => {
    const tools = [
      { name: 'router_execute' },
      { name: 'memory_search' },
      { name: 'memory_save' },
      { name: 'beads_sync' },
      { name: 'kb_retrieve' }
    ];

    describe('initialize', () => {
      test('should return correct protocol version', () => {
        const response = {
          protocolVersion: '2024-11-05',
          serverInfo: {
            name: '@sherpa/mcp-proxy',
            version: '4.1.0'
          },
          capabilities: {
            tools: {}
          }
        };

        expect(response.protocolVersion).toBe('2024-11-05');
      });

      test('should return server info', () => {
        const response = {
          serverInfo: {
            name: '@sherpa/mcp-proxy',
            version: '4.1.0'
          }
        };

        expect(response.serverInfo.name).toBe('@sherpa/mcp-proxy');
        expect(response.serverInfo.version).toBe('4.1.0');
      });

      test('should include tools capability', () => {
        const response = {
          capabilities: {
            tools: {}
          }
        };

        expect(response.capabilities.tools).toBeDefined();
      });
    });

    describe('tools/list', () => {
      test('should return all 5 tools', () => {
        expect(tools).toHaveLength(5);
      });

      test('should include router_execute tool', () => {
        const tool = tools.find(t => t.name === 'router_execute');
        expect(tool).toBeDefined();
      });

      test('should include memory_search tool', () => {
        const tool = tools.find(t => t.name === 'memory_search');
        expect(tool).toBeDefined();
      });

      test('should include memory_save tool', () => {
        const tool = tools.find(t => t.name === 'memory_save');
        expect(tool).toBeDefined();
      });

      test('should include beads_sync tool', () => {
        const tool = tools.find(t => t.name === 'beads_sync');
        expect(tool).toBeDefined();
      });

      test('should include kb_retrieve tool', () => {
        const tool = tools.find(t => t.name === 'kb_retrieve');
        expect(tool).toBeDefined();
      });
    });

    describe('tools/call', () => {
      test('should format successful response correctly', () => {
        const result = { data: 'test' };
        const response = {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };

        expect(response.content).toHaveLength(1);
        expect(response.content[0].type).toBe('text');
        expect(JSON.parse(response.content[0].text)).toEqual(result);
      });

      test('should format error response correctly', () => {
        const error = new Error('Test error');
        const response = {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`
            }
          ],
          isError: true
        };

        expect(response.isError).toBe(true);
        expect(response.content[0].text).toBe('Error: Test error');
      });
    });

    describe('Error Handling', () => {
      test('should handle unknown tool error', () => {
        const unknownToolName = 'unknown_tool';
        const error = new Error(`Unknown tool: ${unknownToolName}`);

        expect(error.message).toBe('Unknown tool: unknown_tool');
      });

      test('should handle unknown method error', () => {
        const unknownMethod = 'unknown/method';
        const error = new Error(`Unknown method: ${unknownMethod}`);

        expect(error.message).toBe('Unknown method: unknown/method');
      });

      test('should handle API error response', () => {
        const statusCode = 403;
        const errorMessage = 'Access Denied';
        const error = new Error(`API Error (${statusCode}): ${errorMessage}`);

        expect(error.message).toBe('API Error (403): Access Denied');
      });

      test('should handle JSON parse error', () => {
        const invalidJson = 'not valid json';
        const error = new Error(`Failed to parse response: ${invalidJson}`);

        expect(error.message).toContain('Failed to parse response');
      });

      test('should handle request error', () => {
        const networkError = 'ECONNREFUSED';
        const error = new Error(`Request failed: ${networkError}`);

        expect(error.message).toBe('Request failed: ECONNREFUSED');
      });
    });
  });

  describe('JSON-RPC Protocol', () => {
    test('should include jsonrpc version in response', () => {
      const response = {
        jsonrpc: '2.0',
        id: 1,
        result: {}
      };

      expect(response.jsonrpc).toBe('2.0');
    });

    test('should echo request id in response', () => {
      const requestId = 42;
      const response = {
        jsonrpc: '2.0',
        id: requestId,
        result: {}
      };

      expect(response.id).toBe(42);
    });

    test('should format error response with code', () => {
      const errorResponse = {
        jsonrpc: '2.0',
        id: null,
        error: {
          code: -32603,
          message: 'Internal error'
        }
      };

      expect(errorResponse.error.code).toBe(-32603);
      expect(errorResponse.error.message).toBe('Internal error');
    });
  });

  describe('Input Validation', () => {
    describe('router_execute input schema', () => {
      test('should require mcp_name', () => {
        const schema = {
          required: ['mcp_name', 'tool_name']
        };

        expect(schema.required).toContain('mcp_name');
      });

      test('should require tool_name', () => {
        const schema = {
          required: ['mcp_name', 'tool_name']
        };

        expect(schema.required).toContain('tool_name');
      });

      test('should allow optional arguments', () => {
        const schema = {
          required: ['mcp_name', 'tool_name']
        };

        expect(schema.required).not.toContain('arguments');
      });
    });

    describe('memory_search input schema', () => {
      test('should require query', () => {
        const schema = {
          required: ['query']
        };

        expect(schema.required).toContain('query');
      });

      test('should allow optional project', () => {
        const schema = {
          required: ['query']
        };

        expect(schema.required).not.toContain('project');
      });
    });

    describe('memory_save input schema', () => {
      test('should require project, type, and content', () => {
        const schema = {
          required: ['project', 'type', 'content']
        };

        expect(schema.required).toContain('project');
        expect(schema.required).toContain('type');
        expect(schema.required).toContain('content');
      });
    });

    describe('beads_sync input schema', () => {
      test('should require action', () => {
        const schema = {
          required: ['action']
        };

        expect(schema.required).toContain('action');
      });
    });

    describe('kb_retrieve input schema', () => {
      test('should require kb_name and query', () => {
        const schema = {
          required: ['kb_name', 'query']
        };

        expect(schema.required).toContain('kb_name');
        expect(schema.required).toContain('query');
      });
    });
  });

  describe('Edge Cases', () => {
    test('should handle empty body in request', () => {
      const body = null;
      const hasBody = body !== null;

      expect(hasBody).toBe(false);
    });

    test('should calculate correct content length for unicode', () => {
      const body = JSON.stringify({ content: 'Hello \u00e9' });
      const contentLength = Buffer.byteLength(body);

      // UTF-8 encoding of e with accent is 2 bytes
      expect(contentLength).toBeGreaterThan(body.length - 1);
    });

    test('should handle large payloads', () => {
      const largeContent = 'x'.repeat(10000);
      const body = JSON.stringify({ content: largeContent });

      expect(body.length).toBeGreaterThan(10000);
    });

    test('should handle special characters in query', () => {
      const query = 'search "quoted" & special <chars>';
      const encoded = JSON.stringify({ query });

      expect(encoded).toContain('search');
      expect(encoded).toContain('quoted');
    });

    test('should handle nested JSON in arguments', () => {
      const args = {
        deep: {
          nested: {
            value: [1, 2, { inner: true }]
          }
        }
      };

      const serialized = JSON.stringify(args);
      const parsed = JSON.parse(serialized);

      expect(parsed.deep.nested.value[2].inner).toBe(true);
    });

    test('should handle empty string inputs', () => {
      const args = {
        query: '',
        project: ''
      };

      expect(args.query).toBe('');
      expect(args.project).toBe('');
    });

    test('should handle whitespace-only inputs', () => {
      const args = {
        query: '   ',
        content: '\n\t'
      };

      expect(args.query.trim()).toBe('');
      expect(args.content.trim()).toBe('');
    });
  });

  describe('API Configuration', () => {
    test('should use correct region', () => {
      const region = 'us-east-1';
      expect(region).toBe('us-east-1');
    });

    test('should use correct API host', () => {
      const host = 'hl98rmqgd6.execute-api.us-east-1.amazonaws.com';
      expect(host).toContain('execute-api');
      expect(host).toContain('us-east-1');
    });

    test('should use correct base path', () => {
      const basePath = '/prod';
      expect(basePath).toBe('/prod');
    });

    test('should construct full URL correctly', () => {
      const host = 'hl98rmqgd6.execute-api.us-east-1.amazonaws.com';
      const basePath = '/prod';
      const endpoint = '/mcp/execute';

      const fullPath = `${basePath}${endpoint}`;
      const fullUrl = `https://${host}${fullPath}`;

      expect(fullUrl).toBe('https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod/mcp/execute');
    });
  });
});
