---
title: Design a component library / design system
type: case
track: frontend
difficulty: core
status: drafted
sources: [Front End Interview Handbook, WCAG 2.2]
updated: 2026-09-02
tags: [component-api, design-tokens, a11y, versioning]
---

# Design a component library / design system

> A shared UI library used by 30 teams across 5 products.
> **The hard part:** API design and versioning. The code is easy; the contract is forever,
> and every escape hatch you don't provide becomes a fork.

## 1. Clarify

| Question | Assumed answer |
|---|---|
| Consumers? | 30 teams, one framework (React), multiple products with different brands |
| Theming? | Yes — multi-brand, light/dark, density modes |
| Release model? | Independent versioning, consumers upgrade on their own schedule |
| A11y target? | WCAG 2.2 AA, guaranteed by the library so product teams inherit it |
| SSR support? | Required |
| Design tool integration? | Tokens shared with Figma |

**Non-goals:** the visual design language itself, a component-per-page-layout catalogue.

## 2. Requirements

**Functional**
- ~40 primitives (button, input, select, dialog, table, toast…) that compose
- Themeable by token override, not by CSS overrides in consumer code
- Documented with live examples and accessibility notes
- Codemods for breaking changes

**Non-functional**

| Target | Value |
|---|---|
| Tree-shakeable | Importing `Button` must not pull in `DataTable` |
| Bundle cost | Each component's cost documented and budgeted |
| A11y | Every component keyboard-operable and screen-reader tested |
| Stability | Semver, deprecation window ≥ 2 minor versions |

## 3. Estimates

Not a traffic problem — the numbers that matter are organisational:

```
40 components × 30 teams = the blast radius of any breaking change
Upgrade cost: if a major version takes each team 2 days → 60 engineer-days per major.
   → Ship majors rarely; ship codemods; keep old APIs working through a deprecation window.
Bundle: a 40-component barrel export without tree-shaking can add 300 KB to every app.
```

> [!info] The real constraint
> **Migration cost across 30 teams.** Design the API so you rarely need a breaking change,
> because each one costs more than the feature that motivated it.

## 4. Interface — the actual deliverable

**Composition over configuration.** A component with 25 boolean props is a component nobody
can extend:

```tsx
// bad: every new need adds a prop, forever
<Dialog title="..." showClose hasFooter footerAlign="right" size="lg" ... />

// good: compound components — consumers arrange the parts
<Dialog>
  <Dialog.Trigger asChild><Button>Open</Button></Dialog.Trigger>
  <Dialog.Content>
    <Dialog.Title>Delete project?</Dialog.Title>
    <Dialog.Description>This cannot be undone.</Dialog.Description>
    <Dialog.Footer>
      <Dialog.Close asChild><Button variant="ghost">Cancel</Button></Dialog.Close>
      <Button variant="danger" onClick={onDelete}>Delete</Button>
    </Dialog.Footer>
  </Dialog.Content>
</Dialog>
```

Rules for every component API:

| Rule | Why |
|---|---|
| **Controlled and uncontrolled** both supported (`value` / `defaultValue` + `onChange`) | Consumers' state models differ; forcing one causes forks |
| **Forward the ref and spread the rest** (`...props`) | Without it, nobody can attach analytics, tooltips, or a test id |
| **`asChild` / render prop escape hatch** | Lets a consumer swap the rendered element instead of forking the component |
| **Styling hook** (`className`, data-attributes for states) | Overrides without `!important` wars |
| States are props (`loading`, `error`, `empty`) | The states exist whether you model them or not |
| No business logic, no data fetching | The moment a component fetches, it's coupled to one product |
| Polymorphic `as` only where genuinely needed | Types get expensive fast |

Those rules exist because of one recurring conversation, and its three possible endings:

```mermaid
sequenceDiagram
    autonumber
    participant T as One product team
    participant L as Library maintainer
    participant C as Component API
    participant O as The other 29 teams

    T->>L: "Dialog needs its footer aligned left, just for this one screen"

    rect rgb(255,240,240)
    Note over L,O: configuration — say yes with a prop
    L->>C: add a footerAlign prop with three accepted values
    Note over C: that is prop 26. Every combination is now a<br/>supported state to test and keep working forever,<br/>and the next request adds prop 27.
    O->>L: 29 more requests shaped exactly like this one
    end

    rect rgb(255,245,235)
    Note over T,O: say no, with no escape hatch
    L-->>T: out of scope
    T->>T: copies the component into the product repo
    Note over T,O: the fork misses next quarter's a11y fix. A keyboard<br/>trap now ships in one app and nobody can see it from<br/>here. Fork count is the library's real health metric.
    end

    rect rgb(240,255,240)
    Note over T,C: composition — the parts were always theirs to arrange
    L-->>T: Dialog.Footer takes children and className, asChild swaps<br/>the element, the ref forwards and the rest spreads
    T->>C: arranges its own footer. No new prop, and no fork.
    Note over C: the API did not change, so the other 29 teams pay<br/>nothing — which is the entire point, because a major<br/>version costs roughly 60 engineer-days across them.
    end
```

## 5. Data model — design tokens

```
primitive tokens   →  semantic tokens        →  component tokens
--blue-600            --color-action-primary    --button-primary-bg
--space-4             --space-inline-md         --button-padding-x
```

Three layers so a rebrand changes the *primitive* layer and everything downstream follows.
Consumers reference **semantic** tokens only; referencing a primitive (`--blue-600`) directly
is the thing that breaks dark mode and multi-brand.

- Source of truth in JSON, generated into CSS custom properties + TS types + Figma variables
  (Style Dictionary-style pipeline). One source, three outputs — no drift between design and
  code.
- Theming at runtime via CSS custom properties on a `[data-theme]` root, not by shipping N
  compiled stylesheets. Dark mode then costs zero JavaScript and no flash of wrong theme.

## 6. Architecture

```
tokens (JSON) ──build──→ css vars + TS constants + Figma variables
                              ↓
primitives (unstyled behaviour: focus, keyboard, ARIA — or wrap a headless library)
                              ↓
styled components (tokens applied) ──→ published package(s)
                              ↓
docs site (live examples, props table, a11y notes, do/don't) + Storybook
                              ↓
CI: unit + a11y (axe) + visual regression + bundle size budget per component
```

One source, three outputs, and two gates:

```mermaid
flowchart LR
    tok[("tokens.json<br/>primitive, then semantic, then component")]
    bld["Style Dictionary build"]
    css["CSS custom properties<br/>on a data-theme root"]
    ts["TS constants and types"]
    fig["Figma variables"]
    hl["Headless layer<br/>focus trap, roving tabindex, ARIA"]
    st["Styled components<br/>~40 primitives"]
    ci["CI gates<br/>axe, visual diff, bundle budget, SSR test"]
    pkg[["Published package<br/>subpath exports, sideEffects false"]]
    docs["Docs site and Storybook<br/>live examples, a11y notes"]
    teams["30 teams, 5 products"]

    tok ==> |"one source of truth"| bld
    bld --> |"runtime theming, zero JS, no wrong-theme flash"| css
    bld --> |"typed token names"| ts
    bld --> |"so design and code cannot drift"| fig
    css --> |"semantic tokens only, never a primitive"| st
    hl --> |"wrap it, do not reimplement it"| st
    st --> |"every interactive component"| ci
    ci ==> |"a11y or size regression blocks the release"| pkg
    st --> docs
    pkg --> |"importing Button must not pull in DataTable"| teams
    pkg -.-> |"a codemod ships with every breaking change"| teams
    teams -.-> |"fork count is the health metric"| st

    classDef service fill:#fff,stroke:#5f6368,color:#111
    classDef store fill:#fef7e0,stroke:#f9ab00,color:#111
    classDef queue fill:#f3e8fd,stroke:#a142f4,color:#111
    classDef client fill:#e8f0fe,stroke:#4285f4,color:#111
    class bld,hl,st,ci,docs service
    class tok,css,ts,fig store
    class pkg queue
    class teams client
```

**Build a headless layer or adopt one?** Reimplementing focus traps, roving tabindex, dialog
semantics and combobox keyboard behaviour correctly is months of work and a permanent
maintenance cost. Wrapping an established headless primitive library and owning the styling
is the lazy, correct answer — say so, and say what would make you build your own
(a genuinely unusual interaction model, or a hard no-dependency policy).

**Packaging:** one package with proper `exports` and `sideEffects: false` (tree-shaking
works) is simpler than 40 packages; 40 packages give finer versioning at high release
overhead. Recommend one package + subpath exports unless teams genuinely need independent
component versions.

## 7. Adoption & failure (the "scale" section for a library)

| Breaks first as adoption grows | Fix |
|---|---|
| Teams fork components to add one prop | Escape hatches (`asChild`, `className`, slots) so forking is never the cheapest path |
| Version skew — 30 teams on 12 versions | Long deprecation windows, codemods, an adoption dashboard per team/version |
| Bundle bloat in consumer apps | Per-component size budgets enforced in CI, tree-shaking verified by test |
| Design and code drift | Tokens generated from one source; visual regression tests in CI |
| Breaking change lands badly | Semver + changesets, canary releases, a migration guide with a codemod for every breaking change |

| Failure | Symptom | Mitigation |
|---|---|---|
| A11y regression | Keyboard trap in a dialog reaches production in 30 apps | axe in CI + manual screen-reader test on every interactive component before release |
| Visual regression | Subtle spacing change across all products | Snapshot/visual diffs gating merges |
| SSR mismatch | Hydration errors in consumer apps | SSR test app in CI; no `window` access at module scope |

## 8. Ops & cost (governance)

- **SLO-equivalent:** ≥ 90% of teams within 2 minor versions of latest; zero known a11y
  defects in released components.
- **Track:** adoption by team and version, fork count (the health metric — forks mean your
  API is too rigid), issue response time, bundle size trend.
- **Release:** changesets → automated versioning, canary on `next`, majors at most 1–2 per
  year with codemods.
- **Cost:** engineering time, and it's justified only by what it *removes* — 30 teams each
  building their own accessible dialog is the alternative. Say that: a design system is a
  cost-avoidance argument, and you should be able to make it in one sentence.
- **First thing I'd cut:** the number of components. A 40-component library nobody maintains
  is worse than 15 excellent ones.

## Referenced by

- [Frontend cases index](README.md)
- [Question bank](../07-drills/question-bank.md)
- [Repo index](../../INDEX.md)

## Sources & further reading

- [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) — the reference for every interactive pattern
- [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/)
- Vendor: `10-resources/vendor/front-end-interview-handbook/`
- Related repo skills: `shadcn`, `frontend-design:frontend-design`, `ui-ux-pro-max:design-system`
