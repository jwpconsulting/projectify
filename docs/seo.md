---
title: SEO checklist
author: Justus
---
<!--
SPDX-FileCopyrightText: 2026 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

This document tracks what's left for optimizing searchability and
discoverability in the public facing Projectify web app.

# Structured Data

- `SoftwareApplication` (https://developers.google.com/search/docs/appearance/structured-data/software-app)
- `Organization` (https://developers.google.com/search/docs/appearance/structured-data/organization)

# Redirects

These should have 301 redirect:

- http://projectifyapp.com/
- https://projectifyapp.com/
- http://www.projectifyapp.com/

# Web Vitals

Fix these issues for the landing page[^pagespeed]:

- Render blocking requests Est savings of 170 ms
- LCP request discovery
- Network dependency tree
- Use efficient cache lifetimes Est savings of 1 KiB
- Improve image delivery Est savings of 524 KiB
- Image elements do not have explicit width and height

[^pagespeed]: <https://pagespeed.web.dev/analysis/https-projectifyapp-com/eqgz7348lt?utm_source=search_console&form_factor=desktop&hl=en>

# Linkchecker

Run with the following:

```bash
nix run nixpkgs#linkchecker -- https://www.projectifyapp.com/
```

```
INFO linkcheck.cmdline 2026-03-15 10:01:09,835 MainThread Checking intern URLs only; use --check-extern to check extern URLs.
LinkChecker 10.6.0
Copyright (C) 2000-2016 Bastian Kleineidam, 2010-2025 LinkChecker Authors
LinkChecker comes with ABSOLUTELY NO WARRANTY!
This is free software, and you are welcome to redistribute it under
certain conditions. Look at the file `COPYING' within this distribution.
Read the documentation at https://linkchecker.github.io/linkchecker/
Write comments and bugs to https://github.com/linkchecker/linkchecker/issues

Start checking at 2026-03-15 10:01:09+009
[…]

URL        `/onboarding/new-workspace'
Name       `visit this URL'
Parent URL https://www.projectifyapp.com/help/workspaces, line 193, col 30
Real URL   https://www.projectifyapp.com/user/log-in?next=/onboarding/new-workspace
Check time 3.640 seconds
D/L time   0.000 seconds
Size       11.18KB
Warning    [http-redirected] Redirected to
           `https://www.projectifyapp.com/user/log-in?next=/onboarding/new-workspace'
           status: 302 Found.
Result     Valid: 200 OK

URL        `/onboarding'
Name       `onboarding page'
Parent URL https://www.projectifyapp.com/help/trial, line 204, col 31
Real URL   https://www.projectifyapp.com/user/log-in?next=/onboarding/welcome
Check time 3.907 seconds
D/L time   0.001 seconds
Size       11.17KB
Warning    [http-redirected] Redirected to
           `https://www.projectifyapp.com/onboarding/' status:
           301 Moved Permanently.
           [http-redirected] Redirected to
           `https://www.projectifyapp.com/onboarding/welcome'
           status: 302 Found.
           [http-redirected] Redirected to
           `https://www.projectifyapp.com/user/log-in?next=/onboarding/welcome'
           status: 302 Found.
Result     Valid: 200 OK

Statistics:
Downloaded: 659.27KB.
Content types: 21 image, 39 text, 0 video, 0 audio, 1 application, 3 mail and 26 other.
URL lengths: min=24, max=246, avg=59.

That's it. 90 links in 94 URLs checked. 4 warnings found. 0 errors found.
Stopped checking at 2026-03-15 10:01:33+009 (23 seconds)
```

Apparently linking to onboarding from the help pages causes issues for
crawling.

# Semrush

Semrush identified these issues:

## On-Page SEO

- Your title is too short (10 characters). Consider increasing its length to 50-60 characters.
- Your meta description is too short (52 characters). Consider increasing its length to at least 100 characters.
- Your content is too thin (248 words). Add more content to better inform users what your page is about. Aim for at least 500 words.

## Technical SEO

- There are critical issues with your canonical tag that may result in search engines indexing incorrect or duplicate pages. Ensure your page includes a single canonical tag that points to a live URL to avoid confusion.
- Your robots.txt file is missing a valid sitemap URL. Add your sitemap URL to help search engines find and crawl your website.
- No XML sitemap found. Add a sitemap.xml or declare it in your robots.txt file.

## Off-Page SEO

Semrush complained that not enough other domains are linking to
www.projectifyapp.com

## Social Media

Semrush complained that Facebook, Instagram, LinkedIn, and YouTube don't link
to Projectify.

## On-Page SEO

- Your heading structure is irregular. Aim for a logical heading structure with H2s, H3s, and H4s used to introduce sections and subsections. Avoid hierarchy gaps (e.g., H4s directly following H2s) and excess headings.
- No hreflang tags found. If your site has language- or region-specific versions, add hreflang tags to help search engines show the right version of the page.
- Your page is missing structured data. Add Schema.org markup to qualify for rich results and help search engines understand your content.

## Page Speed

- Your page is not mobile friendly. Mobile users may struggle with tiny text, missing responsive layouts, or hard-to-tap buttons. Implement a responsive viewport, increase font sizes, and enlarge/space tap targets.
- Clicks and taps on the page feel noticeably delayed and sluggish. Defer non-critical JavaScript, move work off the main thread, and reduce third-party script impact to improve the user experience.
- Unable to retrieve DOM Size metric. The page may be inaccessible or the API is unavailable.

# Asset optimization

Django should compress assets and use webp for pictures.

# Error pages

- Projectify should have an error page for CSRF errors.
- The 404 page doesn't load its content correctly. Try: https://www.projectifyapp.com/not-found

# Done

Here's what's already done for SEO.

## Agents

Crawlers should refrain from crawling these addresses:

- <https://www.projectifyapp.com/onboarding>
- <https://www.projectifyapp.com/onboarding/welcome>
- <https://www.projectifyapp.com/onboarding/welcome/>
- <https://www.projectifyapp.com/user/log-in?next=/onboarding/welcome/>

See the `Disallow:` lines in `projectify/templates/robots.txt`.

## Duplicate without user-selected canonical

This is an error from the Google Search Console that I don't quite understand.
It lists the following pages as affected:

- <https://www.projectifyapp.com/help>
- <https://www.projectifyapp.com/solutions/>

I've made `/help` and `/solutions` the canonical URLs and added these
redirects:

- `/help/` -> `/help`, see `projectify/help/urls.py`
- `/solutions/` -> `/solutions`, see `projectify/storefront/urls.py`

## Pages not found

I've removed a few pages so I should add a redirect for these:

- <https://www.projectifyapp.com/solutions/personal-use>
- <https://www.projectifyapp.com/help/keyboard-shortcuts>
- <https://www.projectifyapp.com/solutions/remote-work>
- <https://www.projectifyapp.com/solutions/research>
- <https://www.projectifyapp.com/solutions/project-management/>
- <https://www.projectifyapp.com/solutions/development-teams/>

The solution was to add more `RedirectView` instances. See
`projectify/storefront/urls.py` and `projectify/help/urls.py`.
