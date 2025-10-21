@echo off
echo Setting up MCP Environment Variables...

setx CONTEXT7_API_KEY "ctx7sk-9652306f-50bf-4085-b004-1591c0ac834e"
setx LIBRECHAT_API_KEY "your_librechat_api_key_here"
setx TAVILY_API_KEY "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"

echo Environment variables have been set.
echo Please restart Claude Code for the changes to take effect.
echo.
echo Note: Replace 'your_librechat_api_key_here' with your actual LibreChat API key.
echo Get API keys from:
echo - Context7: https://context7.com
echo - LibreChat: https://librechat.ai
echo - Tavily: https://tavily.com
pause