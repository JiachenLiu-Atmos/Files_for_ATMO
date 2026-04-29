#%%
import xml.etree.ElementTree as ET
import numpy as np
from netCDF4 import Dataset
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
# ---------- Define file path, change it into yours ----------
nc_file = 'your_file_path/HD86226.ncdf'
xml_file = 'your_file_path/BT-settle_HD86226.xml'

# ---------- Read NC file ----------
nc = Dataset(nc_file, 'r+')
nu_template = nc.variables['nu'][:]
nu_template = np.array(nu_template)
hnu_var = nc.variables['hnu']

# ---------- Read XML ----------
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
    if w > 0.:  # ignore wavelength = 0
        wavelength.append(w)
        flux.append(f)

wavelength = np.array(wavelength)
flux = np.array(flux)

# ---------- units ----------
wavelength_cm = wavelength * 1e-8  # Å -> cm
nu_xml = 1 / wavelength_cm        # cm^-1
hnu_xml = flux * wavelength_cm**2*1e8/4/np.pi   # erg/s/cm²/ster/cm^-1

# ---------- interpolate into NC file's unit----------
interp_func = interp1d(
    nu_xml,
    hnu_xml,
    kind='linear',
    bounds_error=False,
    fill_value=(hnu_xml[0], hnu_xml[-1])  # extrapolate，ingore NaN
)
hnu_new = interp_func(nu_template)

hnu_new = np.array(hnu_new, dtype=float)

# ---------- Write NC file ----------
hnu_var[:] = hnu_new
nc.close()

print("XML has been converted and stored in NC file！")
#%%
# ---------- Check your file is correct ----------
nc_file_hd209 = 'your_file_path/kurucz_hd209.ncdf'
nc_hd209 = Dataset(nc_file_hd209, 'r+')
nu_hd209 = nc_hd209.variables['nu'][:]
hnu_hd209 = nc_hd209.variables['hnu'][:]

nc_file_new = 'your_file_path/HD86226.ncdf'
c = Dataset(nc_file_new, 'r+')
nu_new = nc_new.variables['nu'][:]
hnu_new = nc_new.variables['hnu'][:]
#%%
plt.figure(figsize=(8,5))
plt.plot(nu_new[::100], hnu_new[::100], color='blue')
plt.plot(nu_hd209[::100], hnu_hd209[::100], color='orange')
plt.xlabel('Wavenumber (cm^-1)')
plt.ylabel('Flux (erg/s/cm^2/ster)')
plt.title('Interpolated Spectrum')
# plt.grid(True)
plt.show()
