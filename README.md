# Files for ATMO

Utilities and notes for atmospheric model file preparation.

## Current script

`create_spectrum.py` converts a BT-Settl XML spectrum onto the wavenumber grid of a NetCDF file and writes the interpolated flux into the `hnu` variable.

Before running it, update these paths in the script:

- `nc_file`
- `xml_file`
- `nc_file_hd209`
- `nc_file_new`
You can download BT-Settle XML spectrum file in http://svo2.cab.inta-csic.es/theory/newov2/index.php?models=bt-settl, choose VOTtable when downloading

Then run:

```bash
python create_spectrum.py
```

Large input and output files such as `.nc`, `.ncdf`, `.h5`, and `.hdf` are ignored by Git in this repository.
