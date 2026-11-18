# Tripo Studio MCP Skill

Install this Skill in Codex, Claude Code, or Cursor to guide your agent through 3D generation, model editing, motion, and asset delivery with Tripo Studio MCP.

For a quick project-level install, run:

```sh
npx skills add Tripo-Developer/Tripo-Studio-MCP --skill tripo-studio-mcp
```

Add `-a codex`, `-a claude-code`, or `-a cursor` to select a client explicitly. For native plugins, use the client-specific paths below.

| Client | Install |
| --- | --- |
| Codex | Add the GitHub marketplace and install `tripo-studio-mcp`. |
| Claude Code | Add the GitHub marketplace and install `tripo-studio-mcp`. |
| Cursor | Load the plugin from a local checkout. |

See [installation and updates](INSTALL.md) for commands and a manual Skill installation option. The package includes the Skill and its references. Configure the Tripo Studio MCP connection and sign in separately through your client.

After connecting, try: “Use Tripo Studio MCP to list my five most recent model assets.”

For a first creation, ask for a textured toy robot with a white body, orange joints, and blue eyes. Generation and editing may use credits. See the [credit rules](skills/tripo-studio-mcp/references/credit-rules.md) for reference costs.
