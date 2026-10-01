# Contributing

Keep the entrypoint concise and route detailed guidance to its owning reference. Preserve the user's app architecture, deployment targets, and product choices unless a requested change requires otherwise.

For a publication update, keep the version consistent in root `plugin.json`, both compatibility manifests, and the Claude marketplace entry. Keep OpenAI presentation metadata consistent between the portable manifest and its compatibility fallback. The package validator checks these relationships and that installed skills do not depend on files outside their own folder.

For a factual update, link current official documentation, a session timestamp, or an Apple staff reply with its correction history. Confirm symbol names, introduction versions, and platform availability in the selected SDK. Update the research date and source index for sources actually checked; don't mark an inaccessible source as read. Follow the [research maintenance rules](skills/apple-iphone-duo/references/sources.md).

Do not add copied session transcripts, Apple-bundled prompts, private documentation, or authenticated assets. Use original summaries and examples. Label unresolved reports and inference explicitly.

Run:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_package.py
./scripts/check_examples.sh
```

The compile check requires the Duo-supporting Xcode SDK and macOS. CI runs the portable audit tests and package validator; it does not pretend a hosted generic Xcode can exercise unreleased Duo hardware. Report actual device/simulator validation separately.

For substantial instruction changes, exercise the relevant scenarios in `tests/skill_evals.json` with only the skill and realistic app artifacts supplied to the evaluating agent. Inspect its result for actionable decisions, unsupported APIs, and scope drift. Add tests only for observable audit/tool/package contracts, not for exact headings, source inventories, or skill wording.
