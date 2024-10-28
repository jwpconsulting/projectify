<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<!-- TODO At some point we will add the tab bar and bread crumbs here -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import { currentTask } from "$lib/stores/dashboard/task";

    import type { LayoutData } from "./$types";

    export let data: LayoutData;

    $: task = $currentTask.or(data.task);
</script>

<svelte:head>
    <title>
        {$_("task.title", { values: { title: task.title } })}
    </title>
</svelte:head>

<slot />
