#%%
import xml.etree.ElementTree as ET
import numpy as np
from netCDF4 import Dataset
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
# ---------- 文件路径 ----------
nc_file = '/Users/jiachenliu/Documents/data/Spectrum_file/HD86226.ncdf'
xml_file = '/Users/jiachenliu/Documents/data/Spectrum_file/BT-settle_HD86226.xml'

# ---------- 读取 NC 文件 ----------
nc = Dataset(nc_file, 'r+')
nu_template = nc.variables['nu'][:]
# 确保 nu_template 是普通 ndarray，避免 masked_array
nu_template = np.array(nu_template)
hnu_var = nc.variables['hnu']

# ---------- 读取 XML ----------
tree = ET.parse(xml_file)
root = tree.getroot()
ns = {'v': 'http://www.ivoa.net/xml/VOTable/v1.1'}

rows = root.findall('.//v:TABLEDATA/v:TR', ns)
wavelength = []
flux = []

for row in rows:
    cols = row.findall('v:TD', ns)
    w = float(cols[0].text)
    f = float(cols[1].text)
    if w > 0.:  # 忽略波长为0的点
        wavelength.append(w)
        flux.append(f)

wavelength = np.array(wavelength)
flux = np.array(flux)

# ---------- 单位转换 ----------
wavelength_cm = wavelength * 1e-8  # Å -> cm
nu_xml = 1 / wavelength_cm        # cm^-1
hnu_xml = flux * wavelength_cm**2*1e8/4/np.pi   # erg/s/cm²/ster/cm^-1

# ---------- 插值到原 NC 文件的 nu ----------
interp_func = interp1d(
    nu_xml,
    hnu_xml,
    kind='linear',
    bounds_error=False,
    fill_value=(hnu_xml[0], hnu_xml[-1])  # 使用边界值进行外推，避免 NaN
)
hnu_new = interp_func(nu_template)

# 确保 hnu_new 是普通 ndarray
hnu_new = np.array(hnu_new, dtype=float)

# ---------- 写入 NC 文件 ----------
hnu_var[:] = hnu_new
nc.close()

print("XML 数据已转换并写入原 NC 文件！")
#%%
# ---------- 文件路径 ----------
nc_file = '/Users/jiachenliu/software/atmo/run/HD86226c_eqchem/kurucz_hd209.ncdf'
nc = Dataset(nc_file, 'r+')
nu_hd209 = nc.variables['nu'][:]
hnu_hd209 = nc.variables['hnu'][:]

nc_file = '/Users/jiachenliu/software/atmo/run/HD86226c_eqchem/HD86226.ncdf'
c = Dataset(nc_file, 'r+')
nu_hd86226 = nc.variables['nu'][:]
hnu_hd86226 = nc.variables['hnu'][:]
#%%
plt.figure(figsize=(8,5))
plt.plot(nu_hd86226[::100], hnu_hd86226[::100], color='blue')
plt.plot(nu_hd209[::100], hnu_hd209[::100], color='orange')
plt.xlabel('Wavenumber (cm^-1)')
plt.ylabel('Flux (erg/s/cm^2/ster)')
plt.title('Interpolated Spectrum')
# plt.grid(True)
plt.show()