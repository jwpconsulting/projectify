<script lang="ts">
    import { user, logout } from "$lib/stores/user";

    $: userData = $user;
</script>

{#if userData}
    <button
        class="flex p-3 justify-center items-center hover:bg-base-200 h-14 rounded"
    >
        <div class="flex mr-2   ">
            <span
                class="text-base font-bold overflow-hidden whitespace-nowrap text-ellipsis"
                >{userData?.email}</span
            >
        </div>
        <div
            class="m-1 flex -space-x-1 overflow-hidden w-8 h-8 rounded-full shrink-0 ring-2"
        >
            <img
                draggable="false"
                width="100%"
                height="100%"
                src="https://picsum.photos/200"
                alt="user"
            />
        </div>
    </button>
{/if}
