#!/usr/bin/env python3
"""Portable palette lookup and optional Matplotlib helpers. No input data inferred."""
import argparse
from contextlib import contextmanager
import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def corpus():
    return json.loads((SKILL_DIR / 'references' / 'corpus.json').read_text(encoding='utf-8'))


def palette_record(name):
    for item in corpus()['palettes']:
        if item['id'] == name:
            return item
    raise ValueError(f'Unknown palette {name!r}; run the list command for valid IDs')


def get_palette(name, n=None):
    """Return recorded colors; refuse silent recycling or made-up extra categories."""
    colors = [c['hex'] for c in palette_record(name)['colors']]
    if n is not None:
        if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= len(colors):
            raise ValueError(f'n must be an integer between 1 and {len(colors)}')
        return colors[:n]
    return colors


def relative_luminance(color):
    rgb = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    rgb = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in rgb]
    return sum(a * b for a, b in zip(rgb, (.2126, .7152, .0722)))


@contextmanager
def rc_context(palette='composition-six', font='DejaVu Sans'):
    """Scoped implementation starting points; never overwrite global user settings."""
    import matplotlib as mpl
    from cycler import cycler
    values = {
        'font.family': 'sans-serif', 'font.sans-serif': [font, 'DejaVu Sans'],
        'font.size': 8, 'axes.labelsize': 8, 'axes.titlesize': 8,
        'xtick.labelsize': 7, 'ytick.labelsize': 7, 'legend.fontsize': 7,
        'axes.linewidth': .6, 'xtick.major.width': .6, 'ytick.major.width': .6,
        'xtick.major.size': 3, 'ytick.major.size': 3,
        'xtick.direction': 'out', 'ytick.direction': 'out',
        'lines.linewidth': 1.25, 'axes.grid': False,
        'axes.prop_cycle': cycler(color=get_palette(palette)),
        'legend.frameon': False, 'figure.facecolor': 'white',
        'axes.facecolor': 'white', 'savefig.facecolor': 'white',
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
        'svg.hashsalt': 'nature-figure-style',
    }
    with mpl.rc_context(values):
        yield


def style_axes(ax, full_box=False):
    for side in ('top', 'right'):
        ax.spines[side].set_visible(full_box)
    ax.tick_params(top=False, right=False)
    return ax


def make_cmap(name, reverse=False):
    """Interpolation of anchors only; does not certify perceptual uniformity."""
    from matplotlib.colors import LinearSegmentedColormap
    colors = get_palette(name)
    if reverse:
        colors = colors[::-1]
    return LinearSegmentedColormap.from_list(name, colors)


def save_figure(fig, output, dpi=600):
    """Preserve canvas dimensions; caller must arrange labels inside the canvas."""
    stem = Path(output)
    stem.parent.mkdir(parents=True, exist_ok=True)
    paths = []
    for ext in ('svg', 'pdf', 'png'):
        path = Path(str(stem) + '.' + ext)
        fig.savefig(path, dpi=dpi, facecolor='white', transparent=False)
        paths.append(str(path))
    return paths


def preview(output):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    records = corpus()['palettes']
    with rc_context():
        fig = plt.figure(figsize=(12, 13.8))
        for i, row in enumerate(records):
            ax = fig.add_axes([.035 + (i // 12) * .5, .875 - (i % 12) * .071, .43, .061])
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 1)
            ax.axis('off')
            ax.text(0, .94, row['id'], fontsize=9, weight='bold', va='top')
            colors = [c['hex'] for c in row['colors']]
            for j, color in enumerate(colors):
                ax.add_patch(Rectangle((j, .13), .96, .40, facecolor=color,
                                       edgecolor='#BBBBBB', linewidth=.3))
                ax.text(j + .48, .04, color, ha='center', va='top', fontsize=5.8)
        fig.text(.035, .975, 'FOR THE NATURE / PALETTE ATLAS', fontsize=16, weight='bold')
        fig.text(.035, .951, '20 reviewed screenshots / 24 palettes / recorded labels + sampled corrections',
                 fontsize=9, color='#555555')
        fig.text(.035, .012, 'Palette colors are role-dependent; not all rows are categorical or color-vision safe.',
                 fontsize=9)
        paths = save_figure(fig, output, dpi=160)
        plt.close(fig)
    return paths


def statistical_demo(output):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import TwoSlopeNorm
    rng = np.random.default_rng(381)
    with rc_context():
        fig, axes = plt.subplots(2, 2, figsize=(180/25.4, 140/25.4))
        fig.subplots_adjust(left=.10, right=.96, top=.87, bottom=.12, wspace=.42, hspace=.58)
        fig.suptitle('Synthetic data / style demonstration', fontsize=10, y=.965, weight='bold')
        ax = axes[0, 0]
        values = [rng.normal(mu, .8, 45) for mu in (2.7, 3.4, 4.0)]
        colors = [get_palette('lavender-coral')[i] for i in (0, 5, 7)]
        parts = ax.violinplot(values, showextrema=False)
        for body, color in zip(parts['bodies'], colors):
            body.set_facecolor(color); body.set_edgecolor('#555555'); body.set_linewidth(.4); body.set_alpha(.85)
        for j, (data, color) in enumerate(zip(values, colors), 1):
            ax.scatter(j+rng.uniform(-.10, .10, len(data)), data, s=4,
                       color=color, edgecolors='#555555', linewidths=.15, zorder=3)
        ax.boxplot(values, widths=.13, showfliers=False, patch_artist=True,
                   boxprops={'facecolor':'white', 'linewidth':.6},
                   medianprops={'color':'black', 'linewidth':.8},
                   whiskerprops={'linewidth':.6}, capprops={'linewidth':.6})
        ax.set(xticks=[1, 2, 3], xticklabels=['G1', 'G2', 'G3'], ylabel='Response (a.u.)', title='Distribution + observations')

        ax = axes[0, 1]
        p = get_palette('ocean-uncertainty')
        x = np.linspace(0, 3, 80)
        for offset, color, marker, label in ((0, p[5], 'o', 'Scenario A'), (.4, p[6], 's', 'Scenario B')):
            y = 1 + offset + (.3 + offset) * x + .08*x*x
            band = .16 + .16*x
            ax.fill_between(x, y-band, y+band, color=color, alpha=.18, linewidth=0)
            ax.plot(x, y, color=color, marker=marker, markevery=14, markersize=2.5, label=label)
        ax.set(xlabel='Driver (a.u.)', ylabel='Response (a.u.)', title='Illustrative interval (not a CI)')
        ax.legend(loc='upper left', fontsize=6)

        ax = axes[1, 0]
        matrix = rng.normal(0, 1, (7, 5))
        m = ax.imshow(matrix, cmap=make_cmap('rose-blue-diverging'), norm=TwoSlopeNorm(0, -2.5, 2.5), aspect='auto')
        ax.set(xticks=range(5), xticklabels=['A', 'B', 'C', 'D', 'E'], yticks=range(7),
               yticklabels=[f'Feature {i}' for i in range(1, 8)], title='Signed effect / fixed midpoint')
        cb = fig.colorbar(m, ax=ax, fraction=.046, pad=.04)
        cb.set_label('Synthetic effect')

        ax = axes[1, 1]
        colors = get_palette('composition-six')[:4]
        shares = rng.dirichlet([4, 2, 1.5, 1], 5).T * 100
        bottom = np.zeros(5)
        for name, color, vals in zip(['I', 'II', 'III', 'IV'], colors, shares):
            ax.bar(range(5), vals, bottom=bottom, color=color, edgecolor='white', linewidth=.4, width=.77, label=name)
            bottom += vals
        ax.set(ylim=(0, 100), xticks=range(5), xticklabels=['T1', 'T2', 'T3', 'T4', 'T5'],
               ylabel='Composition (%)', title='Stable category mapping')
        ax.legend(ncols=4, loc='upper center', bbox_to_anchor=(.5, -.14), fontsize=6,
                  columnspacing=.8, handlelength=.8)
        for letter, ax in zip('abcd', axes.flat):
            style_axes(ax)
            ax.text(-.18, 1.08, letter, transform=ax.transAxes, fontsize=10, weight='bold')
        paths = save_figure(fig, str(output)+'-statistical', dpi=240)
        plt.close(fig)
    return paths


def mechanism_demo(output):
    """Generic original diagram to demonstrate layout; no claimed biological mechanism."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Circle
    with rc_context():
        fig, ax = plt.subplots(figsize=(180/25.4, 95/25.4))
        fig.subplots_adjust(left=.035, right=.965, bottom=.08, top=.86)
        ax.set(xlim=(-.15, 12.15), ylim=(0, 5)); ax.axis('off')
        fig.suptitle('Schematic layout demo / no experimental claims', fontsize=10, y=.965, weight='bold')
        p = get_palette('immune-blue-rose')
        for x, title, bg in [(0, '1  Inputs', p[2]), (4.1, '2  Main process', p[0]), (8.2, '3  Readouts', p[2])]:
            ax.add_patch(FancyBboxPatch((x, .2), 3.75, 4.5, boxstyle='round,pad=0.03,rounding_size=.10',
                                       facecolor=bg, edgecolor='#8190A3', linewidth=.6))
            ax.text(x+.2, 4.35, title, fontsize=8, weight='bold', color='#28354A')
        def node(x, y, label, color):
            ax.add_patch(Circle((x, y), .57, facecolor=color, edgecolor='#667487', linewidth=.7))
            ax.text(x, y, label, ha='center', va='center', fontsize=7, color='#253044')
        def arrow(a, b, dashed=False):
            ax.annotate('', xy=b, xytext=a, arrowprops={'arrowstyle':'-|>', 'color':'#476A85',
                         'lw':1.25, 'linestyle':'--' if dashed else '-'})
        node(1.1, 2.8, 'Input A', p[3]); node(2.65, 1.5, 'Input B', p[4])
        node(5.95, 2.25, 'Process', p[1])
        # Dark-blue fill needs white node text.
        ax.texts[-1].set_color('white')
        node(10.05, 3.1, 'Readout A', p[3]); node(10.05, 1.3, 'Readout B', p[4])
        arrow((1.7, 2.8), (5.3, 2.35)); arrow((3.2, 1.6), (5.35, 2.1))
        arrow((6.55, 2.4), (9.4, 3.05)); arrow((6.55, 2.0), (9.4, 1.35), dashed=True)
        ax.text(.2, .55, 'Entity identity uses color + label', fontsize=6.5, color='#28354A')
        ax.text(4.3, .55, 'Background marks spatial grouping', fontsize=6.5, color='#28354A')
        ax.text(8.4, .55, 'Dashed = illustrative alternate route', fontsize=6.1, color='#28354A')
        paths = save_figure(fig, str(output)+'-mechanism', dpi=240)
        plt.close(fig)
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    p = sub.add_parser('palette'); p.add_argument('name')
    for command in ('preview', 'demo'):
        p = sub.add_parser(command)
        p.add_argument('--output', required=True, help='Output prefix, without extension')
    args = parser.parse_args()
    if args.command == 'list':
        for row in corpus()['palettes']:
            print(f"{row['id']:28} {row['kind']:20} {len(row['colors']):2} {row['source']}")
    elif args.command == 'palette':
        try:
            print(json.dumps(palette_record(args.name), ensure_ascii=False, indent=2))
        except ValueError as error:
            parser.error(str(error))
    else:
        import matplotlib
        matplotlib.use('Agg')
        if args.command == 'preview':
            paths = preview(args.output)
        else:
            paths = statistical_demo(args.output) + mechanism_demo(args.output)
            manifest = {
                'data': 'synthetic; fixed random seed 381; not experimental results',
                'statistical_sources': ['IMG_3030', 'IMG_3031', 'IMG_3032', 'IMG_3049'],
                'mechanism_sources': ['IMG_3033', 'IMG_3038', 'IMG_3046'],
                'statistical_canvas_mm': [180, 140], 'mechanism_canvas_mm': [180, 95],
                'matplotlib_version': matplotlib.__version__, 'outputs': [Path(p).name for p in paths],
            }
            Path(str(args.output)+'-design.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
        print('\n'.join(paths))


if __name__ == '__main__':
    main()
