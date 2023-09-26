<script lang="ts">
    import { _ } from "svelte-i18n";

    const leftSideClass = "min-w-content text-left font-bold align-top";
    const rightSideClass = "max-w-xs";
</script>

<table class="w-full max-w-4xl table-auto border-separate border-spacing-y-4">
    <colgroup>
        <col />
        <col />
    </colgroup>
    <tbody>
        <tr>
            <th scope="row" class={leftSideClass}>
                {$_("task-screen.task-title")}
            </th>
            <td class={rightSideClass}>
                <slot name="title" />
            </td>
        </tr>
        <tr>
            <th scope="row" class={leftSideClass}>
                {$_("task-screen.assignee")}
            </th>
            <td class={rightSideClass}>
                <slot name="assignee" />
            </td>
        </tr>
        <tr>
            <th scope="row" class={leftSideClass}>
                {$_("task-screen.labels")}
            </th>
            <td class={rightSideClass}>
                <slot name="labels" />
            </td>
        </tr>
        <tr>
            <th scope="row" class={leftSideClass}>
                {$_("task-screen.section")}
            </th>
            <td class={rightSideClass}>
                <slot name="section" />
            </td>
        </tr>
        <tr>
            <th scope="row" class={leftSideClass}>
                {$_("task-screen.due-date")}
            </th>
            <td class={rightSideClass}>
                <slot name="due-date" />
            </td>
        </tr>
        <tr>
            <th scope="row" class={leftSideClass}>
                {$_("task-screen.description")}
            </th>
            <td class={rightSideClass}>
                <slot name="description" />
            </td>
        </tr>
    </tbody>
</table>
