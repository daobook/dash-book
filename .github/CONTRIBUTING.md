# Development Conventions

Welcome to the Executable Book Project (EBP)!
We're excited you're here and want to contribute 🎉.

This page outlines conventions and best practices for development and maintenance across all repositories in the EBP organisation, to help the community make the best tools possible.

>  **These are guidelines, not rules** 💡
>
> This page is meant to help you make your contribution as efficient and helpful as possible, not to lay down strict rules that must be followed at all times. We think these are reasonable patterns to follow, and the EBP tries to follow them as much as it can. But if you prefer to do things otherwise, that is usually just fine 👍.

Thank you for you interest in contributing ✨

## Table of contents

  - [Code of Conduct](#code-of-conduct)
  - [Questions or Feedback](#questions-or-feedback)
  - [Structure of EBP Repositories](#structure-of-ebp-repositories)
  - [Design Philosophy](#design-philosophy)
  - [Coding Style](#coding-style)
  - [Naming Conventions](#naming-conventions)
  - [Testing](#testing)
  - [Documentation](#documentation)
  - [Git Branches](#git-branches)
  - [Opening a Pull Request](#opening-a-pull-request)
  - [Pull Request Reviews](#pull-request-reviews)
    - [Sources](#sources)
    - [Standards](#standards)
    - [Check-list - What to look for](#check-list---what-to-look-for)
  - [Merging Pull Requests](#merging-pull-requests)
  - [Commit Messages](#commit-messages)
  - [Releases and Change-logs](#releases-and-change-logs)
    - [The process of creating a release](#the-process-of-creating-a-release)
  - [Deprecations](#deprecations)

## Code of Conduct

This project and everyone participating in it is governed by the [EBP Code of Conduct](https://github.com/executablebooks/.github/blob/master/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [executablebooks@gmail.com](mailto:executablebooks@gmail.com).

## Questions or feedback

The Executable Books Project uses [a GitHub discussion board](https://github.com/executablebooks/meta/discussions) for community questions, discussion, and assistance. Please join in here: <https://github.com/executablebooks/meta/discussions>

Additionally, if you would like to see a new feature implemented, see our [Feature Voting page](https://executablebooks.org/en/latest/feature-vote.html).

## Structure of EBP repositories

For EBP's overarching goals and principles, see: <https://executablebooks.org>

EBP is a large open source project; it's made up of numerous packages, in to keep individual components modular and reusable by others.
When you initially consider contributing to EBP, you might be unsure about which of those repositories implements the functionality you want to change or report a bug for. This section should help you with that.

Here's a list of the big ones:

- [markdown-it-py](https://github.com/executablebooks/markdown-it-py) is our Markdown parser. It is a Python port of the very popular [markdown-it](https://github.com/markdown-it/markdown-it) package, which is CommonMark compliant, fast and extensible.
- [MyST-Parser](https://github.com/executablebooks/MyST-Parser) is a bridge between markdown-it-py and [sphinx](https://github.com/sphinx-doc/sphinx). It calls markdown-it-py on Markdown files and converts the parsing tokens created to the docutils Abstact Syntax Tree (AST) used internally by sphinx.
- [MyST-NB](https://github.com/executablebooks/MyST-NB) builds on MyST-Parser to allow parsing and execution of [Jupyter Notebooks](https://jupyter.org/) and their [text-based representation](https://myst-nb.readthedocs.io/en/latest/use/markdown.html).
- [jupyter-cache](https://github.com/executablebooks/jupyter-cache) is used by MyST-NB to execute notebooks and cache their results, such that they are only re-excuted during documentation builds when code cells change.
- [sphinx-book-theme](https://github.com/executablebooks/sphinx-book-theme) is a sphinx HTML theme, designed to be optimal for the presentation of executable books.
- [sphinx-copybutton](https://github.com/executablebooks/sphinx-copybutton), [sphinx-togglebutton](https://github.com/executablebooks/sphinx-togglebutton), [sphinx-panels](https://github.com/executablebooks/sphinx-panels) and [sphinx-thebe](https://github.com/executablebooks/sphinx-thebe) provide sphinx extensions to allow the inclusion of special features in the documentation.
- [jupyter-book](https://github.com/executablebooks/jupyter-book) provides a user-friendly interface for building beautiful, publication-quality books and documents, utlising the above components.
- [myst-language-support](https://github.com/executablebooks/myst-language-support) provides  aTextmate grammar, and VS Code extension, for editing MyST markdown.

Below is documentation of conventions which are applicable to all repositories, but also individual repositories may contain additional contributing guides for that particular code base. 

(dev/design-philosophy)=

## Design Philosophy

There are few high-level principles that this project tries to follow in making
both technical and community decisions. They goals to shoot for, and may not all
be followed perfectly all the time. Here are a few of those principles:

- **Document first** - When deciding whether or not a new feature is needed, first
  consider whether improving documentation could solve the same problem for others.
  New features (and especially new APIs) are costly to develop and maintain. Sometimes
  it's better to show people how to manually do a complex thing via the documentation,
  rather than extending the API. If new features/API are needed, make sure this avenue
  has been exhausted first so the decision is intentional.
- **Standardize developer practices**. We should keep developer/release/community
  practices consistent across all of the EBP repositories. Where possible, share
  infrastructure and documentation between them (like this page!). Keep the same
  level of quality control across all core repositories, regardless of how small
  they are.
- **Keep the semantic document model consistent**. There are a few places where
  markdown syntax / file structure maps on to the structure of a book. The two
  most obviously places this happens are in the Jupyter Book `_toc.yml` file and in
  the underlying Sphinx `toctree` structures. These two models should closely resemble
  one another. Try not to include user-facing structures (e.g., in `_toc.yml` that
  must be translated to a *different* document structure in Sphinx).
- **Release early and often**. We should emphasize smaller, more iterative releases
  over large and complex ones. This keeps our documentation in-line with the latest
  releases and also minimizes the disruption (and subsequent maintenance burden)
  associated with big changes. The [process for creating a release](#releases-and-change-logs)
  is relatively simple and quick, so don't hesitate to release patch versions (or minor
  versions) as appropriate.

(dev/code_style)=

## Coding Style

Coding style is largely enforced automatically, using [pre-commit hooks](https://pre-commit.com/).
For Python packages, the pre-commit should include automated code formatting *via* [Black](https://black.readthedocs.io/) and code linting *via* [flake8](https://flake8.pycqa.org).

(dev/naming_conventions)=

## Naming Conventions

The following naming conventions should be used

**Directives:**

Directives should have names that are:

1. Short, concise and descriptive
2. Use '-' to join words together

For example a directive for evaluating `rst` syntax might be named `eval-rst` which would be used in
a document using the [directive syntax](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#directives-a-block-level-extension-point).

````
```{eval-rst}
<rst>
```
````

(dev/testing)=

## Testing

All packages should contain a test infrastructure, usually automated for PRs and commits *via* [GitHub Actions workflows](https://docs.github.com/en/actions/configuring-and-managing-workflows/configuring-a-workflow).

Testing philosophy:

- Whenever you encounter a bug, add a (failing) test for it. Then fix the bug.
- Whenever you modify or add a feature, write a test for it!
  Writing tests [before writing the actual implementation](http://en.wikipedia.org/wiki/Test_Driven_Development) helps keeping your API clean.
- Make [unit tests](https://en.wikipedia.org/wiki/Software_testing#Testing_levels) as atomic as possible. A unit test should run in the blink of an eye.
- Document why you wrote your test - developers will thank you for it once it fails.

For Python packages, the test infrastructure should be implemented *via* [pytest](https://docs.pytest.org).

(dev/docs)=

## Documentation

A minimal description of the project should be contained in the README.md, then most documentation should generally be contained in a `docs` folder, using [Sphinx](http://www.sphinx-doc.org) (directly or *via* jupyter book) as the documentation generator.

Markdown style should generally follow that rules outlined in [markdownlint](https://github.com/markdownlint/markdownlint) and rST should similarly follow [rstcheck](https://github.com/myint/rstcheck), either of which may be added to the pre-commit configuration.

In addition, when writing documentation authors should adhere to the following guidelines:

1. Write **one sentence per line** and otherwise **no manual line wrapping** to make easy to create and review  diffs. All standard editors allow for dynamic line wrapping, and the line length is irrelevant for the rendered documentation in, e.g., HTML or PDF format.
2. **File and directory names should be alphanumeric** and all lower-case with underscores as word-separators. Example: `entry_points.md`
3. **Headers must be set in sentence-case**. Example: "Entry points"
4. Separate paragraphs by one empty line, but not more.
5. Use the `-` symbol for itemized lists.
6. Correctly prefix code fences/[code-block directives](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block) to indicate their usage, e.g.

- Bash shell scripts should use `bash`

  ````md
  ```bash
  echo "hi"
  ```
  ````

- Bash shell **sessions** (i.e. interactive) should use `console`

  ````md
  ```console
  $ echo "hi"
  ```
  ````

  Use ``#`` instead of ``$`` to indicate a root prompt.

- Python scripts should use `python`
  
  ````md
  ```python
  print("hi")
  ```
  ````

- Python sessions (e.g. *via* `ipython`) should use `ipython`
  
  ````md
  ```ipython
  In  [1]: print("hi")
  Out [1]: "hi"
  ```
  ````

(dev/branches)=

## Git Branches

Repositories should use the `master` branch as their primary branch.
This branch should be "protected" on GitHub and require PR reviews and status checks before merging (see [GitHub branch configuration](https://docs.github.com/en/github/administering-a-repository/configuring-protected-branches)).

Additions to the `master` branch should follow these simple concepts:

- Use feature branches for all new features and bug fixes.
- Merge feature branches into the master branch using pull requests.
- Keep a high quality, up-to-date master branch.

(dev/pr_open)=

## Opening a Pull Request

Pull requests should be submitted to `master` early and often!

To improve understanding of pull requests "at a glance", the use of several standardized title prefixes is encouraged:

- **[BRK]** for changes which break existing builds or tests
- **[DOC]** for new or updated documentation
- **[ENH]** for enhancements
- **[FIX]** for bug fixes
- **[REF]** for refactoring existing code
- **[STY]** for stylistic changes
- **[TST]** for new or updated tests, and

You can also combine the tags above, for example if you are updating both a test and the documentation: **[TST, DOC]**.

PRs should also usually look to respond to one or more open issues. You can link a pull request to an issue to show that a fix is in progress and to automatically close the issue when the pull request is merged; see [Linking a pull request to an issue](https://docs.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue).

If your pull request is not yet ready to be merged, please open your pull request as a draft.
More information about doing this is [available in GitHub's documentation](https://help.github.com/articles/about-pull-requests/#draft-pull-requests).
This tells the development team that the pull request is a "work-in-progress", and that you plan to continue working on it.

When your pull request is "Ready for Review", you can select this option on the PR's page, which will notify project maintainers to review your proposed changes.

(dev/pr_reviews)=

## Pull Request Reviews

### Sources

- https://github.com/aiidateam/aiida-core/wiki/Best-practises-for-code-review
- https://google.github.io/eng-practices/review/reviewer/standard.html
- https://www.ibm.com/developerworks/rational/library/11-proven-practices-for-peer-review/index.html
- https://phauer.com/2018/code-review-guidelines/

[eng-practises]: https://google.github.io/eng-practices/review/reviewer/standard.html
[cisco-study]: https://www.ibm.com/developerworks/rational/library/11-proven-practices-for-peer-review/index.html
[phauer]: https://phauer.com/2018/code-review-guidelines/

### Standards

#### Approving changes

- Technical facts and data overrule personal preferences
- Favour approving a PR once it definitely improves code health overall, even if it isn't perfect

#### Vigilance

- Be responsive to review requests.
   Users who put in the effort of contributing back deserve our attention the most, and timely review of PRs is a big motivator.
- Look at every line of code that is being modified
- Use a check-list like the one below, especially if you are new to code review

#### Communication

- Offer encouragement for things done well, don't just point out mistakes
- Fine to mention what could be improved but is not mandatory (prefix such comments with "Nit:" for "nitpick")
- Good to share knowledge that helps the submitter improve their understanding of the code (clarify where you do/don't expect action)

### Check-list - What to look for

#### Scope

- Are you being asked to review more than 200 lines of code?
   Then don't be shy to ask the submitter to split the PR - review effectiveness [drops substantially beyond 200 lines of code][cisco-study].
- Are there parts of the codebase that have not been modified, but *should* be adapted to the changes?  
   Does the code change require an update of the documentation?

#### Design

- Does this change belong in the codebase?
- Is it integrated well?

#### Functionality

- Does the code do what the developer intended?
- Are there edge cases, where it could break?
- For UI changes: give it a try yourself! (difficult to grasp from reading code)

#### Complexity

- Any complex lines, functions, classes that are not easy to understand?
- Over-engineering: is the code too complex for the problem at hand?

#### Tests

- Are there tests for new functionality? \
Are bugs covered by a test that breaks if the bug resurfaces?
- Are the tests correct and useful? \
Do they make simple and useful assertions?

#### Naming

- A good name is long enough to communicate what the item does, without being so long that it becomes hard to read

#### Comments

- Do comments explain *why* code exists (rather than *what* it is doing)?

#### Style & Consistency

- Does the contribution follow generic coding style (mostly enforced automatically)?

(dev/merge_pr)=

## Merging Pull Requests

A pull request should be opened only once you consider it ready for review.
Each time you push a commit to a branch with an open PR, it triggers a CI build, eating up the quota of the organization.

There are three ways of 'merging' pull requests on GitHub.
**Squash and merge** is the favoured method, applicable to the majority of PRs, but there are some use cases where the other two apply:

- **Squash and merge**: take all commits, squash them into a single one and put it on top of the base branch.
  - Choose this by default for pull requests that address a single issue and are well represented by a single commit.
  - The person merging the PR should choose a [clear commit message](dev/commits) when merging (via the GitHub UI)
- **Rebase and merge**: take all commits and 'recreate' them on top of the base branch. All commits will be recreated with new hashes.
  - Choose this for pull requests that require more than a single commit.
  - Make sure [the commits have clear commit messages](dev/commits).
  - Examples: PRs that contain multiple commits with individually significant changes; PRs that have commits from different authors (squashing commits would remove attribution)
- **Merge with merge commit**: put all commits as they are on the base branch, with a merge commit on top
  - Choose for collaborative PRs with many commits.
     Here, the merge commit provides actual benefits.

One drawback of squash-merging is that it combines multiple commits into a single one. This is usually fine, as PRs have many commits like "fixing typo", and "addressing comments". Squashing these into one message allows the PR merger to create [a commit message that is clear and concise](dev/commits). However, sometimes a PR is best-represented by *multiple* commits. In this case, it's fine to rebase-merge or merge-commit.

> **How can I rename my commits locally?**
>
> If you'd like to rename commits locally (e.g., if you'd like to make a rebase-commit in GitHub, but wish to clean up the commit history first to use [commit messages that are clear and concise](dev/commits)), you can try an [**interactive rebase**]( https://thoughtbot.com/blog/git-interactive-rebase-squash-amend-rewriting-history). This allows you to convert a series of commits into a smaller number of commits, and you can choose the commit message for each one. However, this is an advanced git technique so only do this if you know what you're doing! If you just want to merge in your commits without interactively rebasing, it is not the end of the world.

(dev/commits)=

## Commit Messages

A commit:

- should ideally address one issue
- should be a self-contained change to the code base
- must not lump together unrelated changes

Repositories should follow the following convention (where possible):

```md
<EMOJI> <KEYWORD>: Summarize changes in 72 characters or less (#<PR number>)

More detailed explanatory text, if necessary.
The blank line separating the summary from the body is
critical (unless you omit the body entirely); various tools like `log`,
`shortlog` and `rebase` can get confused if you run the two together.

Explain the problem that this commit is solving. Focus on why you are
making this change as opposed to how (the code explains that).  Are
there side effects or other unintuitive consequences of this change?
Here's the place to explain them to someone else reading your message in
the future. Make sure to include some necessary context for difficult
concepts that might change in the future.

There is no need to mention you also added unit tests when adding a new feature. The code diff already makes this clear.
```

Keywords/emojis are adapted from [Emoji-Log](https://github.com/ahmadawais/Emoji-Log) and [gitmoji](https://github.com/carloscuesta/gitmoji) and should be one of the following (brackets contain [GitHub emoji markup](https://gist.github.com/rxaviers/7360908) for reference):

- `‼️ BREAKING:` (`:bangbang:`) — to introduce a back-incompatible change(s) (and/or remove deprecated code).
- `✨ NEW:` (`:sparkles:`) — to introduce a new feature(s).
- `👌 IMPROVE:` (`:ok_hand:`) — to improve an existing code/feature (with no breaking changes).
- `🐛 FIX:` (`:bug:`) — to fix a code bug.
- `📚 DOCS:` (`:books:`) — to add new documentation.
- `🔧 MAINTAIN:` (`:wrench:`) — to make minor changes (like fixing typos) which should not appear in a changelog.
- `🧪 TEST:` (`:testube:`) — to add additional testing only.
- `🚀 RELEASE:` (`:rocket:`) — to bump the package version for release.
- `⬆️ UPGRADE:` (`:arrow_up:`) — for upgrading a dependency pinning.
- `♻️ REFACTOR:` (`:recycle:`) — for refactoring existing code (with no specific improvements).
- `🗑️ DEPRECATE:` (`:wastebasket:`) — mark some code as deprecated (for removal in a later release). The future version when it will be removed should also be specified, and (if applicable) what will replace it.
- `🔀 MERGE:` (`:twisted_rightwards_arrows:`) — for a merge commit (then all commits within the merge should be categorised)
- `❓ OTHER:` (`:question:`) — anything not covered above (use as a last resort!).

This list is loosely in order of priority, e.g. a commit that is both a bug fix and back-incompatible should be categorised as `BREAKING` not `FIX`.

(dev/releases)=

## Releases and Change-logs

Releases should be made *via* [GitHub Releases](https://docs.github.com/en/github/administering-a-repository/managing-releases-in-a-repository), from the `master` branch and using [semantic versioning](https://semver.org/) for tags, e.g. `v1.2.1`, **for versions above 1.0.0**.
For versions below 1.0.0, it is understood that breaking changes are more frequent (i.e. the repo is in beta), and so semantic versioning is relaxed such that MINOR version changes also signify backward incompatible releases.

The change-log should be easy for users and developers to understand the key changes (as [discussed here](https://keepachangelog.com/)), and should mirror the commits categories described above, with the following format:

```md
## 1.1.0 - 2020-06-25

### Added
- List of `NEW` commits

### Improved
- List of `IMPROVE` commits

### Fixed
- List of `FIX` commits

### Breaking
- List of `BREAKING` and `UPGRADE` commits

### Deprecated
- List of `DEPRECATE` commits

### Documented
- List of `DOCS` commits

```

Sub-headings with no content can be skipped and commits by contributors should be given attrition (e.g. ", thanks to @chrisjsewell").

Package releases should be automated *via* GitHub Action workflows, triggered on tag creation. For examples see:

- <https://github.com/pypa/gh-action-pypi-publish>
- <https://github.com/pascalgn/npm-publish-action>

Use the [needs key](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idneeds) to ensure these actions runs only after pre-commit and unit tests have successfully passed.

### The process of creating a release

Below is the full workflow for creating a release:

- Make a release commit `🚀 RELEASE: ...` on `master` (*via* PR) which bumps the version to `M.m.p` (e.g. changing `__version__` for python packages) and adds a section to `CHANGELOG.md` in the format above.
- Create a GitHub release for that commit, with tag `vM.m.p`, heading `Version M.m.p` (optionally including the changelog section in the body).
- Check that automated release workflows complete successfully.

(dev/deprecations)=

## Deprecations

After the repository has moved out of beta development (i.e. is at version >= 1.0.0), intended deprecations of APIs (functions, classes, etc) should be signalled in the changelog and in the code, e.g. using the [Sphinx deprecated directive](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-deprecated) and/or [DeprecationWarning](https://docs.python.org/3/library/exceptions.html#DeprecationWarning) in Python packages:

```python
import warnings

def deprecated(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)
```

Ideally these should be added one or two major versions before they are actually removed from the code base. The future version when they will be removed should also be specified, and (if applicable) what it will be replaced by.

Where possible also, a list of deprecations should be maintained, such as: <https://www.sphinx-doc.org/en/master/extdev/deprecated.html>
