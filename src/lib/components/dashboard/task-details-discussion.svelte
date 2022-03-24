<script lang="ts">
    import { dateStringToLocal } from "$lib/utils/date";
    import UserProfilePicture from "../userProfilePicture.svelte";

    export let task;
</script>

<div class="flex flex-col h-full">
    <div
        class="flex flex-col divide-y divide-base-300 grow px-6 overflow-y-auto"
    >
        {#each task.chatMessages as message}
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
    <div class="px-6 border-t border-base-300 pt-6 space-y-2">
        <textarea
            rows="2"
            class="textarea textarea-bordered resize-none leading-normal p-4 w-full"
            placeholder={"Please enter message"}
        />
        <div class="flex items-center space-x-2">
            <div class="grow" />
            <button class="btn btn-primary rounded-full btn-sm">Send</button>
        </div>
    </div>
</div>
