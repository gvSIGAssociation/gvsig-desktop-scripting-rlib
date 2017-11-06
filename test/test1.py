
from gvsig import *

import rlib
reload(rlib)

def console(msg,otype=0):
  print msg,

def main(*args):
  
  R = rlib.getREngine(console)
  R.setwd(R.getPathName(getResource(__file__, "data")))
  R.source(R.getPathName(getResource(__file__, "data/test.r")) )
  R.call("load_libraries")
  rasterfile=R.getTemp("r-output.tif")
  R.call("kernel", 
    R.getLayerDSN(getResource(__file__, "data/contorno.shp")),
    R.getLayerName(getResource(__file__, "data/contorno.shp")),
    rasterfile
  )
  R.end()
  
  loadRasterFile(rasterfile)
  """
<rprocess>
  <name>Proceso R de prueba</name>
  <group>Vectorial</group>
  <inputs>
    <input>
      <type>VectorLayer</type>
      <name>LAYER</name>
      <label>Capa vetorial de prueba</label>
      <shapetype>LINE</shapetype>
    </input>
    <input>
      <type>NumericalValue</type>
      <name>X</name>
      <label>Valor de X inicial</label>
      <valuetype>DOUBLE</valuetype>
    </input>
  </inputs>
  <outputs>
    <output>
      <type>VectorLayer</type>
      <name>X</name>
      <label>no se que poner aqui</label>
      <shapetype>LINE</shapetype>
    </output>
  </outputs>
</rprocess>

  """