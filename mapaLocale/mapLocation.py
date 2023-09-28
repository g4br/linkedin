import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from cartopy.feature import NaturalEarthFeature
import cartopy.feature as cfeature
from scale import scale_bar

from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

"""
Plota um mapa centrado nas coordenadas fornecidas com um determinado nível de zoom.

Parâmetros:
- ax (matplotlib.axes): Eixo onde o mapa será plotado.
- latitude (float): Latitude central do mapa.
- longitude (float): Longitude central do mapa.
- zoom (float): Determina a extensão do mapa ao redor do ponto central.
"""
def plot_map(ax, latitude, longitude, zoom):
	ax.set_extent([longitude - zoom, longitude + zoom, latitude - zoom, latitude + zoom], crs=ccrs.PlateCarree())
	ax.plot(longitude,latitude,marker="*",color='k',ms = 20, transform=ccrs.PlateCarree(),zorder=98)
	ax.plot(longitude,latitude,marker="*",color='w',ms = 15, transform=ccrs.PlateCarree(),zorder=99)
	# desenha fonteiras
	states = NaturalEarthFeature(category='cultural', scale='50m',facecolor='none',name='admin_1_states_provinces_lines',edgecolor='k')
	ax.add_feature(cfeature.BORDERS,linewidth=.5, edgecolor='k')
	ax.add_feature(states, linewidth=.125, edgecolor='k')
	ax.coastlines('50m', linewidth=.5, color='k')
	# Define xticks e yticks
	ax.set_xticks([longitude - zoom, longitude - zoom/2, longitude, longitude + zoom/2, longitude + zoom], crs=ccrs.PlateCarree())
	ax.set_yticks([latitude - zoom, latitude - zoom/2, latitude, latitude + zoom/2, latitude + zoom], crs=ccrs.PlateCarree())
	# Define xticklabels e yticklabels
	lon_formatter = LongitudeFormatter(number_format='.1f', degree_symbol='', dateline_direction_label=True)
	lat_formatter = LatitudeFormatter(number_format='.1f', degree_symbol='')
	ax.xaxis.set_major_formatter(lon_formatter)
	ax.yaxis.set_major_formatter(lat_formatter)
	ax.yaxis.set_label_position("right")
	ax.yaxis.tick_right()
	# Desativando os rótulos padrões
	ax.grid(False)
	# Adicionar barra de escala
	scale_bar(ax, ccrs.PlateCarree(), zoom*100)


# backgrouns
satelite = cimgt.GoogleTiles(url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.jpg')
stamen = cimgt.Stamen(style='terrain-background')

# ponto central
latitude, longitude = -30.066356130832947, -51.16407841641491


# começa o plot
fig = plt.figure(figsize=(16, 12))
gs = gridspec.GridSpec(3, 2, figure=fig, hspace=1, wspace=1) 

# Figura principal ocupando as posições [:2, :2]
ax1 = fig.add_subplot(gs[:2, :2], projection=ccrs.PlateCarree())
plot_map(ax1, latitude, longitude, 0.005)
ax1.add_image(satelite,16) 
ax1.set_xticks([])
ax1.set_yticks([])

# Figura secundária na posição [0,1]
ax2 = fig.add_subplot(gs[0, -1], projection=ccrs.PlateCarree())
plot_map(ax2, latitude, longitude, 1)
ax2.add_image(stamen,6) 

# Figura terceira na posição [1,1]
ax3 = fig.add_subplot(gs[1, -1], projection=ccrs.PlateCarree())
plot_map(ax3, latitude, longitude, 3)
ax3.add_image(stamen,4) 

# Ajuste das margens
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
plt.show()
