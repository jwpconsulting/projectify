import Sortable from "sortablejs";

type SortableParamenters = {
    group?: any;
    filter?: string;
    draggable?: string;
};

export function sortable(
    node: HTMLElement,
    params: SortableParamenters = {}
): any {
    const sortable = Sortable.create(node, {
        group: params.group,
        animation: 300,
        forceFallback: true,
        fallbackOnBody: true,
        filter: ".ignore-elements",
        handle: ".drag-handle",
        draggable: ".item",
        onStart(e) {
            node.dispatchEvent(
                new CustomEvent("dragStart", {
                    detail: {
                        from: e.from,
                        to: e.to,
                        oldIndex: e.oldIndex,
                        newIndex: e.newIndex,
                    },
                })
            );
        },
        onEnd(e) {
            node.dispatchEvent(
                new CustomEvent("dragEnd", {
                    detail: {
                        from: e.from,
                        to: e.to,
                        oldIndex: e.oldIndex,
                        newIndex: e.newIndex,
                    },
                })
            );
        },
        ...params,
    });
    return {
        destroy() {
            sortable.destroy();
        },
    };
}
