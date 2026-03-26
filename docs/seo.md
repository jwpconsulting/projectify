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

# Redirects

These should have 301 redirect:

- http://projectifyapp.com/
- https://projectifyapp.com/
- http://www.projectifyapp.com/

# Web Vitals

A recent web vitals pagespeed check brought up a few issues.[^pagespeed]

## Done

I've addressed these Web Vitals issues:

> Improve image delivery Est savings of 524 KiB

Projectify now converts PNG files to WebP. This cuts down landing page
transfer size by about 50 %.

> Render blocking requests Est savings of 170 ms
>
> Requests are blocking the page's initial render, which may delay LCP. Deferring or inlining can move these network requests out of the critical path.LCPFCPUnscored
>
> django/htmx.min.02440c0f5516.js 16.5 KiB 170 ms
> dist/styles.ad5a0e6f4aaa.css 7.3 KiB 50 ms

For `htmx.min.js`, I've added a `defer` property to its `<script>` tag.

For `styles.css`, I don't have a good inlining-based solution at this point. I've put
the relevant `<link rel="stylesheet">` tag before the `<script>` tags
and it seems to somewhat solve reflow issues.

I've tested with the `<head>` tag ordering with
Firefox network throttling set to "Good 2G". When the `<link rel="stylesheet">`
tag appears before the `<script>` tags, the layout doesn't shift around too
much.

> LCP request discovery
>
> Optimize LCP by making the LCP image discoverable from the HTML immediately, and avoiding lazy-loading
>
> lazy load not applied
> fetchpriority=high should be applied
> Request is discoverable in initial document

The fix was to add `fetchpriority=high` property to the landing top image.

> Use efficient cache lifetimes Est savings of 1 KiB
>
> A long cache lifetime can speed up repeat visits to your page. Learn more about caching.
>
> …external_links/primary.svg 1h 1 KiB

The solution is to update the following line in `projectify/views.py`:

```
-@cache_control(max_age=3600)
+@cache_control(max_age=60 * 60 * 24)
```

> Image elements do not have explicit width and height
>
> Set an explicit width and height on image elements to reduce layout shifts
> and improve CLS.

I've resolved this by automatically retrieving width and height from images
with the new `picture` templatetag in `projectify/templatetags/projectify.py`.

## To Do

The following Web Vitals issue remains:

Fix the following issue or test whether adding `defer` to the HTMX
`<script>` already solved it.

> Avoid chaining critical requests by reducing the length of chains, reducing
> the download size of resources, or deferring the download of unnecessary
> resources to improve page load.
>
> Maximum critical path latency: 848 ms
>
> * Initial Navigation
>   * https://www.projectifyapp.com 433 ms, 4.77 KiB
>     * …django/htmx.min.02440c0f5516.js(www.projectifyapp.com) 848 ms, 16.50 KiB
>     * …dist/styles.ad5a0e6f4aaa.css(www.projectifyapp.com) 823 ms, 7.31 KiB
>
> Preconnected origins
>
> preconnect hints help the browser establish a connection earlier in the page
> load, saving time when the first request for that origin is made. The
> following are the origins that the page preconnected to.
>
> no origins were preconnected
>
> Preconnect candidates
>
> Add preconnect hints to your most important origins, but try to use no more
> than 4.
>
> No additional origins are good candidates for preconnecting

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

# Error pages

- Projectify should have an error page for CSRF errors.

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

## 404 page

The 404 page didn't load its content correctly.

Example: https://www.projectifyapp.com/not-found

The solution was to fix the `{% block content %}` line to say `{% block body
%}` instead. The repository introduced this regression after adding
django-allauth and adjusting templates to match its `{% extends %}` hierarchy.

## Structured Data

See entries in `projectify/storefront/templates/storefront/index.html`.

- `SoftwareApplication` <https://developers.google.com/search/docs/appearance/structured-data/software-app>
- `Organization` <https://developers.google.com/search/docs/appearance/structured-data/organization>

Examples:

- [Example `Organization`](https://schema.org/Organization#eg-0007)
- [Example `SoftwareApplication`](https://schema.org/SoftwareApplication#4658)

## Add sitemap to Robots.txt

I've solved the following issue pointed out by semrush:

> Your robots.txt file is missing a valid sitemap URL. Add your sitemap URL to help search engines find and crawl your website.

## Canonical addresses

I've solved the following issue pointed out by semrush:

> There are critical issues with your canonical tag that may result in search
> engines indexing incorrect or duplicate pages. Ensure your page includes a
> single canonical tag that points to a live URL to avoid confusion.

See also <https://stackoverflow.com/a/32867221>

## Sitemap not found

I've solved the following issue by adding a sitemap `<link>` to the base
template:

> No XML sitemap found. Add a sitemap.xml or declare it in your robots.txt file.
