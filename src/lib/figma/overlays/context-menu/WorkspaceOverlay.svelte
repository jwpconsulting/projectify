<script lang="ts">
    import { _ } from "svelte-i18n";
    import MenuButton from "$lib/figma/buttons/MenuButton.svelte";
    import { Briefcase, Plus } from "@steeze-ui/heroicons";
    import { getDashboardWorkspaceUrl } from "$lib/urls";
    import { workspaces } from "$lib/stores/dashboard";
    import Loading from "$lib/components/loading.svelte";
</script>

{#if $workspaces}
    {#each $workspaces as workspace}
        <MenuButton
            kind={{
                kind: "a",
                href: getDashboardWorkspaceUrl(workspace.uuid),
            }}
            label={workspace.title}
            state="normal"
            icon={Briefcase}
        />
    {/each}
{:else}
    <Loading />
{/if}
<MenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("add new workspace not implemented")}
    label={$_("workspace-overlay.add-new-workspace")}
    state="normal"
    color="primary"
    icon={Plus}
/>
