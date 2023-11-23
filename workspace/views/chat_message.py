"""
Chat message views.

Chat messages will not be in the initial release. Therefore, there will be
no replacement DRF views here and the mutations can just be deleted.

Maybe some brief remarks here would be good to show which permission checks
were done so far.

This is the previous mutation we have had:
@strawberry.field
def add_chat_message(
    self, info: GraphQLResolveInfo, input: AddChatMessageInput
) -> types.ChatMessage:
    qs = models.Task.objects.filter_for_user_and_uuid(
        info.context.user,
        input.task_uuid,
    )
    task = get_object_or_404(qs)
    assert info.context.user.has_perm(
        "workspace.can_create_chat_message", task
    )
    chat_message = task.add_chat_message(
        text=input.text,
        author=info.context.user,
    )
    return chat_message
"""
