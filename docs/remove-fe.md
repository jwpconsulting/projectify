---
title: SvelteKit Frontend removal plan
---

SvelteKit SSR didn't turn out to be thing I thought it would be. Managing
global state through `getContext` and `setContext` means having to rewrite,
refactor and retest large parts of the application.

Continuing using Svelte and SvelteKit at this point is starting to look
like I am trapped inside a sunk cost fallacy.

# Goal

We already use Django for the backend. Let's fully embrace Django and also
make use of HTMX, which seems to be beloved

- Fully render frontend in Django using server side templates/views
- Remove dependency on SvelteKit and Svelte.
- Remove Django channels / WebSocket dependency

# How

- Use forms, views, templates in Django
- Use HTMX for interactive bit
- Remove frontend and reverse proxy completely

# Nice to have

- Figure out how to pack backend in single executable binary with `nix bundle`

# SWOOOOOT

## Strengths

- Rendering will be a lot faster
- Remove a vast amount of dependencies
- Simplify frontend rendering complexity
- Lack of interactive features - a feature, actually
- Greatly reduce size of things sent to browser
- JavaScript can be mostly eliminated - great
- Django is great and venerable
- Smaller footprint means fewer bugs.
- No more frontend/backend API type issues
- Core business logic was never part of frontend anyway. Any code that is
  duplicated can now be safely removed.

## Weaknesses

- This will take time. It's a 50% rewrite.
- Not guaranteed to improve product.
- It's complex. Vast re-retesting will be required.

## Opportunities

- Using Django and keeping everything monolithic makes moving forward so much
  more pleasant, I like Django, therefore fun.
- I can learn HTMX yay, fun.
- I might discover latent bugs that I can now fix, fixing bugs is fun.

## Risks

- Lack of HTMX experience, scary scary.
- New bugs or regressions, oh no.
- Lose motivation, this is totally real.
- Maybe it turns out SvelteKit was great for reasons I wasn't aware of yet,
  unlikely, but who knows. It might have been the glue that held everything
  together

# Rewrite steps

## Analysis

1. Test out HTMX. Thoroughly. Make sure you are comfortable.
2. Take inventory of all frontend pages
3. Identify remaining risks
4. Determine acceptance criteria.
5. Consider alternatives.

## Planning

Subject to change.

1. Plan base template structure
2. Write out which views need to be created.
3. Write out which forms need to be created. See how DRF serializers can be turned
   into forms.
4. Write out which templates need to be created.
5. Identify all JavaScript only/frontend only functions that need to be recreated in
   Django

## Implementation

Subject to change.

1. Create views, templates and forms in tandem. Write test cases as you go.
2. Features removed? Update help. Update landing page.
3. Update all architecture docs.

### Removal steps

1. Remove `frontend/`
2. Remove frontend Docker builds
3. Remove reverse proxy
4. Remove frontend stuff from GitHub actions and CircleCI config
5. Remove frontend from render.com blueprint
6. Remove WebSocket API
7. Remove REST API

## Testing

1. Test and compare the two implementations.
2. Perform thorough test of billing logic.
3. Security audit. Check CSPs and other gotchas. Update security docs.
4. Good enough? Continue. Broken? Go back to Analysis

## Deployment

1. Deploy on render.com. Test thoroughly.
2. Security audit for Projectify on render.com

## Acceptance test

1. Perform user tests.
