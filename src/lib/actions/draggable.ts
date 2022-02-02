import { spring } from "svelte/motion";
import delay from "delay";

type DraggableParamenters = {
    direction?: string;
    handle?: string;
    moveToBody?: boolean;
    dragOffset?: number;
};

export function draggable(
    node: HTMLElement,
    params: DraggableParamenters
): any {
    params = {
        moveToBody: false,
        dragOffset: 10,
        ...params,
    };

    let x;
    let y;
    let startX, startY;
    let dragOverIt: HTMLElement = null;

    let dragStarted = false;

    let handle = node;

    if (params.handle) {
        handle = node.querySelector(params.handle);
    }

    const springOpts = {
        stiffness: 0.2,
        damping: 0.4,
    };

    const coordinates = spring({ x: 0, y: 0 }, springOpts);

    // Default Directions
    const directions = {
        y: true,
        x: true,
    };

    if (params?.direction === "x") {
        directions.y = false;
    } else if (params?.direction === "y") {
        directions.x = false;
    }

    let draggingItem: HTMLElement = node;

    coordinates.subscribe(($coords) => {
        if (!draggingItem) {
            return;
        }
        draggingItem.style.transform = `translate3d(${$coords.x}px, ${$coords.y}px, 0)`;
    });

    handle.addEventListener("mousedown", handleMouseDown);

    handle.addEventListener("click", handleClick);

    let zIndex;

    function handleMouseDown(event) {
        dragStarted = false;
        x = event.clientX;
        y = event.clientY;
        startX = x;
        startY = y;
        window.addEventListener("mousemove", handleMouseMove);
        window.addEventListener("mouseup", handleMouseUp);
    }

    let sDx, sDy;

    function handleMouseMove(event) {
        const dx = event.clientX - x;
        const dy = event.clientY - y;

        sDx = event.clientX - startX;
        sDy = event.clientY - startY;
        const dist = Math.sqrt(sDx * sDx + sDy * sDy);

        if (!dragStarted && dist > 10) {
            dragStarted = true;
            node.dispatchEvent(new CustomEvent("dragstart"));
            console.log("Stard Dragging");

            zIndex = node.style.zIndex;
            node.style.zIndex = "10000";

            // coordinates.stiffness = coordinates.damping = 1;

            if (params.moveToBody) {
                const bounds = node.getBoundingClientRect();

                draggingItem = node.cloneNode(true) as HTMLElement;
                draggingItem.style.position = "fixed";
                draggingItem.style.left = `${bounds.x}px`;
                draggingItem.style.top = `${bounds.y}px`;
                draggingItem.style.zIndex = "10000";
                draggingItem.style.opacity = "0.9";
                draggingItem.style.width = `${node.clientWidth}px`;
                draggingItem.style.height = `${node.clientHeight}px`;

                node.style.opacity = "0.0";

                document.body.appendChild(draggingItem);
            }
        }

        x = event.clientX;
        y = event.clientY;
        coordinates.update(
            ($coords) => {
                return {
                    x: directions.x ? $coords.x + dx : 0,
                    y: directions.y ? $coords.y + dy : 0,
                };
            },
            { hard: true }
        );

        let els = document.elementsFromPoint(x, y);
        els = els.filter((el) => {
            if (!el.classList.contains("sortable-item")) {
                return false;
            }
            return true;
        });
        if (els[1]) {
            if (!dragOverIt || els[1] != dragOverIt) {
                if (dragOverIt && els[1] != dragOverIt) {
                    dragOverIt.dispatchEvent(new CustomEvent("dragout"));
                }

                dragOverIt = els[1] as HTMLElement;
                dragOverIt.dispatchEvent(new CustomEvent("dragover"));
            }
        } else {
            if (dragOverIt) {
                dragOverIt.dispatchEvent(new CustomEvent("dragout"));
                dragOverIt = null;
            }
        }
    }

    async function handleMouseUp(e) {
        window.removeEventListener("mousemove", handleMouseMove);
        window.removeEventListener("mouseup", handleMouseUp);

        if (!dragStarted) {
            return;
        }

        dragStarted = false;

        console.log("<<<", node.getClientRects());

        node.dispatchEvent(
            new CustomEvent("dragend", {
                detail: {
                    x: sDx,
                    y: sDy,
                },
            })
        );

        const nodeBounds = node.getBoundingClientRect();
        const draggingItemBounds = draggingItem.getBoundingClientRect();

        const dx = draggingItemBounds.x - nodeBounds.x;
        const dy = draggingItemBounds.y - nodeBounds.y;

        coordinates.update(
            () => {
                return {
                    x: dx,
                    y: dy,
                };
            },
            { hard: true }
        );

        x = 0;
        y = 0;
        coordinates.update(() => {
            return { x, y };
        });

        const curNode = node;
        const curDraggingItem = draggingItem;
        draggingItem = node;

        if (
            params.moveToBody &&
            curDraggingItem &&
            curDraggingItem != curNode
        ) {
            curDraggingItem.remove();
        }

        curNode.style.opacity = "1";

        if (dragOverIt) {
            dragOverIt.dispatchEvent(new CustomEvent("dragout"));
            dragOverIt = null;
        }

        await delay(1000);

        curNode.style.zIndex = zIndex;
    }

    function handleClick(e) {
        if (!dragStarted) {
            handle.dispatchEvent(new CustomEvent("dragClick"));
        }
    }

    return {
        destroy() {
            handle.removeEventListener("mousedown", handleMouseDown);
        },
    };
}
