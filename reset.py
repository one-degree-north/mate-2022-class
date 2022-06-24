from controls import Controls

controls = Controls(onshoreEnabled=False)
controls.resetOffshore()
# controls.setOrientationAutoreport(1)
controls.comms.readThread()