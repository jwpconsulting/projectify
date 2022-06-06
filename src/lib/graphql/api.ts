import { Mutation_MoveTaskAfter } from './operations';
import { client } from './client';

export async function moveTaskAfter(
  taskUuid: string,
  workspaceBoardSectionUuid: string,
  afterTaskUuid: string | null = null,
): Promise<void> {
  try {
    const input: {
      taskUuid: string;
      workspaceBoardSectionUuid: string;
      afterTaskUuid?: string;
    } = {
      taskUuid,
      workspaceBoardSectionUuid,
    };

    if (afterTaskUuid) {
      input.afterTaskUuid = afterTaskUuid;
    }

    await client.mutate({
      mutation: Mutation_MoveTaskAfter,
      variables: { input },
    });
  } catch (error) {
    console.error(error);
  }
}
