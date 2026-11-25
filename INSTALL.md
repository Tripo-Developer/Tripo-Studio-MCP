# Install the Tripo Studio MCP Skill

Codex, Claude Code, and Cursor use the same Skill and references. To call Studio tools, also [connect Tripo Studio MCP and authorize your account](#connect-to-tripo-studio-mcp).

## Quick install with the Skills CLI

With Node.js 22.20 or later, run this from your project directory:

```sh
npx skills add Tripo-Developer/Tripo-Studio-MCP --skill tripo-studio-mcp
```

The CLI can detect your current agent. To target a specific client, add
`-a codex`, `-a claude-code`, or `-a cursor`. Install for the current
project, or add `-g` to install for your user account. Choose either
the Skills CLI or the native plugin for each client to avoid duplicate
Skill entries.

Open a new session and follow [Verify the Skill](#verify-the-skill).
Use `npx skills check` to check for updates and
`npx skills update tripo-studio-mcp` to apply them. Use
`npx skills remove tripo-studio-mcp` to uninstall, adding `-g` if installed globally.

The Skills CLI installs the instructions and references. Next, [connect Tripo
Studio MCP](#connect-to-tripo-studio-mcp) in your client and sign in.

## Codex

Run these commands in a terminal:

```sh
codex plugin marketplace add Tripo-Developer/Tripo-Studio-MCP
codex plugin add tripo-studio-mcp@tripo-studio
```

Open a new Codex session. To update, run `codex plugin marketplace upgrade tripo-studio`, then refresh the plugin in your client. To uninstall, run `codex plugin remove tripo-studio-mcp@tripo-studio`.

## Claude Code

Run these commands inside Claude Code:

```text
/plugin marketplace add Tripo-Developer/Tripo-Studio-MCP
/plugin install tripo-studio-mcp@tripo-studio
```

Use `/reload-plugins` or start a new session. To update, refresh the marketplace and update the plugin from `/plugin`. To uninstall, use `/plugin uninstall tripo-studio-mcp@tripo-studio`.

## Cursor

With local plugin imports enabled, clone the repository into Cursor's local plugin directory:

```sh
mkdir -p "$HOME/.cursor/plugins/local"
git clone https://github.com/Tripo-Developer/Tripo-Studio-MCP.git "$HOME/.cursor/plugins/local/tripo-studio-mcp"
```

Restart Cursor or run **Developer: Reload Window**, then open **Customize** and look for **Tripo Studio MCP**. To update, pull the checkout and reload Cursor. To uninstall, move the checkout out of the local plugin directory and reload.

For other compatible clients, install the entire [`skills/tripo-studio-mcp/`](skills/tripo-studio-mcp/) folder using the client's Skill installation instructions. Keep `SKILL.md` and `references/` together when installing or updating.

## Connect to Tripo Studio MCP

Set up the production connection for your client, then complete the Tripo sign-in in your browser. If you already have the production server configured, use its existing name to sign in again.

### Connect in Codex

```sh
codex mcp add tripo --url https://msapi.tripo3d.ai/mcp --oauth-client-id studio-codex
```

Complete the browser prompt. If the server is already configured or the browser does not open, run `codex mcp login tripo` using your connection name. Open a new Codex session after sign-in.

### Connect in Claude Code

```sh
claude mcp add --transport http --scope user --client-id studio-claude-code \
  --callback-port 3000 tripo https://msapi.tripo3d.ai/mcp
claude mcp login tripo
```

You can also open `/mcp` in Claude Code, select `tripo`, and follow the browser sign-in prompt.

### Connect in Cursor

Add the `tripo` entry to `~/.cursor/mcp.json` for all projects or to `.cursor/mcp.json` for the current project. Keep your other server entries.

```json
{
  "mcpServers": {
    "tripo": {
      "url": "https://msapi.tripo3d.ai/mcp",
      "auth": {
        "CLIENT_ID": "studio-cursor",
        "scopes": [
          "openid",
          "offline_access",
          "asset:read",
          "asset:download",
          "asset:upload",
          "asset:create",
          "asset:edit",
          "task:read",
          "task:cancel",
          "offline"
        ]
      }
    }
  }
}
```

In **Customize → MCPs**, select **Authenticate** or **Sign in** for `tripo`. After approving access in the browser, check that the connection is shown as **Connected**.

### Connect in Manus

Open **Plugins**, search for **Tripo AI**, and follow Manus's authorization prompts. This connects your Studio account through the Manus catalog.

## Verify the Skill

In a new conversation, ask: “Use the Tripo Studio MCP Skill and read its credit rules. What is the reference base cost for an HD text-to-model request?” The bundled reference should give 15 credits for the base operation before applicable add-ons. This check works without calling MCP.

## Verify the MCP connection

In a new conversation, ask the agent to use the connection you just authorized.

> Use the Tripo Studio MCP connection I just authorized. List up to two of my model assets and two of my recent model tasks. Use read-only tools only.

Use the actual tool results to confirm the connection. Empty lists are valid for a new account when both calls succeed.
