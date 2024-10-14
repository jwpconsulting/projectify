<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { workspace, project } from "$lib-stories/storybook";
    import Dashboard from "$routes/(platform)/dashboard/project/[projectUuid]/+page.svelte";

    const data = {
        injectProject: {
            ...project,
            archived: null,
            description: null,
            sections: [],
            workspace,
        },
    };
</script>

<Dashboard {data} />
