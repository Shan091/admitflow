# Workspace colour theme

The institution workspace uses warm ivory surfaces, charcoal text and terracotta actions,
inspired by [Claude's visual palette](https://claude.com/). AdmitFlow keeps its own name,
wordmark, typography, content and navigation. The trailing decorative logo dot is removed
from the login and workspace shells.

## Roles

| Token | Value | Role |
| --- | --- | --- |
| `--paper` | `#faf9f5` | Main ivory canvas |
| `--surface` | `#fffefa` | Input surfaces |
| `--sidebar` | `#f0eee6` | Navigation and login-story surface |
| `--ink` | `#292724` | Primary charcoal text |
| `--muted` | `#6b655d` | Secondary text and placeholders |
| `--accent` | `#a34f32` | Primary action, focus, caret and chart data |
| `--accent-hover` | `#874128` | Primary action hover |
| `--accent-soft` / `--accent-ink` | `#f0e0d5` / `#843e28` | Selected navigation |
| `--control-line` | `#8e867c` | Input and control boundaries |
| `--line` | `#ded9cf` | Decorative separators |

Semantic ready/processing/queued/failed states retain labelled status treatments. Success
green is reserved for status, rather than used as the product brand. Hover on inactive
navigation does not override the selected item's highlight. Selection, scrollbars, native
controls and keyboard focus use the same palette; the existing reduced-motion rule remains.

## Verification

Eight local browser checks cover login, admissions overview, knowledge and institution
management at 1440 and 390 px. All pass with no horizontal body overflow or browser runtime
errors. Screenshots were visually inspected. Computed contrast: primary-button text 5.64:1,
login muted text 5.47:1, input boundary 3.56:1 and selected navigation 6.05:1. Frontend
lint/build and the backend gate (313 default tests; strict typing across 127 files) pass.
Mechanical scans of the theme surfaces and subsequently changed catalogue component report
no findings. No student messages or provider calls were used for these UI checks.

The inspection also caught reference-programme list rows displaying the internal zero fee.
Rows now say **Application fee: Unverified**, matching the detail editor. An extension of
the existing reference-catalogue browser test failed before this fix and passes afterward,
including its existing desktop/mobile detail checks. No fee amount or payment state changed.

The local frontend was refreshed on port 3000. Public deployment was not performed.
