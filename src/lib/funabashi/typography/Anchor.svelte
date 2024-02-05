<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
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
        // TODO remove this class
        small: "text-sm",
        normal: "text-base",
        large: "text-lg",
    }[size];
</script>

<a
    {href}
    class={`font-medium text-primary underline hover:text-primary-hover active:text-primary-pressed ${anchorClass}`}
    target={openBlank ? "_blank" : "_self"}
>
    {label}{#if openBlank}
        <span class="sr-only">{$_("typography.anchor.new-tab")} </span><Icon
            src={ExternalLink}
            class="inline-block h-4 w-4 px-px"
            theme="outline"
        />{/if}</a
>
