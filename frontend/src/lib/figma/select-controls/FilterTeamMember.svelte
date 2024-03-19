<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

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
    // TODO rename FilterTeamMember
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";
    import type { TeamMemberSelectionInput } from "$lib/types/ui";
    import { getDisplayName } from "$lib/types/user";

    export let teamMemberSelectionInput: TeamMemberSelectionInput;
    export let active: boolean;
    export let count: number | undefined;

    export let onSelect: () => void;
    export let onDeselect: () => void;

    function click() {
        active = !active;
        if (active) {
            onSelect();
        } else {
            onDeselect();
        }
    }
</script>

<button
    class="group flex w-full flex-row justify-between px-5 py-2 hover:bg-background"
    on:click={click}
>
    <div class="flex min-w-0 flex-row items-center gap-2">
        <div class="shrink-0">
            <Checkbox
                checked={active}
                disabled={false}
                contained={true}
                {onSelect}
                {onDeselect}
            />
        </div>
        <div class="flex min-w-0 flex-row items-center gap-2">
            {#if teamMemberSelectionInput.kind === "teamMember"}
                <AvatarVariant
                    content={{
                        kind: "single",
                        user: teamMemberSelectionInput.teamMember.user,
                    }}
                    size="medium"
                />
            {:else}
                <AvatarVariant
                    content={{
                        kind: "single",
                    }}
                    size="medium"
                />
            {/if}
            <div class="text-regular min-w-0 truncate">
                {#if teamMemberSelectionInput.kind === "unassigned"}
                    {$_("filter-team-member.assigned-nobody")}
                {:else if teamMemberSelectionInput.kind === "allTeamMembers"}
                    {$_("filter-team-member.all-users")}
                {:else if teamMemberSelectionInput.kind === "teamMember"}
                    {getDisplayName(teamMemberSelectionInput.teamMember.user)}
                {/if}
            </div>
        </div>
    </div>
    <div
        class="flex shrink-0 flex-row items-center gap-2 rounded-2.5xl bg-background px-2 py-0.5 text-primary group-hover:bg-foreground"
    >
        {count ?? ""}
    </div>
</button>
