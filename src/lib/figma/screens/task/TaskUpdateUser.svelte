<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { User as UserIcon } from "@steeze-ui/heroicons";
    import type { User } from "$lib/types/user";
    import UpdateUser from "$lib/figma/buttons/UpdateUser.svelte";

    // Either a user has been assigned, or if not we should ask the user
    // to assign a user
    export let user: User | null;
</script>

<div class="flex flex-row items-center gap-4">
    <div class="w-6">
        <Icon src={UserIcon} theme="outline" />
    </div>
    <UpdateUser {user} />
</div>
