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
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import type { WorkspaceBoardSection } from "$lib/types/workspace";
    import { getDashboardWorkspaceBoardSectionUrl } from "$lib/urls";

    export let workspaceBoardSection: WorkspaceBoardSection;
</script>

<div
    class="flex flex-row flex-wrap items-center justify-between gap-x-2 gap-y-4 lg:flex-nowrap"
>
    <div class="flex shrink flex-row items-center gap-6">
        <div class="shrink-0">
            <!-- XXX Needs label -->
            <CircleIcon
                action={{
                    kind: "a",
                    href: getDashboardWorkspaceBoardSectionUrl(
                        workspaceBoardSection.uuid,
                    ),
                }}
                size="medium"
                icon="close"
            />
        </div>
        <slot name="breadcrumbs">Breadcrumbs missing</slot>
    </div>
    <div class="flex items-center justify-between gap-4 sm:flex-row">
        <slot name="buttons" />
    </div>
</div>
