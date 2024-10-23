<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Automatic API schema generation

An OpenAPI schema is to be generated and used to automatically verify frontend
API call correctness.

In the backend, we want to use
[drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/index.html),
in the frontend, we want to use an automatic code generator for TypeScript
bindings, such as
[openapi-typescript](https://www.npmjs.com/package/openapi-typescript).

# Backend: drf-spectacular

The schema is generated using

```bash
./manage.py spectacular --file schema/schema.yml
```

within the backend folder and has to be updated after any change to the API.
An additional step in the continuous integration will check if the API OpenAPI
schema is up to date or not.

## Annotating APIViews

Right now, no APIViews are annotated. This means that the generated
`schema.yml` does not contain any useful information on which fields can be
passed as JSON data.

The `@extend_schema` decorator, [documented
here](https://drf-spectacular.readthedocs.io/en/latest/readme.html#customization-by-using-extend-schema)
can be used to annotate every API with possible return values.

# Frontend: openapi-typescript and existing code

The repository package in `src/lib/repository` and the type binding contained
in `src/lib/types/{workspace,user,corporate}.ts`, ` already contain an attempt
at making type-safe API bindings. Unfortunately, different APIs do not return
all data, and keeping it manually in sync with the backend is tedious.

Furthermore, having an automatic check for API call correctness, can prevent
regressions.

## Using the generated schema `.d.ts` file

For now, we can try to use the resulting `schema.d.ts` file to guarantee the URLs
used for `fetch()` are correct. The schema file contains URLs in the exported
interface `paths`:

```typescript
export interface paths {
  // [...]
  "/corporate/workspace/{workspace_uuid}/create-billing-portal-session": {
    /** @description Handle POST. */
    post: operations["corporate_workspace_create_billing_portal_session_create"];
  };
  // [...]
}
```

A library like [openapi-fetch](https://openapi-ts.pages.dev/openapi-fetch/)
seems to do what our Repository does, just much more efficiently.
