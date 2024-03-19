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

    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import type { Section } from "$lib/types/workspace";
    import { getDashboardSectionUrl } from "$lib/urls";

    export let section: Section;
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
                    href: getDashboardSectionUrl(section.uuid),
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
