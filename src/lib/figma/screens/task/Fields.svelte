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
<!--
@components Contains the form fields used for task create and update

It would be best if we use regular InputFields with labels. TODO
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import { tw } from "$lib/utils/ui";

    const leftSideClass = tw`col-span-1 text-left font-bold`;
    const rightSideClass = tw`col-span-3`;
    const rowClass = tw`contents`;
</script>

<table class="flex w-full max-w-xl flex-col gap-y-4 sm:grid sm:grid-cols-4">
    <tbody class="contents">
        <tr class={rowClass}>
            <th scope="row" class={leftSideClass}>
                <label for="title">
                    {$_("task-screen.task-title")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="title" />
            </td>
        </tr>
        <tr class={rowClass}>
            <th scope="row" class={leftSideClass}>
                <label for="assignee">
                    {$_("task-screen.assignee")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="assignee" />
            </td>
        </tr>
        <tr class={rowClass}>
            <th scope="row" class={leftSideClass}>
                <label for="labels">
                    {$_("task-screen.labels")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="labels" />
            </td>
        </tr>
        <tr class={rowClass}>
            <th scope="row" class={leftSideClass}>
                <label for="due-date">
                    {$_("task-screen.due-date")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="due-date" />
            </td>
        </tr>
        <tr class={rowClass}>
            <th scope="row" class={leftSideClass}>
                <label for="description">
                    {$_("task-screen.description")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="description" />
            </td>
        </tr>
    </tbody>
</table>
