<script lang="ts">
    import "../app.scss";
    import Header from "$lib/header/Header.svelte";
    import "../i18n.js";
</script>

<Header>
    <main class="flex">
        <slot />
    </main>
</Header>
<slot />
