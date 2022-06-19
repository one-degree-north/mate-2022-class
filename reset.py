from controls import Controls

controls = Controls()
controls.resetOffshore()
controls.setOrientationAutoreport(10)
controls.comms.readThread()