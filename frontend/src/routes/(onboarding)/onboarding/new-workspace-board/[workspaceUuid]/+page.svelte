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
    import { _, json } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import { createWorkspaceBoard } from "$lib/repository/workspace/project";
    import { getNewTaskUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { workspace, project } = data;

    let title: string | undefined = undefined;

    $: disabled = title === undefined;

    async function submit() {
        if (!title) {
            throw new Error("Expected title");
        }
        const result = await createWorkspaceBoard(
            workspace,
            {
                title,
                description: "",
            },
            { fetch },
        );
        if (!result.ok) {
            throw result.error;
        }
        const { uuid } = result.data;
        const nextStep = getNewTaskUrl(uuid);
        await goto(nextStep);
    }

    $: prompts = $json("onboarding.new-project.prompt") as string[];
</script>

<Onboarding
    stepCount={5}
    step={1}
    nextAction={{
        kind: "submit",
        disabled,
        submit,
    }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.new-project.title")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-8">
            {#if project}
                <div class="flex flex-col gap-4">
                    <p>
                        {$_(
                            "onboarding.new-project.project-exists.message",
                            { values: { title: project.title } },
                        )}
                    </p>
                    <p>
                        <Anchor
                            label={$_(
                                "onboarding.new-project.project-exists.prompt",
                                { values: { title: project.title } },
                            )}
                            size="large"
                            href={getNewTaskUrl(project.uuid)}
                        />
                    </p>
                </div>
            {:else}
                <div class="flex flex-col gap-3">
                    {#each prompts as prompt}
                        <p>{prompt}</p>
                    {/each}
                </div>
            {/if}
        </div>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <InputField
            style={{ inputType: "text" }}
            name="title"
            label={$_("onboarding.new-project.input.label")}
            placeholder={$_(
                "onboarding.new-project.input.placeholder",
            )}
            bind:value={title}
            required
        />
    </svelte:fragment>

    <DashboardPlaceholder
        slot="content"
        state={{
            kind: "new-project",
            workspace,
            project,
            title:
                title ??
                project?.title ??
                $_("onboarding.new-project.default-name"),
        }}
    />
</Onboarding>
