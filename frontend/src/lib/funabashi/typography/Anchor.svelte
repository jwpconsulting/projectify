<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    // This adds coupling to svelte-i18n
    import { ExternalLink } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import type { AnchorSize } from "$lib/funabashi/types";

    export let href: string;
    export let label: string;
    export let size: AnchorSize = "normal";
    export let openBlank = false;

    let anchorClass: string;
    $: anchorClass = {
        normal: "text-base",
        large: "text-lg",
    }[size];
</script>

<a
    {href}
    class="text-primary underline hover:text-primary-hover active:text-primary-pressed {anchorClass}"
    target={openBlank ? "_blank" : undefined}
    >{label}{#if openBlank}
        <span class="sr-only">{$_("typography.anchor.new-tab")}</span><Icon
            src={ExternalLink}
            class="inline-block h-4 w-4 px-px"
            theme="outline"
        />{/if}</a
>
