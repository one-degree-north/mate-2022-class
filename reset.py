from controls import Controls

controls = Controls()
controls.resetOffshore()
controls.setOrientationAutoreport(1)
controls.comms.readThread()