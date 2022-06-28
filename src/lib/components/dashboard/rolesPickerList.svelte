<script lang="ts">
    import type { WorkspaceUserRole } from "$lib/types/workspaceUserRole";
    import { workspaceUserRoles } from "$lib/types/workspaceUserRole";
    import { createEventDispatcher } from "svelte";

    export let role: WorkspaceUserRole = null;
    export let dispatch = createEventDispatcher();

    function selectRole(value) {
        role = value;
        dispatch("roleChanged", { role });
    }
</script>

<div>
    <ul
        class="menu flex max-h-full flex-col divide-y divide-base-300 overflow-y-auto pt-2"
    >
        {#each workspaceUserRoles as itRole}
            <li>
                <a
                    href="/"
                    on:click|preventDefault={(e) => {
                        selectRole(itRole);
                    }}>{itRole}</a
                >
            </li>
        {/each}
    </ul>
</div>
