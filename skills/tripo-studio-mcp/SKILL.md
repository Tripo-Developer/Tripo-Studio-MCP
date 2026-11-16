---
name: tripo-studio-mcp
description: Use the connected Tripo Studio MCP to create 3D models from text or images, edit geometry and materials, rig or animate models, import or export files, and track or recover Tripo tasks. Use when the user asks for these workflows in Tripo Studio.
---

# Tripo Studio MCP

Use the connected tool catalogue for current fields and supported options. Preserve the user's intended output, topology, limits, and exact prompt text.

**Set the stop point before the first call.** If the user asks to check the
original task when submission hits a blocker, the original lookup is the
last call in that branch. Reply from that response, including when its
status is pending. If the user requests only a retargeted clip name, reply
from the successful task's `retarget_result.animation_clip` without an
asset lookup.

**Get model downloads from the result asset.** After model creation or edit,
use the successful task's `model_ids` with `tripo_get_model_asset`, then give
the returned `model_url`. A request for a download link alone ends there.
Call `tripo_export_model` only for an explicit export or a requested format
change after checking the existing result.

**End recovery replies at the last verified fact.** Use these reply patterns
in the user's language and end the reply after the matching one:

| Observed state | Reply |
| --- | --- |
| Prior submission is uncertain and both identifiers are missing | Ask for only the original task ID or idempotency key. In Chinese: 请提供原任务 ID 或原始幂等键，我先核对原任务。 |
| Error action is `wait_for_service` | Report the dependency blocker. In Chinese: 服务依赖未就绪，本次操作已停止。 |
| Original-key lookup returns `found: false` | Report the known blocker, lookup result, and uncertainty. For a download quota blocker: 下载额度不足。原任务未找到，提交是否受理尚未确认。 |

End these replies without offers, troubleshooting steps, or conditional advice
to submit again. A negative lookup leaves both task creation and charging
unconfirmed.

Build arguments afresh for each call. Send `model_version` only for text,
single-image, and multiview modeling. Omit unspecified optional fields. A
white model uses `texture: false` with `pbr`, `texture_quality`, and `delight`
omitted. For explicit triangles send `quad: false`, and for explicit quads
send `quad: true` on supported versions. Submit each write once with a
stable `idempotency_key`. Save the exact creating tool name and key for
[recovery](references/recovery.md).

## Decide before calling

**Choose the first call from the request.**
- A new operation on a supplied image or model ID starts with the requested
  write. Skip source asset reads and list calls when all required inputs are
  known. The server checks ownership and asset eligibility during the write.
  This applies to image preprocessing, image-to-model, segmentation, UV, PBR,
  rigging, retargeting with known inputs, and export. When the modeling or
  texturing tool requires an upload and the supplied image was generated,
  [prepare the upload first](references/generation.md#use-generated-images-as-model-inputs).
  For a known generated image, or after the adapter requests re-upload, ask
  for an uploaded `object_key` if the host cannot transfer the bytes.
  “Existing” or “delivered” alone leaves the image origin unknown. Send the
  supplied `image_id` and use the adapter response to decide whether to upload.
- Read the source first when the user requests verification or the operation
  needs an unverified fact, such as the authoritative part names for completion.
- Multiview modeling requires a front view and at least one other view. If
  the user says either is unavailable, ask for it and pause. Search only if
  they ask you to find a candidate.
- A prior submission with an uncertain result starts with the original key or
  task ID. A conditional request to check after a disconnect still starts with
  the new operation, then switches to recovery if the disconnect occurs.

**Follow asynchronous work by task ID.** Poll `tripo_get_model_task` or
`tripo_get_image_task` for state and result IDs. Use progress endpoints for
explicit percentage requests while work is pending. If the user wants only
submission, return the accepted task ID without polling. After a terminal result,
stop polling and read only the requested deliverable. A pending task
at 100% is still pending. For recovery-only
requests, return the task ID and status already in the lookup response.
If both identifiers are missing, use the recovery reply table above. Broad
task lists cannot establish which write was accepted. When the user asks
only to be told about a blocker, report the blocker and end without
suggesting a new attempt. Follow the error's `action`: `recover_task` calls the
recovery tool. `wait_for_service` reports the dependency failure and stops
even if the response includes a recovery tool name. An original task
lookup returning `found: false` establishes neither absence of a task
nor whether a charge occurred.

When completing parts, a successful asset read with `parts_known: false`
blocks the operation. Report the missing catalogue and stop. Re-reading the
same asset, checking its old task, or using client-side node names cannot
establish the trusted catalogue.

For a part edit that starts with a requested source inspection, use two
labelled lines when reporting success: **Edited model** with its ID and
link, and **Original model inspected** with its ID and link if returned.
Omit the original line if the user explicitly asks to see only the edited
result. A result with `parts_known: false` gives no information about
whether it has parts.

Copy asset IDs, task IDs, preset IDs, and full URLs verbatim from their
source. Before replying, verify the full signed URL and identifiers against
the corresponding tool result. When the user supplies exact prompt text,
pass it as written, including the text for each motion segment.
Answer in the user's language.
If the user says the asset is private to another account and they lack
permission, explain the permission limit without looking it up.

**An uploaded model key (for example, `uploads/models/…`) is ready to import.**
Pass it as `resource_key` to `tripo_import_model`. Do not open it as a local file,
request another upload, or search for a substitute asset. Follow the import
task; if it fails, stop any requested conversion and report the import failure.

## Chain completed results

Use the new result ID at each step and stop dependent writes after a failed
or unresolved prerequisite. Deliver an existing link if it meets the
request. Export for an explicit export request or a requested format change.

- **Four views:** Match each delivered asset to `front`, `left`, `right`,
  or `back` by `result_key`. Pause for missing or contradictory views. If
  the user already reports a mismatch and asks for advice, cite the labels
  and task ID and ask for corrected inputs or a verified mapping without
  calling a tool. Check upload requirements before using generated views.
- **Parts:** If the user asks to split a model, deliver the segmentation
  result. Only call `tripo_complete_model` when the user explicitly asks to
  fill missing geometry. Use the new model's trusted part catalogue when
  chaining those two operations.
- **Rig and animate:** Rigging for Mixamo or Unity selects a skeleton
  `spec`. Retarget with the new rigged model ID after a rigging step.
  Send both `motion_id` and `motion_source`. Use `preset` for a full
  preset ID, including its prefix, and `user_generated` for a motion asset ID.
- **Existing file:** Read the asset for its current link. See the delivery
  reference for export presets and exact format settings.

Read only the reference needed for the task:

| Goal | Reference |
| --- | --- |
| Text, single-image, multiview modeling or image preprocessing | [Generation](references/generation.md) |
| Geometry, materials, rigging or animation | [Model processing](references/model-processing.md) |
| Upload, model import, export, delivery, or a GLB the target app cannot open | [Delivery](references/delivery.md) |
| Polling, timeouts, task errors, cancellation, or where to get help | [Recovery](references/recovery.md) |
