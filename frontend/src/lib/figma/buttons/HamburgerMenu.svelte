<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { Menu, X } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    export let action: () => void;

    export let isActive: boolean;
    $: src = isActive ? Menu : X;
</script>

<button
    class="h-11 w-11 rounded-lg border border-transparent p-2.5 hover:bg-secondary-hover focus:border-base-content focus:outline-none active:bg-secondary-pressed"
    on:click={action}
>
    <Icon {src} theme="outline" />
</button>
