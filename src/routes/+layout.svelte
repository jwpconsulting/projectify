<script lang="ts">
    import "$lib/app.scss";
    import Footer from "$lib/figma/navigation/Footer.svelte";
</script>

<svelte:head>
    <title>Projectify</title>
    <meta
        name="description"
        content="Projectify - Manage projects the right way"
    />
</svelte:head>

<slot />
<Footer />
