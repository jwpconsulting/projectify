---
title: Frontend scripting in Projectify
author: Justus
date: 2026-04-15
---
<!--
SPDX-FileCopyrightText: 2026 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

This document outlines the frontend scripting methods used by Projectify.

Projectify uses HTMX and ships with trix.js and Prose.

To all HTMX, trix.js and Prose with stylesheets, ensure you've enabled Nix flakes on your system
and run the following:

```bash
bin/build-thirdparty-scripts
```
