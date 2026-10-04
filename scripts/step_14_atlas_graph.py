#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 14: граф связей направлений.

Создаёт:
  - src/data/graph-positions.ts — координаты 17 узлов
  - src/components/DirectionGraph.astro — SVG-граф
  - патчит src/pages/napravleniya/index.astro — вставляет <DirectionGraph />

Запуск:
    python scripts\step_14_atlas_graph.py --dry-run
    python scripts\step_14_atlas_graph.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORCE = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

FILES: dict[str, str] = {}

# ═════════════════════════════════════════════════════════════════════════
# 1. src/data/graph-positions.ts
# ═════════════════════════════════════════════════════════════════════════
# Координаты в системе viewBox 1000×700.
# Ручная раскладка: постоянные (1-14, 17) образуют внутреннее кольцо,
# временное (16) и переходное (15) — на периферии.
FILES["src/data/graph-positions.ts"] = """\
// Позиции 17 узлов графа направлений.
// Система координат: viewBox 1000×700.
// Раскладка: 14 постоянных + 17 внутри, 15 и 16 — на периферии.

export interface GraphNode {
  id: number;
  x: number;
  y: number;
}

export const graphNodes: GraphNode[] = [
  // Верхняя дуга — 4 узла
  { id: 6,  x: 500, y: 90  },  // Ноология (центр сверху)
  { id: 4,  x: 380, y: 130 },  // Трансляция
  { id: 10, x: 620, y: 130 },  // Искусство
  { id: 14, x: 500, y: 200 },  // Знание (под Ноологией)

  // Правая сторона — 4 узла
  { id: 5,  x: 750, y: 260 },  // Логистика
  { id: 13, x: 800, y: 380 },  // Верификация
  { id: 9,  x: 750, y: 500 },  // Кибернетика
  { id: 16, x: 880, y: 600 },  // Сеть (периферия)

  // Нижняя дуга — 4 узла
  { id: 7,  x: 620, y: 600 },  // Обнуление
  { id: 3,  x: 500, y: 620 },  // Энергия
  { id: 1,  x: 380, y: 600 },  // Жизнеобеспечение
  { id: 2,  x: 250, y: 500 },  // Здравие

  // Левая сторона — 4 узла
  { id: 11, x: 200, y: 380 },  // Социальная Инкубация
  { id: 12, x: 250, y: 260 },  // Психоэкология
  { id: 17, x: 320, y: 440 },  // Правозащита (внутри левой стороны)

  // Центр — 1 узел
  { id: 8,  x: 500, y: 380 },  // Балансировка (центр всей системы)

  // Периферия — переходное направление
  { id: 15, x: 120, y: 600 },  // Шлюз (изолирован)
];

export const graphEdges: [number, number][] = [];
"""

# ═════════════════════════════════════════════════════════════════════════
# 2. src/components/DirectionGraph.astro
# ═════════════════════════════════════════════════════════════════════════
FILES["src/components/DirectionGraph.astro"] = """\
---
import { directions, directionsById } from '../data/directions';
import { graphNodes } from '../data/graph-positions';

const base = import.meta.env.BASE_URL.replace(/\\/$/, '');

// Индексы для быстрого поиска координат
const posById: Record<number, { x: number; y: number }> = {};
for (const n of graphNodes) {
  posById[n.id] = { x: n.x, y: n.y };
}

// Собираем рёбра (без дублей: [a,b] и [b,a] — одно)
const edgeSet = new Set<string>();
const edges: { a: number; b: number }[] = [];
for (const d of directions) {
  for (const rid of d.related) {
    const key = d.id < rid ? `${d.id}-${rid}` : `${rid}-${d.id}`;
    if (edgeSet.has(key)) continue;
    edgeSet.add(key);
    if (posById[d.id] && posById[rid]) {
      edges.push({ a: d.id, b: rid });
    }
  }
}
---

<div class="graph-wrap">
  <div class="graph-head">
    <p class="graph-head__label mono">Карта связей</p>
    <h2 class="graph-head__title">17 узлов, одна сеть</h2>
    <p class="graph-head__sub">
      Линии — связи между направлениями. Размер и цвет узла —
      статус: постоянное (золото), временное (циан), переходное (серо-синий).
    </p>
  </div>

  <svg
    class="graph"
    viewBox="0 0 1000 700"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="Граф связей между направлениями"
  >
    <!-- Рёбра -->
    <g class="graph__edges">
      {edges.map((e) => {
        const pa = posById[e.a];
        const pb = posById[e.b];
        return (
          <line
            x1={pa.x} y1={pa.y}
            x2={pb.x} y2={pb.y}
            data-a={e.a}
            data-b={e.b}
            stroke="var(--gold-dim)"
            stroke-width="1"
            opacity="0.4"
          />
        );
      })}
    </g>

    <!-- Узлы -->
    <g class="graph__nodes">
      {directions.map((d) => {
        const p = posById[d.id];
        if (!p) return null;
        const statusClass = `is-${d.status}`;
        return (
          <a
            href={`${base}/napravleniya/${d.slug}`}
            class={`graph__node ${statusClass}`}
            data-id={d.id}
          >
            <circle cx={p.x} cy={p.y} r="28" class="graph__circle" />
            <text
              x={p.x} y={p.y + 4}
              text-anchor="middle"
              class="graph__icon"
            >{d.icon}</text>
            <text
              x={p.x} y={p.y + 52}
              text-anchor="middle"
              class="graph__label"
            >{d.shortName}</text>
          </a>
        );
      })}
    </g>
  </svg>

  <div class="graph-legend">
    <span class="graph-legend__item graph-legend__item--permanent">
      <span class="graph-legend__dot"></span> Постоянное
    </span>
    <span class="graph-legend__item graph-legend__item--temporary">
      <span class="graph-legend__dot"></span> Временное
    </span>
    <span class="graph-legend__item graph-legend__item--transitional">
      <span class="graph-legend__dot"></span> Переходное
    </span>
  </div>
</div>

<script>
  const svg = document.querySelector('.graph');
  if (svg) {
    const lines = svg.querySelectorAll('line');
    const nodes = svg.querySelectorAll('.graph__node');

    function highlight(id: number) {
      lines.forEach((l) => {
        const a = Number(l.getAttribute('data-a'));
        const b = Number(l.getAttribute('data-b'));
        const active = a === id || b === id;
        l.setAttribute('stroke', active ? 'var(--gold)' : 'var(--gold-dim)');
        l.setAttribute('opacity', active ? '1' : '0.15');
      });
      nodes.forEach((n) => {
        const nid = Number(n.getAttribute('data-id'));
        const el = n as SVGElement;
        if (nid === id) {
          el.style.opacity = '1';
        } else {
          const connected = Array.from(lines).some((l) => {
            const a = Number(l.getAttribute('data-a'));
            const b = Number(l.getAttribute('data-b'));
            return (a === id && b === nid) || (b === id && a === nid);
          });
          el.style.opacity = connected ? '1' : '0.35';
        }
      });
    }

    function clear() {
      lines.forEach((l) => {
        l.setAttribute('stroke', 'var(--gold-dim)');
        l.setAttribute('opacity', '0.4');
      });
      nodes.forEach((n) => {
        (n as SVGElement).style.opacity = '1';
      });
    }

    nodes.forEach((n) => {
      const id = Number(n.getAttribute('data-id'));
      n.addEventListener('mouseenter', () => highlight(id));
      n.addEventListener('mouseleave', clear);
    });
  }
</script>

<style>
  .graph-wrap {
    padding-block: 3rem;
    border-top: 1px solid var(--gold-dim);
    border-bottom: 1px solid var(--gold-dim);
  }

  .graph-head {
    text-align: center;
    max-width: 60ch;
    margin: 0 auto 3rem;
  }

  .graph-head__label {
    color: var(--gold);
    margin-bottom: 1rem;
  }

  .graph-head__title {
    font-size: clamp(1.75rem, 3vw, 2.5rem);
    margin-bottom: 1rem;
  }

  .graph-head__sub {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.6;
  }

  .graph {
    width: 100%;
    max-width: 900px;
    margin: 0 auto;
    display: block;
    aspect-ratio: 1000 / 700;
  }

  .graph__edges line {
    transition: stroke 200ms, opacity 200ms;
  }

  .graph__node {
    cursor: pointer;
  }

  .graph__node * {
    transition: all 200ms;
  }

  .graph__circle {
    fill: var(--bg-raised);
    stroke-width: 2;
  }

  .graph__node.is-permanent .graph__circle {
    stroke: var(--gold);
  }
  .graph__node.is-temporary .graph__circle {
    stroke: var(--cyan);
  }
  .graph__node.is-transitional .graph__circle {
    stroke: var(--transitional);
    stroke-dasharray: 4 3;
  }

  .graph__node:hover .graph__circle {
    fill: var(--bg-subtle);
    stroke-width: 3;
  }

  .graph__icon {
    font-size: 20px;
    pointer-events: none;
  }

  .graph__label {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    fill: var(--text-secondary);
    pointer-events: none;
  }

  .graph__node:hover .graph__label {
    fill: var(--gold-bright);
  }

  .graph-legend {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 2rem;
    margin-top: 2.5rem;
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
  }

  .graph-legend__item {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
  }

  .graph-legend__dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    border: 2px solid;
  }

  .graph-legend__item--permanent .graph-legend__dot { border-color: var(--gold); }
  .graph-legend__item--temporary .graph-legend__dot { border-color: var(--cyan); }
  .graph-legend__item--transitional .graph-legend__dot {
    border-color: var(--transitional);
    border-style: dashed;
  }

  /* На узких экранах граф прячется — там удобнее карточки */
  @media (max-width: 720px) {
    .graph-wrap { display: none; }
  }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 3. Патч главной Атласа
# ═════════════════════════════════════════════════════════════════════════
INDEX = ROOT / "src" / "pages" / "napravleniya" / "index.astro"

PATCH_IMPORT = (
    "import DirectionCard from '../../components/DirectionCard.astro';",
    "import DirectionCard from '../../components/DirectionCard.astro';\n"
    "import DirectionGraph from '../../components/DirectionGraph.astro';",
    "импорт DirectionGraph",
)

PATCH_INSERT = (
    '  <section class="atlas-section">',
    '  <section class="atlas-graph">\n'
    '    <div class="container">\n'
    '      <DirectionGraph />\n'
    '    </div>\n'
    '  </section>\n\n'
    '  <section class="atlas-section">',
    "вставка графа перед первой секцией",
)


def apply_files() -> tuple[int, int]:
    written = skipped = 0
    for rel, content in FILES.items():
        full = ROOT / rel
        if full.exists() and not FORCE:
            try:
                if full.read_text(encoding="utf-8") == content:
                    print(f"[same]  {rel}")
                    skipped += 1
                    continue
            except Exception:
                pass
            print(f"[skip]  {rel}")
            skipped += 1
            continue
        if DRY_RUN:
            print(f"[dry]   {rel} ({len(content)} B)")
            continue
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
        print(f"[write] {rel} ({len(content)} B)")
        written += 1
    return written, skipped


def apply_patches() -> int:
    if not INDEX.exists():
        print(f"[warn]  нет {INDEX}")
        return 0

    text = INDEX.read_text(encoding="utf-8")
    applied = 0

    for old, new, label in [PATCH_IMPORT, PATCH_INSERT]:
        if new.strip() in text:
            print(f"[skip]  {label} (уже применён)")
            continue
        if old not in text:
            print(f"[warn]  {label}: якорь не найден")
            continue
        if DRY_RUN:
            print(f"[dry]   {label}")
            continue
        text = text.replace(old, new, 1)
        print(f"[patch] {label}")
        applied += 1

    if applied and not DRY_RUN:
        INDEX.write_text(text, encoding="utf-8")

    return applied


def main() -> int:
    if not ROOT.exists():
        print(f"[ERR] нет {ROOT}")
        return 1

    print(f"Проект: {ROOT}")
    if DRY_RUN: print("Режим:  --dry-run")
    if FORCE: print("Режим:  --force")
    print()

    print("── Файлы ──")
    w, s = apply_files()
    print()

    print("── Патчи ──")
    p = apply_patches()
    print()

    print(f"Записано: {w}, пропущено: {s}, патчей: {p}.")
    print()
    print("Проверь:")
    print("  npm run dev")
    print("  http://localhost:4321/hartia/napravleniya")
    print()
    print("На десктопе сверху появится граф. На мобильном он скрыт.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())