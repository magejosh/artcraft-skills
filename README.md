# ArtCraft Skills

Give your AI assistant practical instructions for working with creative and productivity apps. These skills help it choose the right commands, preserve editable files, and check the result before handing it back to you.

Each app has its own skill folder, with a `SKILL.md` guide and a detailed command reference. You can use one skill or the whole collection.

## What you can do

- Edit documents, spreadsheets, and presentations while preserving their structure
- Work with drawings, photos, vector artwork, and page layouts
- Inspect and export video, animation, audio, and PDFs
- Avoid app-specific command mistakes and understand format limitations

## Included skills

| Skill | Helps with | Written for |
| --- | --- | --- |
| [CADCraft](skills/cadcraft/SKILL.md) | 2D drawings, CAD conversion, layers, and dimensions | 0.5.0 |
| [DeckCraft](skills/deckcraft/SKILL.md) | Presentations, slide layouts, and slide exports | 0.5.0 |
| [DesignCraft](skills/designcraft/SKILL.md) | Page layouts, publications, and text flow | 0.6.0 |
| [EffectCraft](skills/effectcraft/SKILL.md) | Motion graphics, compositions, and animation | 0.7.0 |
| [FilmCraft](skills/filmcraft/SKILL.md) | Video timelines, captions, and exports | 0.6.0 |
| [GridCraft](skills/gridcraft/SKILL.md) | Spreadsheets, formulas, charts, and print output | 0.5.0 |
| [LightCraft](skills/lightcraft/SKILL.md) | Photo development, culling, and batch exports | 0.6.0 |
| [PDFCraft](skills/pdfcraft/SKILL.md) | PDF inspection, page organization, annotations, and forms | 0.6.0 |
| [PhotoCraft](skills/photocraft/SKILL.md) | Layered image editing, masks, and adjustments | 0.6.0 |
| [SoundCraft](skills/soundcraft/SKILL.md) | Audio sessions, mixing, and rendering | 0.5.0 |
| [VectorCraft](skills/vectorcraft/SKILL.md) | Vector artwork, paths, and artboards | 0.9.0 |
| [WordCraft](skills/wordcraft/SKILL.md) | Documents, styles, tracked changes, and conversion | 0.5.0 |

PDFCraft was previously named PrintCraft. This collection uses the updated [PDFCraft 0.6.0](https://github.com/storytold/pdfcraft) skill.

The versions above identify the app releases these guides were written for. If you have a newer release, the skill points your assistant to that app's official documentation before it uses older commands.

## How to use them

You'll need an assistant that supports skills or can read local instruction files, plus the app installed in an environment the assistant can access. This repository contains instructions, not app installers.

1. Download or clone this repository.
2. Choose the app folder under `skills/`, such as `skills/cadcraft`.
3. Import the entire folder using your assistant's skill-installation workflow, or copy it into that assistant's configured skill directory. Keep the `references` folder with it. If a same-named skill already exists, compare the two before replacing anything.
4. Ask your assistant to use the skill and give it the files or task you want help with.

You can also use a skill without installing it: tell your assistant to read its `SKILL.md` file for the task.

For example:

> Use cadcraft to inspect drawing.dxf, preserve its units and layers, and save a separate SVG preview.

> Use gridcraft to inspect the formulas in budget.xlsx and verify the totals after saving an edited copy.

> Use pdfcraft to extract pages 1, 3, and 5 into a separate PDF and check the page order.

Replace those example filenames with your own files. The skills use portable command discovery rather than assuming a particular installation folder or operating system.

## Check for app updates

Run the read-only release checker with Python 3.9 or newer:

```sh
python3 tools/update_check.py
```

On Windows, use `py -3 tools/update_check.py`. It compares the twelve versions in `skills.json` with the latest stable releases in their official GitHub repositories and shows release and portable-download links. It reports failures as unknown rather than claiming you are up to date.

The baseline is the version each skill was written for, not a scan of the apps installed on your computer. The checker does not download packages, install apps, or change skills. When you decide to update an app, keep the new portable version alongside the existing version until you choose to remove the old copy.

## What to expect

The guides include version-specific source references and practical verification steps. CLI smoke-test coverage varies by app and is recorded in [TESTING.md](TESTING.md). It does not guarantee every feature, file format, or platform combination. Keep an original copy of important files and review converted outputs, especially complex documents or media projects.

For contributors, [AGENTS.md](AGENTS.md) explains the repository conventions and [TESTING.md](TESTING.md) covers the optional checks used to maintain the collection. You do not need to run these checks to use a skill.

## Licensing

No license has been selected for these templates. The upstream applications and documentation retain their own licenses. App binaries, fonts, models, and icons are not included here.
