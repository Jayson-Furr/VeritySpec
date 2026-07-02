# Post-Tag Release Verification

Use this artifact after a `v*` tag is pushed and the GitHub `Release`
workflow has finished. It turns the manual post-tag checks into one repeatable
evidence checklist for maintainers and AI agents.

This checklist does not enable PyPI publishing, change the release workflow, or
replace the release-prep checks in [release-checklist.md](release-checklist.md).
It records the evidence required after the public release exists.

## Setup

Run these commands from a clean checkout on `main` after the release tag has
been pushed. Replace `v0.79.0` only when verifying a different release.

```bash
REPO=Jason-Furr/verity-spec
TAG=v0.79.0
VERSION="${TAG#v}"
```

Confirm the local checkout is at the release commit and that the tag points at
`HEAD`:

```bash
git status --short --branch
git tag --points-at HEAD
git log --oneline -1
```

## 1. Release Workflow Evidence

Find the tag-triggered release workflow run:

```bash
gh run list \
  --workflow release.yml \
  --limit 20 \
  --json databaseId,headBranch,event,status,conclusion,url,displayTitle \
  --jq ".[] | select(.headBranch == \"$TAG\" and .event == \"push\")"
```

Record the run URL and inspect the jobs:

```bash
RUN_ID=$(gh run list \
  --workflow release.yml \
  --limit 20 \
  --json databaseId,headBranch,event,status,conclusion \
  --jq ".[] | select(.headBranch == \"$TAG\" and .event == \"push\") | .databaseId" \
  | head -n 1)

gh run view "$RUN_ID" \
  --json status,conclusion,jobs,url \
  --jq '{url, status, conclusion, jobs: [.jobs[] | {name, status, conclusion}]}'
```

Required evidence:

- The release workflow run exists for the intended tag.
- The workflow conclusion is `success`.
- The build job conclusion is `success`.
- The PyPI publish job is absent or skipped unless a maintainer explicitly ran
  the workflow with `publish_pypi=true`.

## 2. GitHub Release Asset Evidence

Verify that the public GitHub release exists and is not a draft or prerelease:

```bash
gh release view "$TAG" \
  --json tagName,url,isDraft,isPrerelease,targetCommitish,publishedAt,assets
```

Required evidence:

- `tagName` matches `TAG`.
- `isDraft` is `false`.
- `isPrerelease` is `false` unless the release was explicitly planned as a
  prerelease.
- The release includes both `verityspec-${VERSION}-py3-none-any.whl` and
  `verityspec-${VERSION}.tar.gz`.
- Each asset has a `sha256:` digest in the GitHub release metadata.

Download the public assets and compare their local hashes to the GitHub
release metadata:

```bash
ASSET_DIR="/tmp/verityspec-${VERSION}-release-assets"
rm -rf "$ASSET_DIR"
mkdir -p "$ASSET_DIR"
gh release download "$TAG" --dir "$ASSET_DIR"

gh release view "$TAG" \
  --json assets \
  --jq '.assets[] | [.name, .digest] | @tsv'

shasum -a 256 "$ASSET_DIR"/*
```

Required evidence:

- The downloaded wheel hash matches the GitHub release asset digest.
- The downloaded source distribution hash matches the GitHub release asset
  digest.

## 3. Downloaded Wheel Smoke Test

Install the downloaded wheel into a clean environment and run a minimal product
contract smoke test:

```bash
WHEEL_ENV="/tmp/verityspec-${VERSION}-release-wheel"
rm -rf "$WHEEL_ENV"
python3 -m venv "$WHEEL_ENV"
"$WHEEL_ENV/bin/python" -m pip install --upgrade pip
"$WHEEL_ENV/bin/pip" install "$ASSET_DIR/verityspec-${VERSION}-py3-none-any.whl"
"$WHEEL_ENV/bin/verity" --version
"$WHEEL_ENV/bin/verity" pack validate
"$WHEEL_ENV/bin/verity" validate examples/basic
```

Required evidence:

- `verity --version` reports the released version.
- Bundled pack validation passes.
- `examples/basic` validates with the released wheel.

## 4. Public GitHub Tag Install Smoke Test

Install from the public GitHub tag into a second clean environment. This catches
tag drift even when the uploaded wheel is valid:

```bash
GITHUB_ENV="/tmp/verityspec-${VERSION}-github-install"
rm -rf "$GITHUB_ENV"
python3 -m venv "$GITHUB_ENV"
"$GITHUB_ENV/bin/python" -m pip install --upgrade pip
"$GITHUB_ENV/bin/pip" install "verityspec @ git+https://github.com/$REPO.git@$TAG"
"$GITHUB_ENV/bin/verity" --version
"$GITHUB_ENV/bin/verity" pack validate
"$GITHUB_ENV/bin/verity" validate examples/basic
```

Required evidence:

- The install resolves from the intended public tag.
- The installed package reports the released version.
- Bundled pack validation passes.
- `examples/basic` validates from the tag install.

## 5. Milestone And Issue Closure Evidence

After the release artifacts and install paths are verified, confirm that the
release issue and sprint issue are closed, then close the milestone:

```bash
gh issue list --milestone "$TAG" --state all --json number,title,state,url

MILESTONE_NUMBER=$(gh api "repos/$REPO/milestones?state=open" \
  --jq ".[] | select(.title == \"$TAG\") | .number")

gh api -X PATCH "repos/$REPO/milestones/$MILESTONE_NUMBER" \
  -f state=closed \
  --jq '{number,title,state,open_issues,closed_issues}'
```

Required evidence:

- Sprint and release issues for the milestone are closed.
- The milestone has zero open issues.
- The milestone state is `closed`.

## 6. Final Repository And Agent Evidence

Finish by confirming that the repository is clean, no release PR remains open,
and the AI-agent context has been refreshed:

```bash
git status --short --branch
gh pr list --state open --json number,title,headRefName,url
sed -n '1,260p' AGENTS.md
git log --oneline -3
```

Required evidence:

- Local `main` matches `origin/main`.
- No release or sprint PR remains open.
- AGENTS.md has been reread after the release commit and tag.
- The latest commit is the release-prep merge commit.

## CI Outage Fallback

If GitHub checks cannot run because of billing, credits, quota, runner
availability, or another platform issue, run the equivalent local release
checks from [release-checklist.md](release-checklist.md), record the external
CI reason in the issue or PR, and continue from the local evidence.

Do not use this fallback for normal test failures.

## Evidence Summary Template

Use this summary in the release issue, PR, or work ledger:

```text
Release tag:
Release workflow URL:
Release workflow conclusion:
PyPI publish state:
GitHub release URL:
Wheel asset hash:
Source asset hash:
Downloaded wheel smoke:
Public GitHub tag install smoke:
Closed issues:
Closed milestone:
Main CI URL:
Agent context refreshed:
Follow-ups:
```
