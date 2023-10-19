<script lang="ts">
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import type { WorkspaceBoardSection } from "$lib/types/workspace";
    import { getDashboardWorkspaceBoardSectionUrl } from "$lib/urls";

    export let workspaceBoardSection: WorkspaceBoardSection;
</script>

<div class="flex flex-row items-center justify-between">
    <div class="flex flex-row items-center gap-6">
        <div class="shrink-0">
            <CircleIcon
                action={{
                    kind: "a",
                    href: getDashboardWorkspaceBoardSectionUrl(
                        workspaceBoardSection.uuid
                    ),
                }}
                size="medium"
                icon="close"
            />
        </div>
        <slot name="breadcrumbs">Breadcrumbs missing</slot>
    </div>
    <div class="flex h-10 flex-row items-center gap-4">
        <slot name="buttons" />
    </div>
</div>
