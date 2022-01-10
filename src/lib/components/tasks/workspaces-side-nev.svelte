<script lang="ts">
    import { query } from "svelte-apollo";
    import { Query_WorkspacesSideNav } from "$lib/grapql/queries";

    const workspaces = query(Query_WorkspacesSideNav);
</script>

{#if $workspaces.loading}
    Loading...
{:else if $workspaces.error}
    Error: {$workspaces.error["message"]}
{:else}
    {#each $workspaces.data["workspaces"] as workspace}
        <div>{workspace.uuid} / {workspace.title}</div>
    {/each}
{/if}
