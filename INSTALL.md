# Install the Tripo Studio MCP Skill

The plugin uses the same Skill and references on all three clients. Connect Tripo Studio MCP and authorize your account separately if you want to call its tools.

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

## Verify the Skill

In a new conversation, ask: “Use the Tripo Studio MCP Skill and read its credit rules. What is the reference base cost for an HD text-to-model request?” The bundled reference should give 15 credits for the base operation before applicable add-ons. This check works without calling MCP.

After configuring MCP and signing in, ask the agent to list your five most recent model assets. An empty list can be a successful result for a new account.

For other compatible clients, install the entire [`skills/tripo-studio-mcp/`](skills/tripo-studio-mcp/) folder using the client's Skill installation instructions. Keep `SKILL.md` and `references/` together when installing or updating.
