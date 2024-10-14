<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    export let label: string;
    export let href: string;
    export let active: boolean;
</script>

<a
    {href}
    class="border-b-2 p-2.5 font-bold uppercase hover:text-base-content"
    class:border-base-content={active}
    class:border-border={!active}
    class:text-base-content={active}
    class:text-utility={!active}
>
    {label}
</a>
