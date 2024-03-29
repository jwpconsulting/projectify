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
    import { X } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import TeamMemberCard from "$lib/figma/screens/workspace-settings/TeamMemberCard.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { inviteUser, uninviteUser } from "$lib/repository/workspace";
    import { currentWorkspace } from "$lib/stores/dashboard";
    import {
        currentTeamMemberCan,
        currentTeamMembers,
    } from "$lib/stores/dashboard/teamMember";
    import type { FormViewState } from "$lib/types/ui";
    import { coerceIsoDate } from "$lib/utils/date";

    import type { PageData } from "./$types";

    export let data: PageData;

    $: workspace = $currentWorkspace ?? data.workspace;

    async function uninvite(email: string) {
        const result = await uninviteUser(workspace, email, { fetch });
        if (result.ok) {
            return;
        }
        throw Error(JSON.stringify(result.error));
    }

    // Invite form
    let inviteEmail: string | undefined;

    let state: FormViewState = { kind: "start" };
    let inviteEmailValidation: InputFieldValidation | undefined = undefined;

    async function performInviteUser() {
        if (inviteEmail === undefined) {
            throw new Error("No email");
        }
        state = { kind: "submitting" };
        const result = await inviteUser(workspace, inviteEmail, { fetch });
        if (result.ok) {
            state = { kind: "start" };
            return;
        }
        if (result.error.email === undefined) {
            inviteEmailValidation = {
                ok: true,
                result: $_(
                    "workspace-settings.team-members.invite.form.email.validation.ok",
                ),
            };
            state = {
                kind: "error",
                message: $_(
                    "workspace-settings.team-members.invite.error.general",
                ),
            };
        } else {
            inviteEmailValidation = {
                ok: false,
                error: result.error.email,
            };
            state = {
                kind: "error",
                message: $_(
                    "workspace-settings.team-members.invite.error.field",
                ),
            };
        }
    }
</script>

<svelte:head>
    <title
        >{$_("workspace-settings.team-members.title", {
            values: { title: workspace.title },
        })}</title
    >
</svelte:head>

{#if $currentTeamMemberCan("create", "teamMemberInvite")}
    <form
        class="flex flex-col gap-4"
        on:submit|preventDefault={performInviteUser}
    >
        <InputField
            name="project-name"
            bind:value={inviteEmail}
            label={$_(
                "workspace-settings.team-members.invite.form.email.label",
            )}
            placeholder={$_(
                "workspace-settings.team-members.invite.form.email.placeholder",
            )}
            style={{ inputType: "email" }}
            required
            validation={inviteEmailValidation}
        />
        {#if state.kind === "error"}
            <p>{state.message}</p>
        {/if}
        <Button
            action={{ kind: "submit", disabled: state.kind === "submitting" }}
            label={$_("workspace-settings.team-members.invite.invite")}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
        />
    </form>
{/if}
<section class="flex flex-col gap-4">
    <h2 class="text-xl font-bold">
        {$_("workspace-settings.team-members.heading")}
    </h2>
    <table class="grid w-full grid-cols-4 items-center gap-y-4">
        <thead class="contents">
            <tr class="contents">
                <th
                    class="col-span-2 border-b border-border text-left font-bold"
                    >{$_("workspace-settings.team-members.team-member")}</th
                >
                <th class="border-b border-border text-left font-bold"
                    >{$_("workspace-settings.team-members.role")}</th
                >
                <th class="border-b border-border text-left font-bold"
                    >{$_("workspace-settings.team-members.actions.action")}</th
                >
            </tr>
        </thead>
        <tbody class="contents">
            {#each $currentTeamMembers as teamMember}
                <TeamMemberCard {teamMember} />
            {:else}
                <td class="col-span-4">
                    {$_(
                        "workspace-settings.team-members.no-team-members-found",
                    )}
                </td>
            {/each}
        </tbody>
    </table>
</section>
<section class="flex flex-col gap-4">
    <h2 class="text-xl font-bold">
        {$_("workspace-settings.team-members.invites.title")}
    </h2>
    <table class="grid w-full grid-cols-4 items-center gap-y-4">
        <thead class="contents">
            <tr class="contents">
                <th
                    class="col-span-2 border-b border-border text-left font-bold"
                    >{$_("workspace-settings.team-members.invites.email")}</th
                >
                <th class="border-b border-border text-left font-bold"
                    >{$_("workspace-settings.team-members.invites.date")}</th
                >
                <th class="border-b border-border text-left font-bold"
                    >{$_("workspace-settings.team-members.actions.action")}</th
                >
            </tr>
        </thead>
        <tbody class="contents">
            {#each workspace.team_member_invites as invite}
                <td class="col-span-2 overflow-x-auto">
                    {invite.email}
                </td>
                <td>{coerceIsoDate(invite.created)}</td>
                <td
                    ><Button
                        style={{
                            kind: "tertiary",
                            icon: { position: "left", icon: X },
                        }}
                        color="red"
                        action={{
                            kind: "button",
                            action: uninvite.bind(null, invite.email),
                        }}
                        size="medium"
                        label={$_(
                            "workspace-settings.team-members.actions.uninvite",
                        )}
                        grow={false}
                    />
                </td>
            {:else}
                <td class="col-span-3">
                    {$_("workspace-settings.team-members.invites.empty")}
                </td>
            {/each}
        </tbody>
    </table>
</section>
<hr />
<section class="flex flex-col gap-2">
    <strong>{$_("workspace-settings.team-members.help.title")}</strong>
    <ul class="flex list-inside list-disc flex-col gap-2">
        <li>
            <Anchor
                href="/help/team-members"
                label={$_(
                    "workspace-settings.team-members.help.about-team-members",
                )}
                size="normal"
                openBlank
            />
        </li>
        <li>
            <Anchor
                href="/help/roles"
                label={$_("workspace-settings.team-members.help.about-roles")}
                size="normal"
                openBlank
            />
        </li>
    </ul>
</section>
