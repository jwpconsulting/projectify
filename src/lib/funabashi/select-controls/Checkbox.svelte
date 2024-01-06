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
    import { Check } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    export let checked: boolean | undefined;
    export let disabled: boolean;
    // TODO document what this is for
    export let contained: boolean;
    export let required = false;

    export let onSelect: (() => void) | undefined = undefined;
    export let onDeselect: (() => void) | undefined = undefined;
    export let onClick: (() => void) | undefined = undefined;

    function onChange() {
        if (checked && onSelect) {
            onSelect();
        } else if (onDeselect) {
            onDeselect();
        }
    }

    let outerStyle: string;
    $: {
        if (contained) {
            outerStyle =
                checked && !disabled
                    ? "bg-primary border-primary text-foreground group-hover:bg-primary-hover"
                    : disabled
                    ? ""
                    : "group-hover:bg-secondary-hover group-hover:border-foreground";
        } else {
            outerStyle =
                checked && !disabled
                    ? "bg-primary border-primary text-foreground hover:bg-primary-hover"
                    : disabled
                    ? ""
                    : "hover:bg-secondary-hover hover:border-foreground";
        }
    }
</script>

<!-- TODO improve -->
<div
    class="relative m-0.5 h-4 w-4 rounded border border-secondary-hover {outerStyle}"
>
    {#if checked}
        <Icon src={Check} class="absolute" theme="outline" />
    {/if}
    <input
        class="absolute -left-[3px] -top-[3px] h-5 w-5 appearance-none rounded-md border border-transparent"
        type="checkbox"
        bind:checked
        on:change={onChange}
        on:click|stopPropagation={onClick}
        {disabled}
        {required}
    />
</div>
