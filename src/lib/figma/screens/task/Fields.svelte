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
