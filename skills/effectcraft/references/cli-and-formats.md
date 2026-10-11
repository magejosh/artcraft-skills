# EffectCraft 0.7.0: CLI and format reference

## Evidence and use

Commands and capability notes were reviewed against upstream tag v0.7.0, commit `813c7c4650f0d4c805da620c8d5837c9600ad2e3`, including the parser, command schemas and release changelog. These are source/documentation findings, not a guarantee of runtime or visual behavior on a particular machine. Recheck after upgrading; earlier-version smoke tests do not certify this release.

Bare `effectcraft-cli` and `effectcraft` names below are grammar shorthand. Resolve the CLI/GUI as described in SKILL.md, substitute authorized paths for the synthetic examples, and preserve source files. Windows portable packaging includes both executables with a statically linked C runtime; no Visual C++ redistributable is required. Rust 1.95+ is a source-build prerequisite, not a packaged-runtime dependency. No FFmpeg runtime is needed.

For JSON-bearing arguments, confirm native argument passing: Windows PowerShell 5.1 may strip literal quotes. Use verified native argument transport or the documented JavaScript script-file surface where appropriate; `run` takes command/JSON pairs, not a JSONL filename. Validate JSON before invocation and inspect received/resulting values.

## Supported command examples

```text
effectcraft-cli --version
effectcraft-cli commands --filter render.backend --schemas --json
effectcraft-cli commands --filter scriptui --schemas --json
effectcraft-cli exec render.backend --empty --json
effectcraft-cli info --project main.ecproj --json
effectcraft-cli props Main '#1' --project main.ecproj --json
effectcraft-cli set Main '#1' transform/position '[100,360]' --time 0 --project main.ecproj --save-as edited.ecproj
effectcraft-cli render-frame --project main.ecproj --comp Main --time 0 --out preview.png
effectcraft-cli render --project main.ecproj --comp Main --start 0 --end 1 --out preview.mp4
effectcraft-cli exec file.exportLottie '{"comp":"Main","path":"main.json"}' main.ecproj
effectcraft-cli script build.jsx --save-as main.ecproj
effectcraft --control 9877
effectcraft-cli mcp
effectcraft-cli mcp --gpu
effectcraft-cli mcp --bridge 9877
```

GPU and control examples are optional modes, not prerequisites or permission to enable persistent access. A sample/demo operation creates synthetic content, not a copy of a GUI project.

## Exact grammar and defaults

- `exec COMMAND --params JSON` and positional `exec COMMAND JSON` are supported. `run` takes COMMAND/JSON pairs. Discover accepted keys with `commands --schemas --json`; unknown command parameters are rejected.
- General CLI commands default to the demo unless `--project`, positional `.ecproj`, or `--empty` is supplied. JavaScript `script` and headless MCP default to an empty project. The GUI now starts empty too, unless `--demo` is requested.
- Full `render` still opens the demo when no project is supplied, even with `--empty`. Always pass `--project` for a real render. `--save` overwrites; `--save-as` preserves the source. Full render rejects `--bridge`; live rendering uses discovered `renderQueue.add`/`renderQueue.render` commands.
- Composition refs are IDs/names (`-` for active where supported); layers are IDs, names or `#n`, one-based from the top. Property paths come from `props`/`get_layer`, not guessed indexes. Times are seconds; keyframe times are layer time, which differs from composition time for offset/stretched layers.
- `render` supports start/end seconds, work area, frame rate, resolution, quality, channels, audio and codec-specific flags. `render-frame` makes one PNG; `--transparent` preserves alpha. Check output-module schemas and settings instead of inferring codec/alpha from an extension.
- JavaScript scripts use the documented After Effects-style object model. Script file/network access is constrained by the app's scripting preference; do not expand that permission as an incidental workaround.

Render output `--out` paths are relative to the working directory in this version. Use an explicit intended destination. MCP documents progress/cancellation and preserves unsaved bridge work across restart; inspect job/project state before retrying an ambiguous mutation.

## GPU diagnostics and 3D routing

`render.backend {}` reports `renderer`, `gpuAcceleration`, `adapter`, `active` (`gpu`/`cpu`) and `why` (a CPU reason or null). The project saying “Mercury GPU Acceleration” is not evidence that a GPU compositor is attached.

- Headless CLI and MCP default to CPU. `--gpu` attaches a headless GPU compositor and fails explicitly if no adapter is usable. A project set to software remains on CPU even with an adapter; changing `{backend:"gpu"}` is a project edit, not a read-only query.
- `comp.renderer {}` is a different setting: `classic3d` or `advanced3d`. `layer.newModel` and `layer.new3dPrimitive` automatically switch a Classic 3D comp to Advanced 3D in the same edit. Verify model visibility and the rest of the composition after that switch; switching back hides model layers.
- The release improves older-GPU startup, oversized-composition viewing and failed-window-start fallback to OpenGL. These are upstream fixes, not proof the current host works. Inspect backend diagnostics and a small render before a costly export; do not change OS/GPU settings blindly.

## Ease Presets and extensions

Ease Presets is now the bundled `extensions/scriptui-panels/Ease Presets.jsx` panel, opened from Window. The old `keys.easePreset.*` core API is not the current route. It applies curves to neighbouring selected keyframe pairs through the public scripting API, in one undo step. A single selected key is insufficient. Inspect the selected properties, curve and resulting motion.

Use `file.scripts.list` to discover scripts/panels and matching schemas for `scriptui.list`, `scriptui.get`, `scriptui.click`, `scriptui.set` and `scriptui.close`. Running scripts can edit the project; installing scripts/panels and saving/renaming/deleting user presets change persistent state. User presets now live in `script_settings.json`; settings loading migrates older `ease_presets.json` entries while preserving the old file. Treat that as an application settings change, not a read-only check.

WebAssembly effect extensions use `effect.plugins.load {path|folder}` and `effect.plugins.list`; After Effects native `.aex`/`.plugin` ABI binaries are unsupported. Script `.js`/`.jsx` support does not imply `.jsxbin` or ExtendScript preprocessor support. Confirm compatibility and task authorization before loading an extension.

## Formats and verification

Native `.ecproj` is versioned JSON. Lottie export uses `file.exportLottie`, not a render codec; `.lottie` creates a dotLottie archive. Inspect its `{path,bytes,warnings}` for unsupported effects, cameras/lights, audio or footage, then inspect player playback. AEP/AEPX import and native After Effects SDK plug-ins remain unsupported; a mentioned research candidate is not an implemented importer.

Documented media outputs include H.264, HEVC/AV1 MP4, ProRes MOV, WebM, GIF, image sequences including EXR, WAV and AIFF; inspect the exact preset/schema for profile, channels and alpha. Native `.prproj` is not an interchange format: timeline interchange uses FCP7 XML/FCPXML/OTIO/EDL/AAF/OMF and may prerender unsupported layers to adjacent ProRes files. Inspect missing-media and unsupported-feature reports before delivery. ML-assisted tools require optional model downloads; do not fetch them without task authorization.

Save/reopen the editable project. Compare representative frames, eased motion, shape/mask geometry, alpha and audio, then inspect the complete exported playback and actual render backend. Upstream documentation explicitly does not establish broad After Effects fidelity, especially across Windows/Linux GUI behavior.

## Live control and MCP

MCP starts empty unless `--project` or `--demo` is given. Bridge mode uses `--bridge PORT` or a supported address; do not mix it with `--project`/`--demo`. Verify the target session before mutation.

The control port is unauthenticated loopback JSON-lines, not HTTP. Enable it only for the task. Invalid/non-request input or lines over 4 MiB close the connection; at most 16 connections are served. Requests normally time out after 60 seconds. Inspect failure state before retrying a mutation; use supported job/queue state for long work. GUI fallback does not authorize disturbing an unrelated session.

## Changes and verification for 0.7.0

Ease Presets moved from core commands into a bundled ScriptUI extension. Scripts, panels and WebAssembly effects have distinct extension surfaces and side effects. Multilayer EXR, above-one floating-point values and OCIO handling improve; inspect channels, color transforms and rendered pixels on the intended project. This review does not include launching the application or executing these new workflows.

## Source links

- [Target-version release and changelog](https://github.com/storytold/effectcraft/releases/tag/v0.7.0)
- [CLI parser](https://github.com/storytold/effectcraft/blob/v0.7.0/apps/effectcraft-cli/src/main.rs)
- [Agent workflow and MCP](https://github.com/storytold/effectcraft/blob/v0.7.0/docs/agents.md)
- [Backend schema and diagnostics](https://github.com/storytold/effectcraft/blob/v0.7.0/crates/engine/src/commands/file.rs)
- [3D renderer commands](https://github.com/storytold/effectcraft/blob/v0.7.0/crates/engine/src/commands/model3d.rs)
- [Scripts, ScriptUI and effect extensions](https://github.com/storytold/effectcraft/blob/v0.7.0/docs/plugins.md)
- [Render queue schema](https://github.com/storytold/effectcraft/blob/v0.7.0/crates/engine/src/commands/render_queue.rs)
- [Control protocol](https://github.com/storytold/effectcraft/blob/v0.7.0/docs/control-protocol.md)
- [Formats and limitations](https://github.com/storytold/effectcraft/blob/v0.7.0/README.md) and [compatibility assessment](https://github.com/storytold/effectcraft/blob/v0.7.0/docs/gaps.md)
- [Windows packaging](https://github.com/storytold/effectcraft/blob/v0.7.0/packaging/windows/package.ps1)

No runtime helper scripts or executables are bundled with this skill.
