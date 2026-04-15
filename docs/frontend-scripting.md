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

Projectify uses HTMX.

To make the `htmx.js` bundle, ensure you've enabled Nix flakes on your system
and run the following:

```bash
bin/build-htmx
```
