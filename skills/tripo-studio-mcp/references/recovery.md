# Track and recover work

- Save the creating tool name, original client `idempotency_key`, and any returned `task_id`. Reusing the key within the same account and tool identifies the first accepted task. Use a new key only for a deliberately new operation.
- When the task ID is known, read `tripo_get_model_task` for model, import, motion, or export tasks, and `tripo_get_image_task` for image tasks. Treat `admitting`, `accept`, `submit`, and `finalizing` as pending. A progress percentage alone cannot establish success. Allow an interval between reads and back off within the user's wait budget. At the limit, return the ID and last observed status so work can resume.
- When submission times out or returns an unclear result without a task ID, query `tripo_get_model_task_by_idempotency_key` or `tripo_get_image_task_by_idempotency_key` with the original `{creation_tool, idempotency_key}`. Use the full MCP tool name (for example, `tripo_image_to_model`). If the user only asks whether the task exists, report the lookup result and stop. If the user asks to finish or deliver the work, follow the recovered task ID when `found=true`. If `found=false`, give the terminal reply in [the Skill](../SKILL.md) and stop. If the lookup is unavailable, report that recovery is unresolved and stop further submissions for that intent.
- If the original key and task ID are missing, check the host’s available execution history or ask for one of them. Inspect any prior response for typed fields. For a known `image_id`, `tripo_get_image_asset` can identify the originating image task via `source_task_id`. Recover the timed-out model operation using its own task ID or key. A generic preview ID provides neither.
- On `success`, read the corresponding result as described in [Delivery](delivery.md). For `fail`, `expire`, or `cancel`, report the observed terminal state and any useful safe error. Treat unfamiliar statuses as unresolved.
- Inspect MCP `isError` even on HTTP 200. When the error includes `action: recover_task`, follow its `recovery_tool` and original key or task ID, including on a reservation failure that may already have created a task. A temporary read failure may be retried within the wait budget. On a definite input, permission, entitlement, or capability rejection, explain what is missing.
- If the user wants to cancel and the server offers `tripo_cancel_model_task`, use the original task ID and read the returned state. If the cancel response is unclear, check the task again. Report billing or refund information only when independently confirmed.

## Help and support

When the user asks for help, explain what you observed and offer the most
relevant resource. A recovery result of `found=false` takes the terminal
reply above and ends that operation before this help flow.

- For instructions on Studio features and workflows, point to the [Tripo Studio product documentation](https://www.tripo3d.ai/product-doc).
- For troubleshooting, account access, credits, subscriptions, or plugin questions, point to the [Tripo Help Center](https://www.tripo3d.ai/help).
- If the problem persists or needs account-specific investigation, offer [Tripo User Support](mailto:support@tripo3d.ai). Suggest including a short description, the time and time zone, and the task ID or error code if available. Keep tokens, signed links, and private assets out of the suggested email.
