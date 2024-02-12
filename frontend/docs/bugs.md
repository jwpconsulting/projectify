# SVG id collision causing issues when display: none

This bug is [fixed](https://github.com/paolotiu/svelte-boring-avatars/issues/1)
with svelte-boring-avatars 1.2.3, yay.

Here is the code I finally was able to reproduce the issue with:

```svelte
<script lang="ts">
  import Avatar from "svelte-boring-avatars";

  const size = 24;
  const name = "hello-world";
</script>

<div class="hidden">
  <Avatar {name} {size} />
</div>
<Avatar {name} {size} />
```

We had this issue with SVGs imported from Figma before, see this stackoverflow
thread
[here](https://stackoverflow.com/questions/72871578/visibility-hidden-svg-sibling-side-effect).
It makes sense to use an SVG loader, but I am not sure how to integrate it
properly into vite at this point. For webpack,
[svg-inline-loader](https://www.npmjs.com/package/svg-inline-loader) exists.
And, a loader will most likely only work with SVG files. If we generate SVG
through svelte, we might have to come up with yet another solution.
