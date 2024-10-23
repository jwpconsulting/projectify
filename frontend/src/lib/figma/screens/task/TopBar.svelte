<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import type {
        SectionDetail,
        TaskDetailSection,
    } from "$lib/types/workspace";
    import { getDashboardSectionUrl } from "$lib/urls";

    export let section: TaskDetailSection | SectionDetail;
</script>

<div
    class="sticky top-0 flex flex-row flex-wrap items-center justify-between gap-x-2 gap-y-4 bg-foreground pb-8 pt-4 lg:flex-nowrap"
>
    <div class="flex shrink flex-row items-center gap-6">
        <div class="shrink-0">
            <!-- XXX Needs label -->
            <CircleIcon
                action={{
                    kind: "a",
                    href: getDashboardSectionUrl(section),
                }}
                size="medium"
                icon="close"
                ariaLabel={$_("task.go-back-to-section")}
            />
        </div>
        <slot name="breadcrumbs">Breadcrumbs missing</slot>
    </div>
    <div class="flex items-center justify-between gap-4 sm:flex-row">
        <slot name="buttons" />
    </div>
</div>
