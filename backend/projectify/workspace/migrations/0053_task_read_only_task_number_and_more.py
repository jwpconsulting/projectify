# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
# Generated by Django 4.2.7 on 2024-01-10 06:43
"""Update pg triggers."""

from typing import Any

from django.db import migrations

import pgtrigger.compiler
import pgtrigger.migrations


def do_nothing(apps: Any, schema_editor: Any) -> None:
    """Do nothing."""


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0052_alter_workspaceboard_options"),
    ]

    operations = [
        pgtrigger.migrations.AddTrigger(
            model_name="task",
            trigger=pgtrigger.compiler.Trigger(
                name="read_only_task_number",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func="\n              BEGIN\n                IF NEW.number != OLD.number THEN\n                    RAISE EXCEPTION 'invalid number: Task number                         cannot be modified after inserting Task.';\n                END IF;\n                RETURN NEW;\n              END;",
                    hash="d71160eac05635087e9050c4bca6f9abc84387d2",
                    operation="UPDATE",
                    pgid="pgtrigger_read_only_task_number_5ccc0",
                    table="workspace_task",
                    when="BEFORE",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="task",
            trigger=pgtrigger.compiler.Trigger(
                name="ensure_correct_workspace",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='\n                      DECLARE\n                        correct_workspace_id   INTEGER;\n                      BEGIN\n                        SELECT "workspace_workspace"."id" INTO correct_workspace_id\n                        FROM "workspace_workspace"\n                        INNER JOIN "workspace_workspaceboard"\n                            ON ("workspace_workspace"."id" =                             "workspace_workspaceboard"."workspace_id")\n                        INNER JOIN "workspace_workspaceboardsection"\n                            ON ("workspace_workspaceboard"."id" =                                  "workspace_workspaceboardsection"."workspace_board_id")\n                        INNER JOIN "workspace_task"\n                            ON ("workspace_workspaceboardsection"."id" =                                 "workspace_task"."workspace_board_section_id")\n                        WHERE "workspace_task"."id" = NEW.id\n                        LIMIT 1;\n                        IF correct_workspace_id != NEW.workspace_id THEN\n                            RAISE EXCEPTION \'invalid workspace_id: workspace being                                 inserted does not match correct derived workspace.\';\n                        END IF;\n                        RETURN NEW;\n                      END;',
                    hash="f18b127650f990f862d50adf94e0cf71a4d88dcb",
                    operation="INSERT OR UPDATE",
                    pgid="pgtrigger_ensure_correct_workspace_b7606",
                    table="workspace_task",
                    when="BEFORE",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="workspace",
            trigger=pgtrigger.compiler.Trigger(
                name="ensure_correct_highest_task_number",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func="\n              DECLARE\n                max_task_number   INTEGER;\n              BEGIN\n                SELECT MAX(workspace_task.number) INTO max_task_number\n                FROM workspace_task\n                WHERE workspace_task.workspace_id = NEW.id;\n                IF NEW.highest_task_number < max_task_number THEN\n                    RAISE EXCEPTION 'invalid highest_task_number:                      highest_task_number cannot be lower than a task number.';\n                END IF;\n                RETURN NEW;\n              END;",
                    hash="14d0919ac762fccd4436b2c900a04a30d30eefed",
                    operation="UPDATE",
                    pgid="pgtrigger_ensure_correct_highest_task_number_30a81",
                    table="workspace_workspace",
                    when="BEFORE",
                ),
            ),
        ),
        migrations.RunPython(do_nothing),
    ]
