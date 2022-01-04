<script lang="ts">
    import Header from "$lib/header/Header.svelte";
    import "../App.css";
    import "../i18n.js";
</script>

<Header />

<main>
    <slot />
</main>
