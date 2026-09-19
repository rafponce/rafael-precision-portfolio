# Rafael Ponce De Leon — Precision Portfolio

A dependency-free static portfolio with a responsive charcoal theme, a parametric canvas mesh, eleven project case studies and an internship timeline, and reusable Python content templates.

## Edit and build

Run `python scripts/build_portfolio.py` from the repository root. It renders `index.html`, `projects.html`, `404.html`, the eleven `projects/<slug>/index.html` routes and `experience/index.html`, and the matching deployable `dist/` tree. Commit generated pages alongside source changes. There is no npm installation or browser framework.

- Content and contact links: `content/portfolio.json`; templates: `scripts/build_portfolio.py`
- Shared theme and responsive layouts: `assets/portfolio/style.css`
- Menu, motion controls, reveal animations, counters, and mesh: `assets/portfolio/site.js`
- Optimized images and favicon: `assets/portfolio/`
- Sites identity and static output selection: `.openai/hosting.json`

The root pages are also compatible with the repository's existing GitHub Pages/Jekyll structure. Existing template files and project archives remain available. This redesign is prepared on its own branch for review; merging can update the existing GitHub Pages site according to its current publishing configuration.

## Verified content and remaining asset

The email and LinkedIn profile were verified against RafaelPonceDeLeon_Resume_Current4(1).pdf, uploaded August 20, 2026. The online resume URL is the existing `_config.yml` link and is preserved as the owner's managed resume destination. That external link could not be independently opened in this session.

The Nike figures of 70+ simulations, 22 test curves, and 11 materials come from the current project brief and later supplied updates. The saved resume has earlier 60+/17+ counts. The portfolio deliberately follows the newer brief. The self-balancing project is labeled as a concept, with no fabricated completed test results.

The supplied professional portrait is used in the About section. The April 2025 Zemax study uses original figures from the supplied PDF. The three softgoods case studies use all nine supplied images in their specified groups. Exact completion months were not recorded, so they are listed as 2024–2025 in a separate personal-project collection. The pants pattern dimensions are explicitly illustrative reconstructions; only the 0.5-inch seam allowance is confirmed.

The user requested synchronization with `rafponce/rafael-precision-portfolio`. That repository returned 404 through the current GitHub connection during this update, so remote synchronization could not be performed. The existing `rafponce.github.io` repository was not substituted.

## Image provenance

- `midsole.webp` and `mirror.webp`: original AI-generated conceptual illustrations, labeled accordingly. They do not depict proprietary Nike or JPL CAD or measured analysis.
- `tumbler-cad.webp`: actual team exploded CAD, Figure 1 of *Project Tumbler — Final Design Report*, May 27, 2026.
- `tumbler-wiring.webp`: actual team wiring schematic, Figure 2 of that report.
- `tumbler-yaw.webp`: actual measured wrapped-yaw response, Figure 8 of that report.
- Senior-design work remains identified as an academic team project. Individual teammate names were removed at Rafael’s request.
- Inline technical SVG diagrams are labeled schematic. The mesh comparison encodes the reported study, without fabricating numerical force–displacement or stress data.

## Accessibility and performance

Semantic headings, landmarks, skip link, keyboard-focus indicators, accessible mobile menu, descriptive image alternatives, and reduced-motion support are included. Animation can be paused, stops when offscreen or the page is hidden, and limits pixel density and frame rate. Images use WebP, explicit dimensions, and lazy loading. Content and navigation remain readable without JavaScript.

Validation performed: Python generation, JavaScript syntax, every generated route, local asset reference, internal anchor, unique element IDs, one main heading per page, and image alternative text. Browser screenshot/interaction QA was unavailable for this static deployment path and should be checked in the delivered site at desktop and mobile sizes.
