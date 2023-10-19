// TODO prohibit root level strings
// TODO type MessageDirectory = Record<string, MessageCollection>;
export type Message = string | string[] | MessagesRecord;
// TODO https://github.com/microsoft/TypeScript/issues/41164
// eslint-disable-next-line @typescript-eslint/no-empty-interface
interface MessagesRecord extends Record<string, Message> {}

export type MessageCollection = Record<string, Message>;
