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
    export let heroBackground = true;
    export let isProseContent = false;
</script>

<!-- Common layout for solution layouts -->
<main
    class="flex flex-col items-center gap-10 bg-foreground pb-20"
    class:pt-10={!$$slots.hero}
>
    {#if $$slots.hero}
        <div
            class="flex w-full flex-col items-center bg-background"
            class:bg-background={heroBackground}
        >
            <div class="w-full max-w-4xl px-6 py-6 sm:py-12">
                <slot name="hero" />
            </div>
        </div>
    {/if}
    {#if $$slots.side}
        <div
            class="flex w-full max-w-5xl grow flex-col gap-4 bg-foreground p-6 sm:flex-row sm:gap-8"
        >
            <slot name="side" />
            <slot name="content" />
        </div>
    {:else}
        <div
            class="w-full p-6"
            class:w-full={!isProseContent}
            class:max-w-4xl={!isProseContent}
        >
            <slot name="content" />
        </div>
    {/if}
</main>
