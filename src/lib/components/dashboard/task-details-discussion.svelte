<script lang="ts">
    import { client } from "$lib/graphql/client";
    import { Mutation_AddChatMessage } from "$lib/graphql/operations";

    import { dateStringToLocal } from "$lib/utils/date";
    import UserProfilePicture from "../userProfilePicture.svelte";
    import { afterUpdate } from "svelte";

    export let task;

    let chatMessageText = "";

    async function sendChatMessage() {
        if (chatMessageText.length <= 1) {
            chatMessageText = "";
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_AddChatMessage,
                variables: {
                    input: {
                        taskUuid: task.uuid,
                        text: chatMessageText,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }

        chatMessageText = "";
    }

    let messagesView: HTMLDivElement;

    afterUpdate(() => {
        if (messagesView && task?.chatMessages?.length > 0) {
            messagesView.scrollTo(0, messagesView.scrollHeight);
        }
    });
</script>

<div
    class="flex flex-col h-full max-h-full overflow-hidden absolute w-full top-0 left-0"
>
    <div
        bind:this={messagesView}
        class="flex flex-col divide-y divide-base-300 grow px-6 overflow-y-auto"
    >
        {#each task?.chatMessages || [] as message}
            <div class="flex space-x-4  py-6">
                <div class="shrink-0">
                    <UserProfilePicture
                        pictureProps={{
                            url: message.author.profilePicture,
                            size: 32,
                        }}
                    />
                </div>
                <div class="grow space-y-2">
                    <div class="flex items-center space-x-2 text-xs">
                        <div class="font-bold grow">
                            {message.author.fullName || message.author.email}
                        </div>
                        <div class="font-bold opacity-50">
                            {dateStringToLocal(message.created, true)}
                        </div>
                    </div>

                    <div>{message.text}</div>
                </div>
            </div>
        {/each}
    </div>
    <div class="p-6 border-t border-base-300 space-y-2">
        <textarea
            rows="2"
            class="textarea textarea-bordered resize-none leading-normal p-4 w-full"
            placeholder={"Please enter message"}
            bind:value={chatMessageText}
            on:keyup={(e) => {
                if (!e.shiftKey && e.key === "Enter") {
                    sendChatMessage();
                }
            }}
        />
        <div class="flex items-center space-x-2">
            <div class="grow" />
            <button
                class="btn btn-primary rounded-full btn-sm"
                disabled={chatMessageText.length === 0}
                on:click={() => sendChatMessage()}>Send</button
            >
        </div>
    </div>
</div>
