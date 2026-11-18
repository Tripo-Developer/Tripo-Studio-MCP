# Tripo Studio MCP Skill

Use this Skill with a local agent such as Codex or Claude Code to create and edit 3D models, work with textures and motion, track tasks, and retrieve results through Tripo Studio MCP.

## Install

1. Download or clone this repository.
2. Install the entire [`skills/tripo-studio-mcp/`](skills/tripo-studio-mcp/) folder using your agent client's Skill installation instructions. Keep [`SKILL.md`](skills/tripo-studio-mcp/SKILL.md) and [`references/`](skills/tripo-studio-mcp/references/) together.
3. Connect Tripo Studio MCP in your client and sign in with your Tripo account. Verify the connection by asking the agent to list your model assets.

## Try it

Start with a read-only request:

> Use Tripo Studio MCP to list my five most recent model assets.

To create a model, try:

> Use Tripo Studio MCP to generate a textured 3D model of a small toy robot with a rounded white body, orange joints, and blue glowing eyes. Show the full body in a standing pose. Give me the model link when it is ready.

Generation and editing may use credits. See [credit rules](skills/tripo-studio-mcp/references/credit-rules.md) for reference costs and [Tripo Studio](https://studio.tripo3d.ai/) for current plan terms and account allowances.

Skill updates are reviewed through pull requests. Reinstall or update the entire Skill folder to get the latest instructions and references together.
