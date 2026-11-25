# Tripo Studio MCP

Create 3D models from text or images with Tripo Studio in Codex, Claude Code, or Cursor. The Skill guides your agent through generation, editing, and export. Connect to Tripo Studio MCP and sign in to run those workflows with your Studio account.

## What you can do

- **Generate 3D models** from a text prompt, a single reference image, or multiple views.
- **Refine geometry and materials** with texturing, UV unwrapping, remeshing, and part editing.
- **Rig and animate** models with generated or preset motions.
- **Track and deliver assets** by checking task status, retrieving previews and downloads, and importing or exporting files for game, animation, and design workflows.

Generation and editing depend on your Studio account permissions and available credits. See the [credit rules](skills/tripo-studio-mcp/references/credit-rules.md) for reference costs.

## Quick start

1. **Install the Skill** from your project directory.

   ```sh
   npx skills add Tripo-Developer/Tripo-Studio-MCP --skill tripo-studio-mcp
   ```

   To target a specific client, add `-a codex`, `-a claude-code`, or `-a cursor`. The [installation guide](INSTALL.md) also covers native plugins, manual installation, and updates.

2. **Connect to Tripo Studio MCP** in your client and authorize your account. Start at [Tripo Studio MCP setup](https://studio.tripo3d.ai/mcp).

3. **Verify the connection** in a new conversation with a read-only request.

   > Use Tripo Studio MCP to list my five most recent model assets.

   An empty list is a successful result for an account with no models.

## Try your first model

> Create a 3D toy robot with a white body, orange joints, and blue eyes. Apply textures and show me the finished model preview.

You can also attach an image and ask the agent to turn it into a textured 3D model.

## Support

- For Skill installation, documentation, or plugin discovery issues, open a [GitHub issue](https://github.com/Tripo-Developer/Tripo-Studio-MCP/issues). Include your client version, installation method, and error message. Keep tokens, signed download links, and private assets out of public issues.
- For sign-in, account, credit, or task issues, contact [Tripo support](mailto:support@tripo3d.ai). Include the task ID or error code if available.
