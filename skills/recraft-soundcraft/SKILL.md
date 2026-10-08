---
name: recraft-soundcraft
description: "Use SoundCraft for multitrack audio editing, mixing, routing, automation, MIDI, sessions, and WAV/AIFF/FLAC bounce or stems. Trigger on SoundCraft or reCraft audio-production tasks; validate meters, playback, and exported duration."
---

# SoundCraft

Edit and render local audio sessions without disturbing audio devices or other running work.

## Target version and setup

Written for SoundCraft 0.3.0. Use the application already authorized for the current task; these templates neither install an app nor assume an operating system or installation directory. Read [the version-pinned command reference](references/cli-and-formats.md) before constructing commands. Upstream: https://github.com/storytold/soundcraft.

- Discover the CLI from `soundcraft-cli` on PATH, or set `SOUNDCRAFT_CLI` to its verified full executable path. On Windows, resolve the `.exe`; on other systems, use the available matching platform build. Resolve the GUI independently when it is needed.
- Confirm the application's actual version using its supported version/help output or release/package metadata. Do not assume every CLI supports `--version` or subcommand `--help`.
- Verify executable provenance and task permission before launch. Start with read-only command/schema discovery, then a tiny copied-file trial. Keep unrelated documents, processes, devices, and ports undisturbed.
- Do not configure persistent MCP access, download models or plugins, enable recording, overwrite originals, or transmit files merely because the skill describes those features.

Example discovery after those checks, in a shell appropriate to the host:

```sh
CLI="${SOUNDCRAFT_CLI:-$(command -v soundcraft-cli)}"
[ -n "$CLI" ] || { printf '%s\n' 'Set SOUNDCRAFT_CLI to the verified executable.' >&2; exit 1; }
"$CLI" commands
```

```powershell
$cli = $env:SOUNDCRAFT_CLI
if (-not $cli) { $cli = (Get-Command soundcraft-cli -ErrorAction Stop).Source }
& $cli commands
```

The command examples in the reference use synthetic relative filenames. Substitute real authorized inputs and distinct output destinations; never assume the example files exist.

## Workflow

1. Confirm source/session, sample rate, tempo/time signature, target loudness, channel layout, output bit depth, and whether recording or playback is requested.
2. Inspect session tracks/routing/commands, then apply changes to a copy. Avoid guessed plugin identifiers or implicit transport/record commands.
3. Test a short bounce and inspect meters/true peak/LUFS before a full mix or stem export.
4. Use GUI for detailed editing, MIDI/score work, routing, or listening. Recording/microphone permissions and new plug-ins require appropriate task authorization.
5. Before live control, verify that the process, document, and port belong to this task. Use this app's documented protocol, keep it on loopback, and obtain any required approval for persistent access.
6. Inspect each command result and save a new named output without unintended overwrite. Native commands differ in JSON/script syntax: consult the reference, not another reCraft app's flags.

## Verify and deliver

Reopen the session and listen to exported audio at a safe level. Check duration, sample rate, bit depth, channels, peaks/clipping, silence, synchronization, and requested loudness; verify all stems align and begin at the agreed origin.

Return the output path or approved attachment, changes made, and any warnings. Distinguish source-documented, execution-tested, and visually verified results. Exit code zero, a filename extension, and file existence alone do not establish correctness.

## Formats and limits

.scraft session plus Audio Files/ media. WAV/BWF/RF64, AIFF/AIFC, FLAC read/write; MP3/Ogg/AAC/ALAC/CAF and MP4/MOV audio inputs. MIDI import/export, MusicXML/score output. Bounce formats WAV/AIFF/FLAC.

Pre-alpha. Windows uses WASAPI; ALSA headers are Linux build requirements. Plug-in depth needs verification. Validate JSON before run/app because malformed JSON may silently become {}; script parsing fails explicitly. CLI convert chooses AIFF for .aif/.aiff, FLAC for .flac, and WAV for every other suffix.

Distinguish source-build dependencies from packaged-runtime requirements. Check the matching platform release and linked packaging documentation before installing extra dependencies.

## Example request

“Lower the demo Kick to -6 dB, bounce a new WAV, and inspect channel count, duration, and clipping.”

Target app version: SoundCraft 0.3.0. If the installed or globally available SoundCraft version is newer, check that application’s official repository documentation at https://github.com/storytold/soundcraft before relying on these commands.
