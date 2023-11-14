export type Message = string | string[] | MessagesRecord[] | MessagesRecord;
// TODO https://github.com/microsoft/TypeScript/issues/41164
// eslint-disable-next-line @typescript-eslint/no-empty-interface
interface MessagesRecord extends Record<string, Message> {}

export type MessageCollection = Record<string, Message>;

export type MessageDirectory = Record<string, MessageCollection>;
