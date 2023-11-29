<script lang="ts">
    import { onMount } from "svelte";

    onMount(() => {
        throw new Error("this page shall not be seen");
    });
</script>

If you can see this page, then something went wrong.
