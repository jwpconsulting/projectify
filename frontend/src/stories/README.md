# Encoding arg types

Arg types are only loosely documented, here:

- https://storybook.js.org/docs/7.0/svelte/api/argtypes
- https://storybook.js.org/docs/7.0/svelte/writing-stories/args

It doesn't fully work with Svelte yet because of a type issue.

```typescript
const argTypes = {
  label: {
    type: { name: "string", required: true },
    control: "text",
    defaultValue: "Hello, World",
  },
  size: {
    type: { name: "string", required: true },
    control: "select",
    defaultValue: "medium",
    options: ["extra-small", "small", "medium"],
  },
  color: {
    type: { name: "string", required: true },
    control: "select",
    defaultValue: "red",
    options: ["red", "blue"],
  },
  disabled: {
    type: { name: "boolean", required: true },
    control: "boolean",
    defaultValue: true,
  },
};
```
