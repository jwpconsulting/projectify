This file contains functions for managing tasks that were found in deleted
components. They might be useful.

# task-details-subtasks

```typescript
/* eslint-disable */
// TODO this file shall be deleted
import lodash from "lodash";
import { tick } from "svelte";
import { _ } from "svelte-i18n";

import { client } from "$lib/graphql/client";
import {
  Mutation_AddSubTask,
  Mutation_ChangeSubTaskDone,
  Mutation_DeleteSubTaskMutation,
  Mutation_MoveSubTaskMutation,
  Mutation_UpdateSubTask,
} from "$lib/graphql/operations";
import type { SubTask } from "$lib/types/workspace";

export let taskUuid: string;
export let subTasks: SubTask[];
let percent = 0;
let newSubTaskTitle = "";

$: {
  if (subTasks.length) {
    const sum = lodash.sumBy(subTasks, (it) => (it.done ? 1 : 0));
    percent = Math.round((sum / subTasks.length) * 100);
  }
}

async function addSubTask() {
  if (!newSubTaskTitle || newSubTaskTitle.length < 1) {
    return;
  }
  subTasks = [
    ...subTasks,
    {
      title: newSubTaskTitle,
      uuid: "",
      done: false,
      created: "",
      modified: "",
      order: 0,
    },
  ];

  if (taskUuid) {
    try {
      await client.mutate({
        mutation: Mutation_AddSubTask,
        variables: {
          input: {
            taskUuid: taskUuid,
            title: newSubTaskTitle,
            description: "",
          },
        },
      });
    } catch (error) {
      console.error(error);
    }
  }

  newSubTaskTitle = "";
}

async function changeSubTaskDone(subTask: SubTask) {
  if (!subTask || !subTask.uuid) {
    return;
  }

  try {
    await client.mutate({
      mutation: Mutation_ChangeSubTaskDone,
      variables: {
        input: {
          subTaskUuid: subTask.uuid,
          done: subTask.done,
        },
      },
    });
  } catch (error) {
    console.error(error);
  }
}

async function deleteSubTask(subTask: SubTask) {
  if (!subTask || !subTask.uuid) {
    return;
  }

  const inx = subTasks.findIndex((it) => subTask.uuid == it.uuid);
  if (inx == -1) {
    return;
  }
  subTasks.splice(inx, 1);
  subTasks = subTasks;

  try {
    await client.mutate({
      mutation: Mutation_DeleteSubTaskMutation,
      variables: {
        input: {
          uuid: subTask.uuid,
        },
      },
    });
  } catch (error) {
    console.error(error);
  }
}

async function moveSubTask(subTask: SubTask, order: number) {
  try {
    await client.mutate({
      mutation: Mutation_MoveSubTaskMutation,
      variables: {
        input: {
          subTaskUuid: subTask.uuid,
          order,
        },
      },
    });
  } catch (error) {
    console.error(error);
  }
}

async function moveUp(subTask: SubTask) {
  await moveSubTask(subTask, subTask.order - 1);
}
async function moveDown(subTask: SubTask) {
  await moveSubTask(subTask, subTask.order + 1);
}

let subtaskEditTitle: string | null = null;
let editSubtaskUuid: string | null = null;
let editSubtaskInput: HTMLElement | null = null;

async function editSubtask(subTask: SubTask) {
  editSubtaskUuid = subTask.uuid;
  subtaskEditTitle = subTask.title;

  await tick();

  if (!editSubtaskInput) {
    throw new Error("Expected editSubtaskInput");
  }
  editSubtaskInput.focus();
}
function stopEditSubtask() {
  editSubtaskUuid = null;
  subtaskEditTitle = null;
}

async function saveSubTask(subTask: SubTask) {
  if (!subtaskEditTitle) {
    return;
  }

  try {
    await client.mutate({
      mutation: Mutation_UpdateSubTask,
      variables: {
        input: {
          uuid: subTask.uuid,
          title: subtaskEditTitle,
          description: "",
        },
      },
    });
  } catch (error) {
    console.error(error);
  }

  subTask.title = subtaskEditTitle;
  editSubtaskUuid = null;
}
```

# task-details-discussion

```typescript
async function sendChatMessage() {
  let msg = chatMessageText.trim();
  chatMessageText = "";

  if (!msg) {
    return;
  }

  try {
    await client.mutate({
      mutation: Mutation_AddChatMessage,
      variables: {
        input: {
          taskUuid: task.uuid,
          text: msg,
        },
      },
    });
  } catch (error) {
    console.error(error);
  }
}

let messagesView: HTMLDivElement;

afterUpdate(() => {
  if (!task.chat_messages) {
    throw new Error("Expected task.chat_messages");
  }
  if (messagesView && task.chat_messages.length > 0) {
    messagesView.scrollTo(0, messagesView.scrollHeight);
  }
});
```
