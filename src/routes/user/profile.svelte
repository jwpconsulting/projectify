<script lang="ts">
    import AuthGuard from "$lib/components/authGuard.svelte";
    import IconPhotocamera from "$lib/components/icons/icon-photocamera.svelte";
    import IconUser from "$lib/components/icons/icon-user.svelte";
    import SettingFooterEditSaveButtons from "$lib/components/settingFooterEditSaveButtons.svelte";
    import SettingPage from "$lib/components/SettingPage.svelte";
    import { user } from "$lib/stores/user";
    let isEditMode = false;
</script>

<AuthGuard>
    <SettingPage title="My Profile">
        <header
            class="flex flex-col justify-center items-center space-y-2 mt-[-40px]"
        >
            <div class="relative">
                <div
                    class="m-1 flex overflow-hidden w-[120px] h-[120px] rounded-full shrink-0 ring-4 bg-secondary text-base-100"
                >
                    {#if $user.profilePicture}
                        <img
                            draggable="false"
                            width="100%"
                            height="100%"
                            src={$user.profilePicture}
                            alt="user"
                        />
                    {:else}
                        <IconUser />
                    {/if}
                </div>
                <button
                    class="absolute bottom-0 right-0 btn shadow-lg btn-circle children-first:w-2 text-primary"
                    ><IconPhotocamera /></button
                >
            </div>
            <div class="font-bold text-xl">
                {$user.fullName ? $user.fullName : "Not set"}
            </div>
        </header>

        <SettingFooterEditSaveButtons bind:isEditMode />
    </SettingPage>
</AuthGuard>
