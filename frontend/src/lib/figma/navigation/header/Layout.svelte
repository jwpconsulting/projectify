<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

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
    import { _ } from "svelte-i18n";

    import PolyLogo from "../polylogo.svg?url";

    export let logoVisibleDesktop = false;
    export let logoVisibleMobile = false;
    export let alwaysVisible = false;
    export let logoHref = "/";

    $: justCenter =
        !$$slots["desktop-left"] &&
        !$$slots["desktop-right"] &&
        $$slots["desktop-center"];
    // There are lots of conditionals here, it might make sense to refactor
    // it a bit
</script>

<nav
    class="hidden flex-row items-center justify-between border-b-2 border-border bg-foreground px-6 py-4 md:flex"
    class:justify-between={!justCenter}
    class:justify-center={justCenter}
    class:hidden={!alwaysVisible}
    class:flex={alwaysVisible}
>
    <div class="flex flex-row items-center gap-4">
        {#if logoVisibleDesktop}
            <a href={logoHref} class="shrink">
                <img src={PolyLogo} alt={$_("navigation.header.logo.alt")} />
            </a>
        {/if}
        {#if $$slots["desktop-left"]}
            <div class="flex flex-row gap-2">
                <slot name="desktop-left" />
            </div>
        {/if}
    </div>
    <slot name="desktop-center" />
    {#if $$slots["desktop-right"]}
        <div class="flex shrink-0 flex-row items-center gap-2">
            <slot name="desktop-right" />
        </div>
    {/if}
</nav>

{#if !alwaysVisible}
    <nav
        class="flex flex-row items-center justify-between border-b-2 border-border bg-foreground px-2 py-4 md:hidden"
    >
        {#if logoVisibleMobile}
            <a href={logoHref}>
                <img src={PolyLogo} alt={$_("navigation.header.logo.alt")} />
                <!-- TODO add text that says "back to landing" for AT users -->
            </a>
        {/if}
        <slot name="mobile" />
    </nav>
{/if}
