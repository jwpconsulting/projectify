<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

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
    // TODO missing:
    // proper input field
    // Wire into rest of application
    // Sub tasks need assignees
    import { _ } from "svelte-i18n";

    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";
    import type { SubTaskAssignment } from "$lib/types/stores";
    import type { CreateUpdateSubTask } from "$lib/types/workspace";

    // TODO we might want to create a separate sub task line for readonly.
    export let subTaskAssignment: SubTaskAssignment | undefined = undefined;
    export let subTask: Partial<CreateUpdateSubTask>;
    export let index: number | undefined = undefined;
    export let readonly = true;
    export let onInteract: (() => void) | undefined = undefined;
</script>

<div class="flex w-full flex-row items-center justify-between gap-2 px-2 py-1">
    <div class="flex grow flex-row items-center gap-2">
        <Checkbox
            bind:checked={subTask.done}
            disabled={readonly}
            contained={false}
            onClick={onInteract}
        />
        <!-- XXX should be only editable when in edit mode -->
        <div class="grow">
            <label for="sub-task" class="sr-only">
                $_("task-screen.enter-a-subtask")}
            </label>
            <InputField
                label={undefined}
                style={{ inputType: "text" }}
                placeholder={$_("task-screen.enter-a-subtask")}
                name="sub-task"
                bind:value={subTask.title}
                {readonly}
                onClick={onInteract}
            />
        </div>
    </div>
    {#if index !== undefined && subTaskAssignment && $subTaskAssignment}
        <div class="flex flex-row gap-2">
            <CircleIcon
                size="medium"
                icon="up"
                action={{
                    kind: "button",
                    action: subTaskAssignment.moveSubTaskUp.bind(null, index),
                    disabled: index < 1,
                }}
            />
            <CircleIcon
                size="medium"
                icon="down"
                action={{
                    kind: "button",
                    action: subTaskAssignment.moveSubTaskDown.bind(
                        null,
                        index,
                    ),
                    disabled: index >= $subTaskAssignment.length - 1,
                }}
            />
            <CircleIcon
                size="medium"
                icon="delete"
                action={{
                    kind: "button",
                    action: subTaskAssignment.removeSubTask.bind(null, index),
                }}
            />
        </div>
    {/if}
</div>
