import datetime
{project=QHIPP, properties={Q_WF_VERSION=1.0, Q_WF_STATUS=RUNNING, Q_WF_NAME=ligandomicsid_v1_0_2016, Q_WF_EXECUTED_BY=iismo01, Q_WF_STARTED_AT=2016-10-19 10:59:19 +0000}, code=QHIPPE176, space=MNF_ELK, type=Q_WF_MS_LIGANDOMICS_ID}
def setProperties(tr, exp, props):
  print "props "+props
  for prop in props.keySet():
    if prop == "ENZYMES":
      m = 0
      matType = "Q_PROTEASE_PROTOCOL"
      matCode = project+"_Proteases"
      while tr.getMaterial(matCode, matType):
        m += 1
        matCode = project+"_Proteases"+str(m)
      material = tr.createNewMaterial(matCode, matType)
      enzymes = props.get("ENZYMES")
      i = 0
      for e in enzymes:
        i+=1
        material.setPropertyValue("Q_PROTEASE_"+str(i),e)
      exp.setPropertyValue("Q_PROTEASE_DIGESTION", matCode)
    else:
      if prop == "Q_PREPARATION_DATE":
        time = props.get(prop)
        date = datetime.datetime.strptime(time, "%d-%m-%Y").strftime('%Y-%m-%d %H:%M:%S')
        exp.setPropertyValue(prop, date)
      else:
        if props.get(prop):
          try:
            val = props.get(prop)
            val = str(val)
          except:
            val = unicode(val,"utf-8")
            val = val.encode("utf-8")
          exp.setPropertyValue(prop, val)

def process(tr, parameters, tableBuilder):
  """Create a new experiment with the code specified in the parameters

  """
  user = parameters.get("user")
  if user:
    tr.setUserId(user)

  codes = parameters.get("codes")
  if not codes:
    codes = [parameters.get("code")]
  types = parameters.get("types")
  if not types:
    types = [parameters.get("type")]
  project = parameters.get("project")
  space = parameters.get("space")
  props = parameters.get("properties")
  # only one experiment
  if not codes:
    props = [props]

  for data in zip(codes, types, props):
    print "data "+data
    expId = "/" + space + "/" + project + "/" + data[0]
    exp = tr.createNewExperiment(expId, data[1])
    if not data[2] == None:
      setProperties(tr, exp, data[2])