import { type Ref, watch } from 'vue';

export function calculateMasonryRowSpan(
  itemHeight: number,
  rowHeight: number,
  itemGap: number,
): number {
  if (!Number.isFinite(rowHeight) || rowHeight <= 0) return 1;

  const safeHeight = Number.isFinite(itemHeight) ? Math.max(itemHeight, 0) : 0;
  const safeGap = Number.isFinite(itemGap) ? Math.max(itemGap, 0) : 0;
  return Math.max(1, Math.ceil((safeHeight + safeGap) / rowHeight));
}

function layoutMasonryGrid(grid: HTMLElement): void {
  const style = window.getComputedStyle(grid);
  const rowHeight = Number.parseFloat(style.gridAutoRows);
  const itemGap = Number.parseFloat(style.columnGap);

  for (const child of grid.children) {
    if (!(child instanceof HTMLElement)) continue;

    const span = calculateMasonryRowSpan(
      child.getBoundingClientRect().height,
      rowHeight,
      itemGap,
    );
    const gridRowEnd = `span ${span}`;
    if (child.style.gridRowEnd !== gridRowEnd) {
      child.style.gridRowEnd = gridRowEnd;
    }
  }
}

export function useMasonryGrid(grid: Ref<HTMLElement | null>): void {
  watch(
    grid,
    (element, _previousElement, onCleanup) => {
      if (!element || typeof ResizeObserver === 'undefined') return;

      let animationFrame: number | undefined;
      const scheduleLayout = (): void => {
        if (animationFrame !== undefined) return;
        animationFrame = window.requestAnimationFrame(() => {
          animationFrame = undefined;
          layoutMasonryGrid(element);
        });
      };

      const resizeObserver = new ResizeObserver(scheduleLayout);
      const observeChild = (child: Element): void => {
        if (child instanceof HTMLElement) resizeObserver.observe(child);
      };
      const unobserveChild = (child: Element): void => {
        if (child instanceof HTMLElement) resizeObserver.unobserve(child);
      };

      element.dataset.masonryGrid = '';
      Array.from(element.children).forEach(observeChild);

      const mutationObserver = new MutationObserver((records) => {
        for (const record of records) {
          record.removedNodes.forEach((node) => {
            if (node instanceof Element) unobserveChild(node);
          });
          record.addedNodes.forEach((node) => {
            if (node instanceof Element) observeChild(node);
          });
        }
        scheduleLayout();
      });
      mutationObserver.observe(element, { childList: true });

      layoutMasonryGrid(element);

      onCleanup(() => {
        if (animationFrame !== undefined) {
          window.cancelAnimationFrame(animationFrame);
        }
        resizeObserver.disconnect();
        mutationObserver.disconnect();
        delete element.dataset.masonryGrid;
        for (const child of element.children) {
          if (child instanceof HTMLElement) {
            child.style.removeProperty('grid-row-end');
          }
        }
      });
    },
    { flush: 'post' },
  );
}
