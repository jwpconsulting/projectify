<script lang="ts">
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import type { WorkspaceBoardSection } from "$lib/types/workspace";
    import { getDashboardWorkspaceBoardSectionUrl } from "$lib/urls";

    export let workspaceBoardSection: WorkspaceBoardSection;
</script>

<div
    class="flex flex-row flex-wrap items-center justify-between gap-x-2 gap-y-4 lg:flex-nowrap"
>
    <div class="flex shrink flex-row items-center gap-6">
        <div class="shrink-0">
            <!-- XXX Needs label -->
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
    <div class="flex items-center justify-between gap-4 sm:flex-row">
        <slot name="buttons" />
    </div>
</div>
