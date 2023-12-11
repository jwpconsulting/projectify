<script lang="ts">
    import { _ } from "svelte-i18n";

    const leftSideClass = "min-w-content text-left font-bold align-top";
    const rightSideClass = "max-w-xs";
</script>

<table class="w-full max-w-4xl table-auto border-separate border-spacing-y-4">
    <tbody>
        <tr>
            <th scope="row" class={leftSideClass}>
                <label for="title">
                    {$_("task-screen.task-title")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="title" />
            </td>
        </tr>
        <tr>
            <th scope="row" class={leftSideClass}>
                <label for="assignee">
                    {$_("task-screen.assignee")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="assignee" />
            </td>
        </tr>
        <tr>
            <th scope="row" class={leftSideClass}>
                <label for="labels">
                    {$_("task-screen.labels")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="labels" />
            </td>
        </tr>
        <tr>
            <th scope="row" class={leftSideClass}>
                <label for="due-date">
                    {$_("task-screen.due-date")}
                </label>
            </th>
            <td class={rightSideClass}>
                <slot name="due-date" />
            </td>
        </tr>
        <tr>
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
