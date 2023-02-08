<script lang="ts">
    import "../app.scss";
    import "../i18n.js";
    import DialogModal from "$lib/components/dialogModal.svelte";
    import DatePickerDropDown from "$lib/components/datePickerDropDown.svelte";
    import ConnectionStatus from "$lib/components/connectionStatus.svelte";
    import GlobalDropDown from "$lib/components/globalDropDown.svelte";
    import DestructiveOverlayContainer from "$lib/components/DestructiveOverlayContainer.svelte";
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import "$lib/stores/global-ui";
    import { browser } from "$app/env";
</script>

<svelte:head>
    <title>Projectify</title>
    <meta name="description" content="Projects menagemet app" />
</svelte:head>

<slot />

<ConnectionStatus />

{#if browser}
    <DialogModal id="dataPicker">
        <DatePickerDropDown />
    </DialogModal>
{/if}

<GlobalDropDown />

<DestructiveOverlayContainer />
<ContextMenuContainer />
