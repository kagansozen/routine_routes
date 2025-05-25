import gpxpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import numpy as np
from matplotlib import font_manager

with open("samoens_Run.gpx", "r") as f:
    gpx = gpxpy.parse(f)

coords = [(p.longitude, p.latitude) for tr in gpx.tracks for seg in tr.segments for p in seg.points]

min_lon, max_lon = min(c[0] for c in coords), max(c[0] for c in coords)
min_lat, max_lat = min(c[1] for c in coords), max(c[1] for c in coords)

fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_xlim(min_lon, max_lon)
ax.set_ylim(min_lat, max_lat)
ax.axis('off')

xs = [c[0] for c in coords]
ys = [c[1] for c in coords]

line_outline, = ax.plot([], [], color='navy', lw=7, alpha=0.8)
line_main, = ax.plot([], [], lw=3, alpha=0.7)

flag_size = (max_lat - min_lat) * 0.09
flag_width = flag_size * 4.5
flag_height = flag_size * 2

center_x = (min_lon + max_lon) / 2 - flag_width / 2
center_y = (min_lat + max_lat) / 2 + flag_height / 4

def draw_flag(x, y, size):
    width = size * 4.5
    height = size * 2
    rects = []
    rects.append(Rectangle((x, y), width/3, height, color='#0055A4', zorder=5))
    rects.append(Rectangle((x + width/3, y), width/3, height, color='white', zorder=5))
    rects.append(Rectangle((x + 2*width/3, y), width/3, height, color='#EF4135', zorder=5))
    for r in rects:
        ax.add_patch(r)

draw_flag(center_x, center_y, flag_size)

font_prop = font_manager.FontProperties(family='PF Playskool Pro Regular', weight='400')
txt = ax.text(center_x + flag_width/2, center_y - flag_size*0.3, 'Samoens - Christmas 2023', color='white', fontsize=8,
              ha='center', va='top', zorder=6, fontproperties=font_prop)

def flashing_color(i):
    if (i // 10) % 2 == 0:
        return '#FFFF66'
    else:
        return '#FFFFB2'

def update(num):
    line_outline.set_data(xs[:num], ys[:num])
    line_main.set_data(xs[:num], ys[:num])
    if num > 0:
        line_main.set_color(flashing_color(num))
    else:
        line_main.set_color('#FFFF66')
    return line_outline, line_main, txt

ani = animation.FuncAnimation(fig, update, frames=len(coords), interval=50, blit=True, repeat=False)

plt.show()

ani.save('route_animation.mp4', writer='ffmpeg', fps=20, dpi=150)
fig.savefig('route_snapshot.png', dpi=150, facecolor='black')