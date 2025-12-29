# Free AI Assistant Setup for Multi-AI Orchestration (2025)

**Goal**: Replace Ollama with best free, local AI assistant for multi-AI collaboration

**Date**: 2025-10-18

---

## 🎯 Recommendation: LM Studio + Qwen2.5-Coder

**Why this combination?**

### LM Studio (Best Platform for Windows)
✅ **GUI-based** - Easy to use, no terminal complexity
✅ **Windows optimized** - Works great with NVIDIA GPUs
✅ **Hugging Face integration** - Direct model browser
✅ **Fast setup** - Download and run in minutes
✅ **MCP compatible** - Works with Claude Code orchestration
✅ **Free & Open Source** - Zero costs
✅ **Better for non-developers** - Polished interface

vs Ollama:
- Ollama: CLI-focused, better for developers/scripts
- LM Studio: GUI-focused, better for everyday use
- Both perform similarly, LM Studio easier for your use case

### Qwen2.5-Coder (Best Coding Model 2025)
✅ **Top benchmark performance** - Beats larger models
✅ **Agentic capabilities** - Handles entire workflows autonomously
✅ **92 programming languages** - Comprehensive coverage
✅ **Multiple sizes** - 0.5B to 32B (choose based on your hardware)
✅ **Long context** - 128K tokens
✅ **Trained on 5.5T tokens** - Massive training dataset
✅ **Free & Open Source** - No API costs

vs DeepSeek-Coder-V2:
- DeepSeek-V2: Better for math/logic reasoning, 338 languages, MoE architecture
- Qwen2.5-Coder: Better for practical coding, faster, more optimized
- Qwen wins on HumanEval benchmark (most relevant for coding)

---

## 📊 Hardware Requirements

### Minimum (Small Models)
- **RAM**: 8GB
- **GPU**: Optional (CPU-only works)
- **Disk**: 10GB free space
- **Model**: Qwen2.5-Coder 0.5B or 1.5B

### Recommended (Medium Models)
- **RAM**: 16GB
- **GPU**: NVIDIA GTX 1660 or better (6GB VRAM)
- **Disk**: 20GB free space
- **Model**: Qwen2.5-Coder 7B (recommended for most users)

### Optimal (Large Models)
- **RAM**: 32GB+
- **GPU**: NVIDIA RTX 3090/4090 (24GB VRAM)
- **Disk**: 40GB free space
- **Model**: Qwen2.5-Coder 14B or 32B

---

## 🚀 Installation Guide

### Step 1: Download LM Studio

**Official Website**: https://lmstudio.ai/

```bash
# For Windows:
1. Visit https://lmstudio.ai/
2. Click "Download for Windows"
3. Run LMStudio-0.3.x-Setup.exe
4. Follow installer wizard
5. Launch LM Studio
```

**Time**: 2-3 minutes

---

### Step 2: Install Qwen2.5-Coder Model

**In LM Studio**:

1. Click **"Search"** tab (magnifying glass icon)
2. Search for: `Qwen2.5-Coder`
3. Choose model size based on your hardware:

**Recommended models**:

```
For most users (16GB RAM):
├─ Qwen/Qwen2.5-Coder-7B-Instruct-GGUF
└─ Choose: Q4_K_M variant (fastest, good quality)

For powerful machines (32GB+ RAM):
├─ Qwen/Qwen2.5-Coder-14B-Instruct-GGUF
└─ Choose: Q5_K_M variant (best quality)

For budget machines (8GB RAM):
├─ Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF
└─ Choose: Q4_K_M variant
```

4. Click **Download** button
5. Wait for download to complete (5-20 minutes depending on size)

**Time**: 5-20 minutes (depending on internet speed)

---

### Step 3: Test the Model

1. Click **"Chat"** tab
2. Select downloaded Qwen2.5-Coder model from dropdown
3. Click **"Load Model"**
4. Test with: `"Write a Python function to calculate fibonacci numbers"`

**Expected**: Fast, accurate code generation

**Time**: 1 minute

---

### Step 4: Enable Local Server (For MCP Integration)

1. In LM Studio, click **"Local Server"** tab
2. Click **"Start Server"**
3. Note the server URL: `http://localhost:1234`
4. Keep LM Studio running in background

**Time**: 30 seconds

---

### Step 5: Configure MCP Integration

**File**: `claude-code-mcp-config.json`

```json
{
  "mcpServers": {
    "lm-studio": {
      "command": "node",
      "args": [
        "C:\\Users\\SainathreddyDadiredd\\OneDrive - ERPA\\Claude\\projects\\mcp-servers\\lm-studio-mcp\\server.js"
      ],
      "env": {
        "LM_STUDIO_URL": "http://localhost:1234",
        "MODEL_NAME": "Qwen2.5-Coder-7B-Instruct"
      }
    }
  }
}
```

**Time**: 2 minutes

---

### Step 6: Create LM Studio MCP Server

We'll create a simple MCP server that connects Claude Code to LM Studio:

**File**: `projects/mcp-servers/lm-studio-mcp/server.js`

```javascript
#!/usr/bin/env node

/**
 * LM Studio MCP Server
 * Connects Claude Code to local LM Studio instance
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');
const axios = require('axios');

const LM_STUDIO_URL = process.env.LM_STUDIO_URL || 'http://localhost:1234';
const MODEL_NAME = process.env.MODEL_NAME || 'Qwen2.5-Coder-7B-Instruct';

class LMStudioServer {
  constructor() {
    this.server = new Server(
      {
        name: 'lm-studio',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();

    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'lm_studio_generate',
          description: 'Generate code or text using local LM Studio with Qwen2.5-Coder',
          inputSchema: {
            type: 'object',
            properties: {
              prompt: {
                type: 'string',
                description: 'The prompt to send to the model',
              },
              max_tokens: {
                type: 'number',
                description: 'Maximum tokens to generate (default: 2000)',
                default: 2000,
              },
              temperature: {
                type: 'number',
                description: 'Temperature for generation (0.0-1.0, default: 0.7)',
                default: 0.7,
              },
            },
            required: ['prompt'],
          },
        },
        {
          name: 'lm_studio_code_review',
          description: 'Review code using local LM Studio',
          inputSchema: {
            type: 'object',
            properties: {
              code: {
                type: 'string',
                description: 'Code to review',
              },
              language: {
                type: 'string',
                description: 'Programming language',
              },
            },
            required: ['code'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        if (name === 'lm_studio_generate') {
          return await this.generate(args.prompt, args.max_tokens, args.temperature);
        } else if (name === 'lm_studio_code_review') {
          const prompt = `Review the following ${args.language || ''} code and provide feedback:\n\n${args.code}\n\nProvide: 1) Issues found, 2) Suggestions, 3) Security concerns`;
          return await this.generate(prompt, 2000, 0.3);
        }

        throw new Error(`Unknown tool: ${name}`);
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  async generate(prompt, maxTokens = 2000, temperature = 0.7) {
    try {
      const response = await axios.post(`${LM_STUDIO_URL}/v1/chat/completions`, {
        model: MODEL_NAME,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: maxTokens,
        temperature: temperature,
      });

      const result = response.data.choices[0].message.content;

      return {
        content: [
          {
            type: 'text',
            text: result,
          },
        ],
      };
    } catch (error) {
      throw new Error(`LM Studio request failed: ${error.message}`);
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('LM Studio MCP server running on stdio');
  }
}

const server = new LMStudioServer();
server.run().catch(console.error);
```

**Time**: 5 minutes to create and test

---

## 🎯 Integration with Multi-AI Orchestration

### Updated AI Arsenal

```
Your Complete AI Team (All Free/Subscription):

1. Claude Code (Me) - Primary Implementation
   ├─ Claude Max subscription
   └─ Role: Orchestrator, implementation

2. Codex CLI - Deep Review & Architecture
   ├─ ChatGPT Pro subscription ($200/month)
   └─ Role: Code review, debugging

3. Gemini CLI - Large Context Analysis
   ├─ Gemini Pro subscription
   └─ Role: Codebase analysis, 2M context

4. LM Studio (Qwen2.5-Coder) - Local AI Worker ⭐ NEW
   ├─ Free, runs on your hardware
   ├─ No API costs, no subscription
   ├─ Privacy: Data never leaves your machine
   └─ Role: Background tasks, code generation, experimentation
```

---

## 🚀 Usage Patterns

### Pattern 1: Code Generation
**When**: Need quick code snippets, boilerplate, utilities
**Who**: LM Studio (Qwen2.5-Coder)
**Why**: Fast, free, good quality, no API usage

```bash
# In Claude Code session
I'll call LM Studio to generate the boilerplate code...
```

### Pattern 2: Code Review
**When**: Critical code, security concerns, production
**Who**: Codex CLI (GPT-5)
**Why**: Best quality, deep reasoning, worth the subscription usage

### Pattern 3: Large Codebase Analysis
**When**: Need to understand entire project structure
**Who**: Gemini CLI
**Why**: 2M token context window

### Pattern 4: Experimentation
**When**: Trying different approaches, prototyping
**Who**: LM Studio (Qwen2.5-Coder)
**Why**: Free, can iterate without limit

### Pattern 5: Security-Critical
**When**: Authentication, payment, data handling
**Who**: All four (Claude + Codex + Gemini + LM Studio)
**Why**: Multiple perspectives catch more issues

---

## 📈 Performance Comparison

| Metric | Claude Code | Codex GPT-5 | Gemini Pro | LM Studio Qwen2.5 |
|--------|-------------|-------------|------------|-------------------|
| **Speed** | Very Fast | Fast | Very Fast | Fast (depends on GPU) |
| **Quality** | Excellent | Excellent | Excellent | Very Good |
| **Context** | 200K tokens | ~128K tokens | 2M tokens | 128K tokens |
| **Cost** | Subscription | Subscription | Subscription | FREE ⭐ |
| **Privacy** | Cloud | Cloud | Cloud | LOCAL ⭐ |
| **Limits** | Unlimited | 300-1500/5hrs | 1000/day | UNLIMITED ⭐ |
| **Best For** | Implementation | Review | Analysis | Experiments |

---

## 🔧 Configuration Files

### File 1: `projects/mcp-servers/lm-studio-mcp/package.json`

```json
{
  "name": "lm-studio-mcp",
  "version": "1.0.0",
  "description": "MCP server for LM Studio integration",
  "main": "server.js",
  "type": "module",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.4",
    "axios": "^1.7.9"
  }
}
```

### File 2: Add to `CLAUDE.md`

```markdown
## LM Studio Integration (Local Free AI)
{{include: global-instructions/lm-studio-integration.md}}
```

---

## 🎯 Smart Routing Rules

**I (Claude) will automatically route to LM Studio when**:

✅ Generating boilerplate code
✅ Creating test data or mock objects
✅ Prototyping multiple approaches
✅ Converting between formats (JSON ↔ YAML, etc.)
✅ Generating documentation from code
✅ Simple refactoring tasks
✅ Code completion/suggestions
✅ Experimentation without API cost concerns

**I will NOT use LM Studio for**:
❌ Security-critical code (use Codex)
❌ Production deployment code (use Codex)
❌ Complex architecture decisions (use Codex)
❌ Large codebase analysis (use Gemini)
❌ Final production code (I handle it myself)

---

## 💡 Pro Tips

1. **Keep LM Studio Running**: Start server on Windows startup for instant access
2. **GPU Acceleration**: Enable NVIDIA GPU in LM Studio settings for 10x speed boost
3. **Model Selection**: Start with 7B model, upgrade to 14B if your hardware allows
4. **Memory Management**: Close other apps when running large models
5. **Parallel Execution**: LM Studio can run while Claude/Codex/Gemini work
6. **Privacy First**: Use LM Studio for sensitive code that can't go to cloud
7. **Cost Optimization**: Use LM Studio for high-volume tasks to save subscription limits

---

## 🚨 Troubleshooting

### Issue: LM Studio server won't start
**Solution**: Check if port 1234 is in use, change port in settings

### Issue: Model runs very slowly
**Solution**: Enable GPU acceleration in Settings > Hardware

### Issue: Out of memory errors
**Solution**: Use smaller model (1.5B instead of 7B) or close other apps

### Issue: MCP connection failed
**Solution**: Ensure LM Studio server is running before starting Claude Code

---

## 📚 Resources

**LM Studio**:
- Official Site: https://lmstudio.ai/
- Documentation: https://lmstudio.ai/docs
- Discord: https://discord.gg/lmstudio

**Qwen2.5-Coder**:
- Official Blog: https://qwenlm.github.io/blog/qwen2.5-coder/
- GitHub: https://github.com/QwenLM/Qwen2.5-Coder
- Hugging Face: https://huggingface.co/Qwen

---

## ✅ Setup Checklist

- [ ] Download and install LM Studio
- [ ] Download Qwen2.5-Coder model (7B recommended)
- [ ] Test model in LM Studio chat
- [ ] Start local server (port 1234)
- [ ] Create MCP server directory and files
- [ ] Install MCP server dependencies (`npm install`)
- [ ] Add to claude-code-mcp-config.json
- [ ] Restart Claude Code
- [ ] Test MCP integration
- [ ] Add to global instructions
- [ ] Update multi-AI orchestration rules

---

**Status**: Ready for implementation
**Estimated Setup Time**: 30-45 minutes (including model download)
**Monthly Cost**: $0 (completely free!)
**Privacy**: 100% local (data never leaves your machine)

🚀 **You now have FOUR AI systems working together: Claude + Codex + Gemini + LM Studio (Qwen2.5-Coder)!**
