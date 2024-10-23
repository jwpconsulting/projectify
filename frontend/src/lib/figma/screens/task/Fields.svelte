<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<!-- It would be best if we use regular InputFields with labels. TODO -->
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
                    {$_("task-screen.form.title.label")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="title" />
            </td>
        </tr>
        <tr class={rowClass}>
            <th scope="row" class={leftSideClass}>
                <label for="assignee">
                    {$_("task-screen.form.assignee.label")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="assignee" />
            </td>
        </tr>
        <tr class={rowClass}>
            <th scope="row" class={leftSideClass}>
                <label for="labels"
                    >{$_("task-screen.form.labels.label")}</label
                >
            </th>
            <td class={rightSideClass}>
                <slot name="labels" />
            </td>
        </tr>
        <tr class={rowClass}>
            <th scope="row" class={leftSideClass}>
                <label for="due-date"
                    >{$_("task-screen.form.due-date.label")}</label
                >
            </th>
            <td class={rightSideClass}>
                <slot name="due-date" />
            </td>
        </tr>
        <tr class={rowClass}>
            <th scope="row" class={leftSideClass}>
                <label for="description">
                    {$_("task-screen.form.description.label")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="description" />
            </td>
        </tr>
    </tbody>
</table>
