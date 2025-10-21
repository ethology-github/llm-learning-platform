# MCP 服务器设置指南

## 已安装的 MCP 服务器

### ✅ 正常运行的服务器

1. **GitHub MCP Server** - ✓ Connected
   - 功能：GitHub 仓库管理和 API 访问
   - 无需额外配置

2. **Context7 MCP Server** - ✓ Connected
   - 功能：高级上下文管理和知识库
   - 需要 API Key：设置环境变量 `CONTEXT7_API_KEY`
   - 获取 API Key：https://context7.com

3. **Sequential Thinking MCP Server** - ✓ Connected
   - 功能：结构化思考和问题解决
   - 无需额外配置

4. **Memory MCP Server** - ✓ Connected
   - 功能：持久化记忆和知识图谱
   - 无需额外配置


### ⚠️ 部分配置的服务器

1. **Tavily MCP Server** - ⚠️ 配置完成，需要重启
   - 功能：网络搜索和内容提取
   - API Key：已配置 `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`
   - 获取 API Key：https://tavily.com

2. **Context7 MCP Server** - ✅ 已配置
   - 功能：高级上下文管理和知识库
   - API Key：已配置 `ctx7sk-9652306f-50bf-4085-b004-1591c0ac834e`
   - 获取 API Key：https://context7.com

## 环境变量设置

### Windows 系统设置

1. **设置环境变量**：
   ```cmd
   set CONTEXT7_API_KEY=ctx7sk-9652306f-50bf-4085-b004-1591c0ac834e
   set LIBRECHAT_API_KEY=your_librechat_api_key_here
   set TAVILY_API_KEY=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
   ```

2. **或者永久设置**：
   - 右键"此电脑" → "属性" → "高级系统设置" → "环境变量"
   - 在"用户变量"中添加以上环境变量

3. **重启 Claude Code** 以使环境变量生效

## 可用功能

### GitHub 集成
- 访问 GitHub API
- 管理仓库
- 获取用户信息
- 创建和更新问题

### Context7 知识库
- 文档管理和检索
- 知识图谱构建
- 上下文增强

### Sequential Thinking
- 结构化思考过程
- 问题分解
- 决策分析

### Memory 系统
- 持久化记忆存储
- 知识图谱
- 上下文关联



## 故障排除

### 服务器连接问题
1. 检查网络连接
2. 验证 API Key 是否正确
3. 确保环境变量已设置
4. 重启 Claude Code

### 权限问题
某些服务器需要特定的 API 权限：
- 确保 API Key 有足够的权限
- 检查 API Key 是否过期

## 更多 MCP 服务器

如需添加更多 MCP 服务器，可以使用以下命令：
```bash
claude mcp add <server-name> <command>
```

示例：
```bash
claude mcp add filesystem "node ./filesystem-server.js"
```

## 更新和维护

定期更新 MCP 服务器：
```bash
npm update -g @modelcontextprotocol/server-*
npm update -g @upstash/context7-mcp
npm update -g tavily-mcp
```

## 支持

如有问题，请参考：
- Claude Code 文档：https://docs.anthropic.com/claude-code
- 各 MCP 服务器的 GitHub 仓库
- API 提供商的文档