<script>
    import IconPlus from "$lib/components/icons/icon-plus.svelte";
    import SettingPage from "$lib/components/SettingPage.svelte";
</script>

<SettingPage title="My Profile">
    <header
        class="flex flex-col justify-center items-center space-y-2 mt-[-40px]"
    >
        <div
            class="m-1 flex -space-x-1 overflow-hidden w-20 h-20 rounded-full shrink-0 ring-4"
        >
            <img
                draggable="false"
                width="100%"
                height="100%"
                src="https://picsum.photos/200"
                alt="user"
            />
        </div>
        <div class="font-bold text-xl">Not set</div>
    </header>
</SettingPage>
